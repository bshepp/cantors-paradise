# Cantor's Paradise

> *"No one shall expel us from the paradise that Cantor has created."*
> -- David Hilbert

A training data pipeline for fine-tuning a language model that thinks like Georg Cantor (1845--1918).

Not a chatbot that quotes him -- a model that reproduces his mathematical intuition, his theological framework, his combative precision, and his psychological landscape. The theology wasn't decoration; it was scaffolding. The depression wasn't incidental; it interleaved with his most productive periods. The conflict with Kronecker wasn't drama; it forced him to sharpen his foundations. All of it goes in.

## What This Does

Cantor's Paradise is a five-stage pipeline that takes primary and secondary sources about Georg Cantor and transforms them into weighted, annotated, formatted training data ready for LoRA/QLoRA fine-tuning.

```
Acquire --> Extract --> Annotate --> Format --> Fine-tune
```

The pipeline produces:
- **57 cataloged sources** across 8 reliability tiers, from Cantor's own letters (weight 1.0) down to E.T. Bell's fabrications (weight 0.0, excluded)
- **Segmented text** split by letter, paper section, theorem, or chapter
- **5-dimension annotations** (mathematical intuition, theology, Kronecker conflict, psychology, personal context) with 24 mathematical topic tags
- **Training data** in Llama, ChatML, OpenAI, and Alpaca formats with tier-weighted sampling
- **50 synthetic dialogues** in Cantor's first-person voice covering math, theology, debate, introspection, and counter-factual defense
- **18 contrastive examples** debunking Bell's fabrications and pop-psychology myths
- **33 validation questions** with automated evaluation (Bell-test, dimension coverage, consistency)

## Quick Start

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate
# Unix
source .venv/bin/activate

pip install -e .

# Initialize the source catalog (57 sources, all 8 tiers)
cantor db init
cantor db status

# Scrape freely available sources
cantor acquire all

# Process, annotate, and build training data
cantor process extract
cantor process segment
cantor annotate tag
cantor training build --format llama

# Generate synthetic and negative training examples
cantor training synthetic
cantor training negative

# Export validation questions
cantor eval export-questions
```

For fine-tuning (requires GPU and additional dependencies):

```bash
pip install -e ".[train]"

cantor finetune presets
cantor finetune train --preset 8b-qlora --train-data data/training/cantor_llama.jsonl
```

## Source Tiers

Every document ingested into the dataset is assigned a reliability weight based on proximity to Cantor's actual thought.

| Tier | Weight | Description | Rationale |
|------|--------|-------------|-----------|
| 1 | 1.0 | Cantor's own words -- papers, letters, manuscripts | Primary source. This IS the mind we're reconstructing. |
| 2 | 0.85 | Direct correspondents -- Dedekind, Mittag-Leffler, Hilbert | They understood the work and responded in real time. |
| 3 | 0.70 | Mathematical opponents -- Kronecker, Poincare, Brouwer | The opposition shaped his thinking. Include both sides. |
| 4 | 0.65 | Catholic theologians -- Gutberlet, Esser, Franzelin | The theological dialogue was NOT peripheral. |
| 5 | 0.55 | Serious historical scholarship (post-1970) | Dauben, Ferreiros, Hallett, Meschkowski, Grattan-Guinness. |
| 6 | 0.35 | Secondary mathematical exposition | Gets the results right, loses the thinking process. |
| 7 | 0.15 | Popular accounts | The "Cantor went mad" narrative. Negative examples only. |
| 8 | 0.0 | E.T. Bell's *Men of Mathematics* (1937) | Actively harmful. EXCLUDED. |

## Pipeline Stages

### 1. Acquire

Web scrapers for freely available sources:
- **jamesrmeyer.com** -- modern English translations of Cantor's major papers (1874, Grundlagen, diagonal argument, Beitrage)
- **archive.org** -- Jourdain's 1915 translation (public domain)
- **arXiv** -- recent scholarship on Cantor's theology
- **MacTutor** -- biography and chronology

Copyrighted sources (Dauben's biography, Meschkowski & Nilson's *Briefe*, Tapp's *Kardinalitat und Kardinale*) must be acquired manually and placed in `data/raw/`.

### 2. Process

- **Extract** text from PDF, HTML, and plain text files
- **Segment** into training units: letters (by date/salutation), papers (by section/theorem), books (by chapter)
- **Detect language** (German, English, French, Latin) and link parallel texts

### 3. Annotate

Every segment is tagged along five dimensions:

- **Mathematical intuition** -- diagonal argument, cardinality, ordinals, continuum hypothesis, well-ordering, transfinite arithmetic
- **Theological framework** -- Absolutum, Transfinitum, neo-Thomism, anti-Kantianism, Platonic realism, divine revelation
- **Kronecker conflict** -- finitism, institutional power, combative rhetoric, mathematical substance
- **Psychological landscape** -- depressive episodes, productive periods, hospitalizations, non-mathematical interests
- **Personal context** -- Halle career, family, DMV founding, supporters

Supports both rule-based keyword tagging and LLM-assisted annotation.

### 4. Training Data

- **Weighted sampling** with configurable Tier 1 oversampling
- **Four output formats**: Llama chat, ChatML, OpenAI JSONL, Alpaca instruction
- **Synthetic dialogues** in Cantor's voice covering all five dimensions
- **Contrastive examples** pairing Bell fabrications with historically grounded corrections

### 5. Fine-tune & Evaluate

- **Five model presets**: Llama 3.1 8B (QLoRA and full LoRA), Llama 3.1 70B (QLoRA), Qwen 2.5 7B, Mistral 7B
- **Validation set** with 33 questions across 6 categories
- **Bell-test**: automated check that the model reproduces zero Bell fabrications
- **Dimension coverage**: does the model draw on all five aspects of Cantor's mind?
- **Consistency check**: does the persona hold across repeated queries?

## Project Structure

```
cantors-paradise/
  cantor/                     # Python package
    cli.py                    # CLI entry point (click)
    db/                       # Source catalog (SQLite)
      schema.py               #   Database schema
      catalog.py              #   CRUD operations
      seed_data.py            #   57 pre-loaded sources
    acquire/                  # Web scrapers
      base.py                 #   Base scraper with rate limiting
      jamesrmeyer.py          #   jamesrmeyer.com (Cantor's papers)
      archive_org.py          #   archive.org (Jourdain 1915)
      arxiv.py                #   arXiv papers
      mactutors.py            #   MacTutor biography
      tracker.py              #   Acquisition status display
    process/                  # Text processing
      extract.py              #   PDF/HTML text extraction
      segment.py              #   Segmentation (letter/paper/book)
      language.py             #   Language detection, parallel texts
    annotate/                 # Annotation system
      schema.py               #   5-dimension schema, 24 math topics
      tagger.py               #   Rule-based + LLM-assisted tagging
    training/                 # Training data construction
      sampler.py              #   Tier-weighted sampling
      formatter.py            #   Multi-format output + system prompt
      synthetic.py            #   50 synthetic Cantor-voice dialogues
      negative.py             #   18 contrastive Bell-debunking pairs
    finetune/                 # Fine-tuning
      config.py               #   Model presets and hyperparameters
      train.py                #   HuggingFace Trainer + PEFT/LoRA
    eval/                     # Evaluation
      validation.py           #   33 validation questions
      evaluate.py             #   Scoring, Bell-test, consistency
  data/                       # Data directory (gitignored)
    raw/                      #   Downloaded source files
    processed/                #   Extracted text
    annotated/                #   Annotated segments
    training/                 #   Final JSONL training data
    eval/                     #   Evaluation results
  PROJECT_CANTOR_SEED.md      # Original design document
  pyproject.toml
  LICENSE
  README.md
```

## Key Themes the Model Must Internalize

1. **"The essence of mathematics lies in its freedom."** Mathematics is creative, not merely investigative.
2. **The Transfinitum is real.** Not a useful fiction, not a potential infinity. Actually infinite sets exist.
3. **The Absolute Infinite is beyond mathematics.** The Absolutum (God) cannot be grasped by mathematical means. This is a structural feature of reality.
4. **Paradox is expected.** Cantor's religious beliefs led him to expect paradoxes in any concept of the infinite.
5. **Physical motivation.** Cantor was NOT a pure formalist. The transfinites were suggested to him by physical considerations.
6. **The continuum hypothesis feels true.** He was convinced but could never prove it. Godel (1940) and Cohen (1963) showed it's independent of ZFC.

## What Success Looks Like

A model that, given a novel mathematical question about infinity, reasons the way Cantor would have -- drawing on set-theoretic intuition, theological conviction, Platonic realism, and combative precision. A model that can argue with Kronecker. A model that sees the diagonal argument as obvious. A model that feels the continuum hypothesis is true and can articulate why, while acknowledging it cannot prove it.

A model that, when asked about its depression, responds with the dignity and honesty of a man who suffered but kept working.

A model that, when asked about God and infinity, speaks with the conviction of someone who believed -- genuinely, not metaphorically -- that he was revealing divine truth to the world.

## License

MIT
