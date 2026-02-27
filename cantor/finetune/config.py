"""Model and training hyperparameter configuration for LoRA/QLoRA fine-tuning."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    base_model: str = "meta-llama/Llama-3.1-8B-Instruct"
    output_dir: str = "output/cantor-model"

    # LoRA config
    lora_rank: int = 64
    lora_alpha: int = 128
    lora_dropout: float = 0.05
    target_modules: list[str] = field(default_factory=lambda: [
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ])

    # Quantization
    use_4bit: bool = True  # QLoRA
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_quant_type: str = "nf4"

    # Training
    learning_rate: float = 2e-4
    num_epochs: int = 3
    per_device_batch_size: int = 4
    gradient_accumulation_steps: int = 8
    warmup_ratio: float = 0.03
    weight_decay: float = 0.01
    max_seq_length: int = 2048

    # Logging
    logging_steps: int = 10
    save_strategy: str = "epoch"
    eval_strategy: str = "epoch"
    report_to: str = "wandb"  # or "tensorboard"
    run_name: str = "cantor-finetune"

    # Early stopping
    early_stopping_patience: int = 2
    metric_for_best_model: str = "eval_loss"


PRESETS = {
    "8b-qlora": ModelConfig(),
    "8b-full-lora": ModelConfig(use_4bit=False, per_device_batch_size=2),
    "70b-qlora": ModelConfig(
        base_model="meta-llama/Llama-3.1-70B-Instruct",
        lora_rank=32,
        lora_alpha=64,
        per_device_batch_size=1,
        gradient_accumulation_steps=16,
        max_seq_length=2048,
    ),
    "qwen-qlora": ModelConfig(
        base_model="Qwen/Qwen2.5-7B-Instruct",
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj",
        ],
    ),
    "mistral-qlora": ModelConfig(
        base_model="mistralai/Mistral-7B-Instruct-v0.3",
    ),
}
