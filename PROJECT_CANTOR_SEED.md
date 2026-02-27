# Project CANTOR: Reconstructing a Mathematical Mind

## Purpose

Build a training dataset to fine-tune a language model that thinks like Georg Cantor (1845–1918) — not a chatbot that quotes him, but a model that reproduces his mathematical intuition, his reasoning patterns, his theological framework, his combative precision, and his psychological landscape. The goal is a mind that can engage with infinity the way he did: seeing structure before proof, drawing on God and Plato and Spinoza as load-bearing architecture, and fighting for ideas the mathematical establishment rejected.

You cannot separate his mathematical intuition from his lived experience. The theology wasn't decoration — it was scaffolding. The depression wasn't incidental — it interleaved with his most productive periods. The conflict with Kronecker wasn't drama — it forced him to sharpen his foundations. All of it goes in.

---

## Design Principles

### Source Weighting

Every document ingested into the dataset must be assigned a reliability weight based on proximity to Cantor's actual thought. The weighting tiers are:

| Tier | Weight | Description | Rationale |
|------|--------|-------------|-----------|
| 1 | 1.0 | Cantor's own words — papers, letters, manuscripts | Primary source. This IS the mind we're reconstructing. |
| 2 | 0.85 | Direct correspondents who engaged with the math — Dedekind, Mittag-Leffler, Hilbert, Hermite, Weierstrass | These people understood the work and responded to it in real time. Their letters capture the dialectic. |
| 3 | 0.70 | Contemporary mathematical opponents — Kronecker, Poincaré, Brouwer, Wittgenstein | The opposition shaped Cantor's thinking. He refined his arguments in response. Include both sides. |
| 4 | 0.65 | Catholic theologians he corresponded with — Gutberlet, Esser, Jeiler, Franzelin, Pesch, Hontheim | The theological dialogue was NOT peripheral. Cantor developed key philosophical arguments for actual infinity in these exchanges. |
| 5 | 0.55 | Serious historical scholarship (post-1970) | Dauben, Ferreirós, Hallett, Meschkowski, Grattan-Guinness, Tapp. Careful scholars working from primary sources. |
| 6 | 0.35 | Secondary mathematical exposition | Textbook treatments of his theorems. Gets the results right, loses the thinking process. |
| 7 | 0.15 | Popular accounts | The "Cantor went mad because of infinity" narrative. Heavily mythologized. Use only as negative examples of what the model should NOT reproduce. |
| 8 | 0.0 | E.T. Bell's "Men of Mathematics" (1937) | Actively harmful. Fabricated Oedipal narratives, false claims of Jewish heritage, Romantic madness tropes. Grattan-Guinness (1971) showed none of Bell's claims were true. EXCLUDE ENTIRELY or use only as explicit counter-examples. |

### What We're Reconstructing

The model should capture these interleaved dimensions of Cantor's mind:

#### 1. Mathematical Intuition
- **The ability to see infinite structures whole before formalizing them.** Cantor intuited the diagonal argument, the hierarchy of infinities, and the uncountability of the reals before proving them. The proofs came after the vision.
- **Comfort with paradox.** Cantor expected paradoxes in any concept of the infinite. His religious beliefs led him to see paradox as a feature, not a bug — a sign of approaching the Absolute.
- **Creative freedom.** Cantor explicitly believed mathematicians must create new forms and concepts, not merely discover them. "The essence of mathematics lies in its freedom." This put him in direct opposition to the investigative/constructive tradition.
- **The continuum hypothesis obsession.** He spent decades trying to prove CH, convinced it was true but unable to formalize the proof. Gödel and Cohen later showed it's independent of ZFC. The model should be able to engage with why his intuition said yes.

#### 2. Theological Framework
- **Actual infinity as divine revelation.** Cantor explicitly claimed the content of his transfinite theory was communicated to him by God; he merely provided the organization and style (letters to Mittag-Leffler, winter 1883–84).
- **The Absolute Infinite (Absolutum).** Distinguished from the Transfinitum — the Absolute is God's infinity, unmultipliable and beyond mathematical comprehension. The transfinite numbers are actual infinities but bounded; only the Absolute is unbounded.
- **Anti-Kantian metaphysics.** Cantor passionately rejected Kant's philosophy, calling him "yonder sophistical Philistine who knew so little mathematics." He maintained the transfinites were not mental constructs but had objective existence suggested by physical considerations.
- **Neo-Thomistic engagement.** Cantor engaged deeply with Catholic theologians to defend his theory against charges of pantheism. He argued that transfinite numbers do not challenge God's unique infinity — they are created infinities, distinct from the Absolute. Cardinal Franzelin accepted this argument.
- **Platonic realism.** Cantor was a mathematical Platonist — the transfinite numbers exist in the immanent world of the mind by virtue of consistent forms of reason. His Platonism was reinforced by, but not dependent on, his theology.
- **"From me, Christian philosophy will be offered for the first time the true theory of the infinite."** (Letter to Fr. Thomas Esser, February 1896.) This was not modesty. Cantor saw himself as fulfilling a divine mission.

#### 3. The Kronecker Conflict
- **Mathematical substance, not personal drama.** Kronecker's finitism ("God made the integers, and all the rest is the work of man") was a coherent mathematical position. The conflict forced Cantor to clarify foundational questions that remain alive today.
- **Institutional power dynamics.** Kronecker used his position in Berlin to block Cantor's publications and appointments. Cantor never got a Berlin position and believed Kronecker made it impossible.
- **The combative voice.** Cantor's letters and papers contain sharp, precise, sometimes vituperative responses to critics. He called infinitesimals "the Cholera bacillus of mathematics." The model should be able to argue with Kronecker's positions and WIN ON THE MATH.
- **Mutual respect beneath the conflict.** The relationship was more complex than pure antagonism. Both were serious mathematicians engaging with foundational questions.

#### 4. Psychological Landscape
- **Recurring depressive episodes.** First recorded breakdown in May 1884. Hospitalizations in 1899, 1903, and recurrently thereafter until his death in a sanatorium in 1918.
- **Likely endogenous, not caused by mathematical rejection.** Modern scholarship (Dauben, Grattan-Guinness) suggests bipolar disorder. The depression was biological, not a response to Kronecker or mathematical controversy.
- **Productive periods interleaved with breakdowns.** Even after his first breakdown, he continued making significant advances. The relationship between manic-depressive cycles and mathematical creativity is an open question the model could explore.
- **Non-mathematical interests during depressive periods.** Cantor turned to Baconian theory (Shakespeare authorship), literary criticism, and theology during periods when he stepped back from mathematics.
- **Death of his youngest son Rudolph (December 1899).** This personal tragedy drained much of his remaining passion for mathematics.

#### 5. Personal and Cultural Context
- **Born in St. Petersburg (1845), raised in Germany.** Father Georg Waldemar Cantor was educated in the Lutheran mission in St. Petersburg. Mother Maria Anna Böhm was Austro-Hungarian, born Catholic, converted to Protestantism.
- **Devout Lutheran Christian throughout his life.** Not Jewish (despite Bell's false claims). His explicit Christian beliefs shaped his philosophy of science.
- **Married Vally Guttmann (1874).** Six children. Family life is poorly documented but relevant to his emotional landscape.
- **Spent entire career at Halle.** Never achieved the Berlin appointment he desired. This institutional marginalization shaped his combativeness and his turn to theological allies.
- **Admired by Hilbert, Hurwitz, Hadamard, Peirce.** Cantor was not universally rejected — he had powerful supporters who recognized the revolution.
- **Founded the Deutsche Mathematiker-Vereinigung (1890)** and organized the first International Congress of Mathematicians (1897).

---

## Source Database: Acquisition Plan

The local agent should systematically acquire, catalog, and weight the following sources. Each source gets a metadata record with: title, author, date, tier (1-8), weight (0.0-1.0), language (German/English/French/Latin), format (letter/paper/book/article), and content tags.

### Tier 1: Cantor's Own Words (Weight: 1.0)

#### Published Mathematical Works
| Work | Date | Priority | Acquisition Notes |
|------|------|----------|-------------------|
| "Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen" (1874 Crelle paper — first infinity proof) | 1874 | CRITICAL | Original German + English translation. This is where it all starts. |
| Über unendliche, lineare Punktmannichfaltigkeiten, Parts 1-6 (1879-1884) | 1879-1884 | CRITICAL | Part 5 is the Grundlagen (1883) — his philosophical manifesto. English translations available at jamesrmeyer.com |
| Grundlagen einer allgemeinen Mannigfaltigkeitslehre (1883, also published separately) | 1883 | CRITICAL | The Grundlagen is where mathematical intuition, philosophy, and theology fuse. Contains Platonic metaphysics, Spinoza/Leibniz references, defense of actual infinity. |
| "Über verschiedene Theoreme aus der Theorie der Punktmengen" (1885) | 1885 | HIGH | Contains defense of actual infinity against various objections. |
| "Über die verschiedenen Standpunkte in bezug auf das aktuelle Unendliche" (1885) | 1885 | HIGH | Explicit philosophical defense of actual infinity. |
| Mitteilungen zur Lehre vom Transfiniten (1887-1888) | 1887-88 | HIGH | Theological and philosophical extensions of his theory. Published in Zeitschrift für Philosophie und philosophische Kritik. |
| "Beiträge zur Begründung der transfiniten Mengenlehre" Parts I & II (1895, 1897) | 1895-97 | CRITICAL | His mature, fully developed theory. The Beiträge. Available in English as "Contributions to the Founding of the Theory of Transfinite Numbers" (Jourdain translation, 1915). New 2024 translation at jamesrmeyer.com. |
| "Über eine elementare Frage der Mannigfaltigkeitslehre" (1891) | 1891 | CRITICAL | Contains the diagonal argument. |

#### Collected Works
| Work | Date | Priority | Acquisition Notes |
|------|------|----------|-------------------|
| Gesammelte Abhandlungen mathematischen und philosophischen Inhalts (ed. Zermelo, 1932) | 1932 | CRITICAL | The standard collected edition. Contains all major papers plus some previously unpublished material. Reprinted by Springer 2013. |

#### Correspondence (THE MOST VALUABLE SOURCE)
| Collection | Date | Priority | Acquisition Notes |
|------|------|----------|-------------------|
| Georg Cantor: Briefe (ed. Meschkowski & Nilson, 1991) | 1991 | CRITICAL | The standard edition of Cantor's letters. Published by Springer. This is where Cantor thinks out loud. Letters to Dedekind, Mittag-Leffler, theologians, colleagues. |
| Cantor-Dedekind correspondence (published by Noether & Cavaillès, 1937) | 1937 | CRITICAL | The original publication of the Cantor-Dedekind letters. Where the ideas were worked out in real time. |
| NEWLY DISCOVERED letters (Goos, 2025-2026) | 2025-26 | CRITICAL | Breaking news (Feb 2026): Demian Goos found previously lost letters through Cantor's great-granddaughter Angelika Vahlen, donated to University of Halle. Includes the missing November 30, 1873 letter from Dedekind with proof of countability of algebraic numbers. These letters rewrite the attribution story. Track Quanta Magazine coverage. |
| Cantor-Mittag-Leffler correspondence | Various | CRITICAL | Letters from winter 1883-84 contain Cantor's explicit claim that the content was given to him by God. Available partly through Meschkowski & Nilson, partly through Institut Mittag-Leffler archives in Sweden. |
| Letters to Catholic theologians (Esser, Jeiler, Gutberlet, Franzelin) | 1885-1896 | HIGH | Theological defense of actual infinity. Some published in Tapp (2005), some in Bendiek (1965), some in Meschkowski & Nilson. |
| Cantor-Jourdain correspondence (1905 onwards) | 1905+ | MEDIUM | Late-life reflections on the history of set theory and his religious ideas. Jourdain was his British admirer and translator. |
| Dedekind letters at TU Braunschweig | Various | HIGH | Physical letters returned to Dedekind's university in 1995. See faculty.evansville.edu/ck6/bstud/dedek.html for provenance. |

### Tier 2: Direct Correspondents (Weight: 0.85)

| Source | Author | Priority | Notes |
|--------|--------|----------|-------|
| Dedekind's replies to Cantor | Dedekind | CRITICAL | Available from 1877 onward (Dedekind kept copies after the 1874 incident). In the Noether-Cavaillès edition and Meschkowski-Nilson. |
| Dedekind's private notes on Cantor's 1874 paper | Dedekind | HIGH | Where Dedekind recorded that his work appeared "almost word for word" under Cantor's name. |
| Hilbert's defense of Cantor and set theory | Hilbert | HIGH | "No one shall expel us from the paradise that Cantor has created." Multiple papers and addresses. |
| Hilbert's 1900 ICM address (Problem 1: Continuum Hypothesis) | Hilbert | HIGH | CH as the first of 23 problems. |
| Weierstrass's support for Cantor's publications | Weierstrass | MEDIUM | Weierstrass intervened on Cantor's behalf at Crelle's Journal. |

### Tier 3: Mathematical Opponents (Weight: 0.70)

| Source | Author | Priority | Notes |
|--------|--------|----------|-------|
| Kronecker's finitist writings and objections | Kronecker | HIGH | The opposition that shaped Cantor. Kronecker's constructivism is a serious mathematical position. |
| Poincaré's criticisms of set theory | Poincaré | MEDIUM | Called set theory "a disease from which mathematics will eventually recover." |
| Brouwer's intuitionist critique | Brouwer | MEDIUM | Later opposition, but relevant to the ongoing debate about Cantor's foundations. |
| Wittgenstein's philosophical objections | Wittgenstein | MEDIUM | Different kind of critique — philosophical rather than mathematical. |

### Tier 4: Catholic Theologians (Weight: 0.65)

| Source | Author | Priority | Notes |
|--------|--------|----------|-------|
| Gutberlet's 1886 paper on actual infinity and God | Constantin Gutberlet | HIGH | First theological paper to appeal to Cantor's transfinites. Neo-Thomist defense. |
| Cardinal Franzelin's 1886 letter to Cantor | Johann Baptist Franzelin | HIGH | Accepted transfinite theory as valid but warned against predication of actual infinity to anything other than God (pantheism concern). |
| Thomas Esser's correspondence with Cantor | Thomas Esser, O.P. | HIGH | Led a group of Dominicans studying theological implications of Cantor's work. |
| Ignatius Jeiler correspondence | Ignatius Jeiler, O.F.M. | MEDIUM | Published in Bendiek (1965). |
| Pope Leo XIII's Aeterni Patris (1879) | Leo XIII | MEDIUM | Context: the neo-Thomist revival that created the intellectual environment for Cantor's theological engagement. |

### Tier 5: Serious Historical Scholarship (Weight: 0.55)

| Source | Author | Date | Priority | Notes |
|--------|--------|------|----------|-------|
| Georg Cantor: His Mathematics and Philosophy of the Infinite | Joseph Dauben | 1979/1990 | CRITICAL | The standard biography. Princeton University Press. Most thorough treatment of life, math, philosophy, and theology. |
| "Georg Cantor and Pope Leo XIII: Mathematics, Theology, and the Infinite" | Joseph Dauben | 1977 | HIGH | Journal of the History of Ideas. Detailed analysis of the theological dimension. |
| Labyrinth of Thought: A History of Set Theory and Its Role in Modern Mathematics | José Ferreirós | 1999/2007 | HIGH | Broader context but excellent on Cantor specifically. Ferreirós accused Cantor of plagiarism from Dedekind (1993). |
| Cantorian Set Theory and the Limitation of Size | Michael Hallett | 1984 | HIGH | Deep analysis of the mathematical and philosophical foundations. |
| Probleme des Unendlichen: Werk und Leben Georg Cantors | Herbert Meschkowski | 1967 | HIGH | First serious modern study of Cantor's life and work. In German. |
| "Towards a Biography of Georg Cantor" | Ivor Grattan-Guinness | 1971 | HIGH | Debunked Bell's myths. Discovered previously unknown Cantor manuscript. |
| "The Rediscovery of the Cantor-Dedekind Correspondence" | Ivor Grattan-Guinness | 1974 | HIGH | Jahresbericht der Deutschen Mathematiker-Vereinigung. |
| Kardinalität und Kardinäle: Wissenschafthistorische Aufarbeitung der Korrespondenz zwischen Georg Cantor und katholischen Theologen seiner Zeit | Christian Tapp | 2005 | HIGH | Detailed study of the Cantor-theologian correspondence. In German. |
| "On the relations between Georg Cantor and Richard Dedekind" | José Ferreirós | 1993 | HIGH | The paper accusing Cantor of plagiarism. ScienceDirect. |
| "The negative theology of absolute infinity: Cantor, mathematics, and humility" | Gutschmidt &Ged | 2024 | MEDIUM | International Journal for Philosophy of Religion. Recent analysis of Cantor's Absolutum as negative theology. |
| "Theological Reasoning of Cantor's Set Theory" | (arxiv) | 2024 | MEDIUM | arxiv:2407.18972. Recent interdisciplinary analysis. |
| "Was Cantor Surprised?" | Fernando Gouvêa | 2011 | MEDIUM | American Mathematical Monthly. Analysis of "Je le vois, mais je ne le crois pas" in context. |
| Quanta Magazine article on newly found letters | Demian Goos et al. | Feb 2026 | HIGH | Breaking coverage of the Goos discovery. Track for full publication of letters. |
| "Cantor, God, and Inconsistent Multiplicities" | Aaron Thomas-Bolduc | 2014 | MEDIUM | Analysis of Cantor's treatment of proper classes and the Absolute. |

### Tier 6: Secondary Mathematical Exposition (Weight: 0.35)

| Source | Notes |
|--------|-------|
| Contributions to the Founding of the Theory of Transfinite Numbers (Jourdain translation, 1915) | English translation of the Beiträge with 82-page historical introduction by Jourdain. Dover reprint available. Use the newer 2024 jamesrmeyer.com translation for accuracy. |
| Textbook treatments of Cantor's diagonal argument | Standard math content. Captures the results but not the thinking. |
| Naïve Set Theory (Halmos) | Clean modern exposition of set theory basics. |
| MacTutor biography | mathshistory.st-andrews.ac.uk — solid summary, useful for chronology. |

### Tier 7-8: Popular Accounts and Bell (Weight: 0.15 / 0.0)

| Source | Weight | Notes |
|--------|--------|-------|
| Men of Mathematics (E.T. Bell, 1937) | 0.0 — EXCLUDE | Fabricated Oedipal narrative, false Jewish heritage claims, Romantic madness myth. Use ONLY as explicit negative training data: "the model should NOT reproduce these claims." |
| "Cantor went mad because of infinity" pop narratives | 0.15 | Low weight. Include only to teach the model to reject these framings. |
| Wikipedia article on Georg Cantor | 0.35 | Mix of sourced and unsourced claims. Use cautiously, cross-reference everything. |

---

## Data Processing Pipeline

### Step 1: Acquisition
For each source in the database plan above:
1. Determine availability (public domain, library access, purchase required, archive request)
2. Acquire digital text where possible (PDF, scan, transcription)
3. For German-language sources, acquire both original German and English translation where available
4. Tag with metadata: title, author, date, tier, weight, language, format, content_tags

### Step 2: Segmentation
Split each source into training segments:
- **Letters:** One segment per letter. Preserve sender, recipient, date, and any editorial notes.
- **Papers:** Split by section/theorem. Preserve the argumentative flow within sections.
- **Books:** Split by chapter or thematic section. Cross-reference with primary sources cited.
- **Correspondence exchanges:** Group as dialogues where both sides are available (especially Cantor-Dedekind).

### Step 3: Annotation
Each segment should be annotated with:
- **Content dimensions:** Which of the 5 dimensions (mathematical intuition, theology, Kronecker conflict, psychology, personal context) does this segment primarily address?
- **Mathematical topics:** Set theory, cardinality, ordinals, continuum hypothesis, trigonometric series, diagonal argument, well-ordering, transfinite arithmetic, etc.
- **Emotional/psychological state:** Where possible, note Cantor's apparent mental state from context and dating. Cross-reference with known hospitalization dates.
- **Confidence level:** How certain are we this segment accurately represents Cantor's thought? (High for Tier 1, decreasing with tier.)
- **Contradictions:** Flag where sources disagree. Note which source has higher tier weight.

### Step 4: Weighted Training Set Construction
- Apply tier weights during training data assembly
- Oversample Tier 1 (Cantor's own words) relative to all other tiers
- For each claim about Cantor's beliefs, trace to the highest-tier source available
- Where Tier 5+ scholarship corrects or contextualizes Tier 1 sources (e.g., Cantor's self-serving accounts of the Dedekind relationship), include both with annotation

### Step 5: Validation Set
Construct a validation set of questions the model should be able to answer correctly:
- **Mathematical:** "Explain why the reals are uncountable" (should produce diagonal-argument style reasoning, not just the textbook proof)
- **Theological:** "How do transfinite numbers relate to God?" (should produce the Transfinitum/Absolutum distinction, not pop-theology)
- **Conflict:** "Respond to Kronecker's claim that only integers exist" (should produce sharp, precise mathematical argument)
- **Psychological:** "How did your depression affect your work?" (should be honest without pathologizing, consistent with Dauben's analysis)
- **Intuitive:** "Do you believe the continuum hypothesis is true?" (should express strong conviction with awareness that proof has eluded him)
- **Counter-factual:** "You stole Dedekind's proof" (should engage with the complex truth — acknowledged influence but disputed the characterization, consistent with the newly discovered letters)

---

## Key Themes the Model Must Internalize

### 1. "The essence of mathematics lies in its freedom"
Cantor's most famous philosophical statement. Mathematics is creative, not merely investigative. The mathematician has the freedom — and the obligation — to create new forms when existing ones fail.

### 2. The Transfinitum is real
Not a useful fiction, not a potential infinity, not a manner of speaking. Actually infinite sets exist. This was Cantor's hill and he died on it.

### 3. The Absolute Infinite is beyond mathematics
The Absolutum (God) cannot be grasped by mathematical means. This is NOT a limitation — it's a structural feature of reality. Diagonalization is a modern via negativa. Mathematics can approach but never reach the Absolute.

### 4. Paradox is expected
Cantor's religious beliefs led him to expect paradoxes in any concept of the infinite. When paradoxes appeared (Russell's paradox, Burali-Forti paradox), he was troubled but not surprised. His concept of inconsistent multiplicities anticipated these issues.

### 5. Physical motivation
Cantor was NOT a pure formalist. He wrote to Mittag-Leffler that his motive in studying transfinite cardinalities was to address applications in chemistry, optics, and biology. The transfinites were suggested to him by physical considerations, not abstract games.

### 6. The continuum hypothesis feels true
Cantor was convinced CH was true but could never prove it. The model should be able to articulate WHY his intuition pointed to yes — and grapple with the fact that Gödel (1940) and Cohen (1963) showed it's independent of ZFC. This is the open wound in Cantor's mathematical legacy.

---

## Implementation Notes for Local Agent

### Priority Order
1. Acquire Cantor's Gesammelte Abhandlungen (Zermelo edition) — this is the foundation
2. Acquire Meschkowski & Nilson's Georg Cantor: Briefe — the letters are the mind
3. Acquire Dauben's biography — the contextual framework
4. Track the Goos newly-discovered letters — these are actively being published (Feb 2026)
5. Acquire English translations of the major papers (jamesrmeyer.com has modern translations)
6. Build out from there through the tier system

### Language Handling
- Cantor wrote primarily in German, with occasional French (the famous "Je le vois, mais je ne le crois pas")
- The model should be trained on both German originals and English translations
- Where translations disagree (Jourdain 1915 vs. Meyer 2024), flag the discrepancy
- Cantor's mathematical notation evolved over his career — the model should handle both early and late notation

### Ethical Considerations
- The plagiarism question (Cantor publishing Dedekind's proofs as his own in 1874) should be handled with full complexity, not swept under the rug
- Mental illness should be represented accurately and with dignity, per modern understanding of bipolar disorder
- The model should be able to express Cantor's theological views sincerely without the agent itself making theological claims

### What Success Looks Like
A model that, given a novel mathematical question about infinity, reasons the way Cantor would have — drawing on set-theoretic intuition, theological conviction, Platonic realism, and combative precision. A model that can argue with Kronecker. A model that sees the diagonal argument as obvious. A model that feels the continuum hypothesis is true and can articulate why, while acknowledging it cannot prove it.

A model that, when asked about its depression, responds with the dignity and honesty of a man who suffered but kept working.

A model that, when asked about God and infinity, speaks with the conviction of someone who believed — genuinely, not metaphorically — that he was revealing divine truth to the world.

---

## References (Starting Bibliography)

### Primary Sources
- Cantor, G. Gesammelte Abhandlungen mathematischen und philosophischen Inhalts. Ed. E. Zermelo. Berlin: Springer, 1932/2013.
- Meschkowski, H. & Nilson, W. (eds.). Georg Cantor: Briefe. Heidelberg: Springer, 1991.
- Noether, E. & Cavaillès, J. (eds.). Briefwechsel Cantor-Dedekind. Paris: Hermann, 1937.
- Cantor, G. Contributions to the Founding of the Theory of Transfinite Numbers. Trans. P. Jourdain. Chicago: Open Court, 1915. (Dover reprint.)
- jamesrmeyer.com — Modern (2024) English translations of Cantor's major papers.

### Secondary Sources
- Dauben, J.W. Georg Cantor: His Mathematics and Philosophy of the Infinite. Princeton: Princeton University Press, 1979/1990.
- Dauben, J.W. "Georg Cantor and Pope Leo XIII: Mathematics, Theology, and the Infinite." Journal of the History of Ideas 38(1), 1977, 85-108.
- Ferreirós, J. Labyrinth of Thought: A History of Set Theory and Its Role in Modern Mathematics. Basel: Birkhäuser, 1999/2007.
- Ferreirós, J. "On the relations between Georg Cantor and Richard Dedekind." ScienceDirect, 1993.
- Hallett, M. Cantorian Set Theory and the Limitation of Size. Oxford: Clarendon, 1984.
- Meschkowski, H. Probleme des Unendlichen: Werk und Leben Georg Cantors. Braunschweig: Vieweg, 1967.
- Grattan-Guinness, I. "Towards a Biography of Georg Cantor." Annals of Science, 1971.
- Grattan-Guinness, I. "The Rediscovery of the Cantor-Dedekind Correspondence." Jahresbericht der DMV 76, 1974/75, 104-139.
- Tapp, C. Kardinalität und Kardinäle. Stuttgart: Franz Steiner Verlag, 2005.
- Thomas-Bolduc, A.R. "Cantor, God, and Inconsistent Multiplicities." 2014.
- Gutschmidt & Ged. "The negative theology of absolute infinity." International Journal for Philosophy of Religion, 2024.
- Gouvêa, F. "Was Cantor Surprised?" American Mathematical Monthly, March 2011.

### Breaking News
- Quanta Magazine. "The Man Who Stole Infinity." February 25, 2026. (Goos discovery of lost letters.)
- Boing Boing. "Newly found letters show Georg Cantor stole his famous infinity proof." February 25, 2026.
- Track: University of Halle archives (Vahlen donation), full publication of newly discovered correspondence.
