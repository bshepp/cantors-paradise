"""HuggingFace Trainer integration for LoRA/QLoRA fine-tuning."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from cantor.finetune.config import ModelConfig

logger = logging.getLogger(__name__)

_GPU_LIBS_AVAILABLE = True
_IMPORT_ERROR_MSG: str | None = None

try:
    import torch
    from datasets import Dataset
    from peft import LoraConfig, PeftModel, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        EarlyStoppingCallback,
        Trainer,
        TrainingArguments,
    )
except ImportError as exc:
    _GPU_LIBS_AVAILABLE = False
    _IMPORT_ERROR_MSG = (
        f"Missing GPU/training dependencies ({exc}). "
        "Install them with: pip install torch transformers peft bitsandbytes accelerate datasets"
    )


def _check_deps() -> None:
    if not _GPU_LIBS_AVAILABLE:
        raise RuntimeError(_IMPORT_ERROR_MSG)


# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

def load_model(config: ModelConfig) -> tuple:
    """Load base model with optional 4-bit quantization and apply LoRA.

    Returns ``(model, tokenizer)``.
    """
    _check_deps()

    quantization_config = None
    if config.use_4bit:
        compute_dtype = getattr(torch, config.bnb_4bit_compute_dtype, torch.bfloat16)
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_quant_type=config.bnb_4bit_quant_type,
            bnb_4bit_use_double_quant=True,
        )

    logger.info("Loading base model %s", config.base_model)
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        quantization_config=quantization_config,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(
        config.base_model,
        trust_remote_code=True,
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.eos_token_id

    if config.use_4bit:
        model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=config.lora_rank,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        target_modules=config.target_modules,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    trainable, total = 0, 0
    for param in model.parameters():
        total += param.numel()
        if param.requires_grad:
            trainable += param.numel()
    logger.info(
        "Trainable parameters: %s / %s (%.2f%%)",
        f"{trainable:,}", f"{total:,}", 100 * trainable / total,
    )

    return model, tokenizer


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

def load_dataset(data_path: Path, tokenizer, max_length: int) -> Dataset:
    """Load a JSONL file in chat/messages format and tokenize via the chat template.

    Each JSONL line must have a ``"messages"`` key containing a list of
    ``{"role": ..., "content": ...}`` dicts.
    """
    _check_deps()

    records: list[dict] = []
    with open(data_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    if not records:
        raise ValueError(f"No records found in {data_path}")

    def _tokenize(example: dict) -> dict:
        text = tokenizer.apply_chat_template(
            example["messages"],
            tokenize=False,
            add_generation_prompt=False,
        )
        encoded = tokenizer(
            text,
            truncation=True,
            max_length=max_length,
            padding=False,
        )
        encoded["labels"] = encoded["input_ids"].copy()
        return encoded

    ds = Dataset.from_list(records)
    ds = ds.map(_tokenize, remove_columns=ds.column_names)
    return ds


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train(
    config: ModelConfig,
    train_path: Path,
    val_path: Path | None = None,
) -> Path:
    """Run the full LoRA/QLoRA fine-tuning loop.

    Returns the path to the saved adapter directory.
    """
    _check_deps()

    model, tokenizer = load_model(config)

    logger.info("Loading training data from %s", train_path)
    train_ds = load_dataset(train_path, tokenizer, config.max_seq_length)

    val_ds = None
    if val_path is not None:
        logger.info("Loading validation data from %s", val_path)
        val_ds = load_dataset(val_path, tokenizer, config.max_seq_length)

    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.per_device_batch_size,
        per_device_eval_batch_size=config.per_device_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        warmup_ratio=config.warmup_ratio,
        weight_decay=config.weight_decay,
        logging_steps=config.logging_steps,
        save_strategy=config.save_strategy,
        eval_strategy=config.eval_strategy if val_ds is not None else "no",
        load_best_model_at_end=val_ds is not None,
        metric_for_best_model=config.metric_for_best_model if val_ds is not None else None,
        greater_is_better=False,
        report_to=config.report_to,
        run_name=config.run_name,
        bf16=True,
        optim="paged_adamw_8bit" if config.use_4bit else "adamw_torch",
        lr_scheduler_type="cosine",
        max_grad_norm=0.3,
        group_by_length=True,
        remove_unused_columns=False,
        dataloader_pin_memory=True,
    )

    callbacks = []
    if val_ds is not None:
        callbacks.append(
            EarlyStoppingCallback(early_stopping_patience=config.early_stopping_patience)
        )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        callbacks=callbacks,
    )

    logger.info("Starting training")
    trainer.train()

    adapter_path = output_dir / "final-adapter"
    model.save_pretrained(str(adapter_path))
    tokenizer.save_pretrained(str(adapter_path))
    logger.info("Adapter saved to %s", adapter_path)

    return adapter_path


# ---------------------------------------------------------------------------
# Merge adapter into base model
# ---------------------------------------------------------------------------

def merge_and_save(
    config: ModelConfig,
    adapter_path: Path,
    output_path: Path,
) -> None:
    """Merge LoRA weights into the base model and save the full merged model."""
    _check_deps()

    logger.info("Loading base model %s for merging", config.base_model)
    model = AutoModelForCausalLM.from_pretrained(
        config.base_model,
        device_map="auto",
        torch_dtype=torch.bfloat16,
        trust_remote_code=True,
    )

    logger.info("Loading adapter from %s", adapter_path)
    model = PeftModel.from_pretrained(model, str(adapter_path))
    model = model.merge_and_unload()

    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info("Saving merged model to %s", output_path)
    model.save_pretrained(str(output_path))

    tokenizer = AutoTokenizer.from_pretrained(
        str(adapter_path),
        trust_remote_code=True,
    )
    tokenizer.save_pretrained(str(output_path))

    logger.info("Merged model saved to %s", output_path)
