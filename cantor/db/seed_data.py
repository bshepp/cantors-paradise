"""Pre-populate the source catalog with every source from PROJECT_CANTOR_SEED.md."""

from __future__ import annotations

from pathlib import Path

from cantor.db.catalog import Source, add_sources_bulk
from cantor.db.schema import DB_PATH, init_db


def _tier1_sources() -> list[Source]:
    """Cantor's own words (weight 1.0)."""
    return [
        # --- Published mathematical works ---
        Source(
            title="Über eine Eigenschaft des Inbegriffes aller reellen algebraischen Zahlen",
            author="Georg Cantor",
            date="1874",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["first_infinity_proof", "algebraic_numbers", "uncountability"],
            url="https://www.jamesrmeyer.com/infinite/cantors-first-paper.html",
            notes="1874 Crelle paper — first infinity proof. Need original German + English translation.",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 1",
            author="Georg Cantor",
            date="1879",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "linear_manifolds"],
            url="https://www.jamesrmeyer.com/infinite/cantor-punkt1.html",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 2",
            author="Georg Cantor",
            date="1880",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "linear_manifolds"],
            url="https://www.jamesrmeyer.com/infinite/cantor-punkt2.html",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 3",
            author="Georg Cantor",
            date="1882",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "linear_manifolds"],
            url="https://www.jamesrmeyer.com/infinite/cantor-punkt3.html",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 4",
            author="Georg Cantor",
            date="1883",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "linear_manifolds"],
            url="https://www.jamesrmeyer.com/infinite/cantor-punkt4.html",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 5 (Grundlagen)",
            author="Georg Cantor",
            date="1883",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["grundlagen", "philosophy", "actual_infinity", "platonic_realism",
                          "spinoza", "leibniz", "mathematical_freedom"],
            url="https://www.jamesrmeyer.com/infinite/cantor-grundlagen.html",
            notes="The Grundlagen — philosophical manifesto. Mathematical intuition, philosophy, theology fuse here.",
        ),
        Source(
            title="Über unendliche, lineare Punktmannichfaltigkeiten, Part 6",
            author="Georg Cantor",
            date="1884",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "linear_manifolds"],
            url="https://www.jamesrmeyer.com/infinite/cantor-punkt6.html",
        ),
        Source(
            title="Grundlagen einer allgemeinen Mannigfaltigkeitslehre (separate publication)",
            author="Georg Cantor",
            date="1883",
            tier=1, weight=1.0, language="de", format="book",
            content_tags=["grundlagen", "manifold_theory", "philosophy", "theology"],
            notes="Also published as Part 5 above. Separate monograph with additional material.",
        ),
        Source(
            title="Über verschiedene Theoreme aus der Theorie der Punktmengen",
            author="Georg Cantor",
            date="1885",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["point_sets", "actual_infinity", "defense"],
        ),
        Source(
            title="Über die verschiedenen Standpunkte in bezug auf das aktuelle Unendliche",
            author="Georg Cantor",
            date="1885",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["actual_infinity", "philosophy", "defense"],
            notes="Explicit philosophical defense of actual infinity.",
        ),
        Source(
            title="Mitteilungen zur Lehre vom Transfiniten",
            author="Georg Cantor",
            date="1887-1888",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["transfinite", "theology", "philosophy"],
            notes="Published in Zeitschrift für Philosophie und philosophische Kritik.",
        ),
        Source(
            title="Über eine elementare Frage der Mannigfaltigkeitslehre",
            author="Georg Cantor",
            date="1891",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["diagonal_argument", "uncountability", "power_set"],
            url="https://www.jamesrmeyer.com/infinite/cantors-1891-proof.html",
            notes="Contains the diagonal argument.",
        ),
        Source(
            title="Beiträge zur Begründung der transfiniten Mengenlehre, Part I",
            author="Georg Cantor",
            date="1895",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["transfinite", "set_theory", "cardinality", "ordinals"],
            url="https://www.jamesrmeyer.com/infinite/cantors-beitrage.html",
            notes="Mature, fully developed theory. The Beiträge.",
        ),
        Source(
            title="Beiträge zur Begründung der transfiniten Mengenlehre, Part II",
            author="Georg Cantor",
            date="1897",
            tier=1, weight=1.0, language="de", format="paper",
            content_tags=["transfinite", "set_theory", "well_ordering", "ordinals"],
            url="https://www.jamesrmeyer.com/infinite/cantors-beitrage2.html",
        ),
        # --- Collected works ---
        Source(
            title="Gesammelte Abhandlungen mathematischen und philosophischen Inhalts",
            author="Georg Cantor (ed. Zermelo)",
            date="1932",
            tier=1, weight=1.0, language="de", format="collection",
            content_tags=["collected_works", "complete"],
            notes="The standard collected edition. Reprinted Springer 2013. Foundation source.",
        ),
        # --- Correspondence ---
        Source(
            title="Georg Cantor: Briefe",
            author="Georg Cantor (ed. Meschkowski & Nilson)",
            date="1991",
            tier=1, weight=1.0, language="de", format="collection",
            content_tags=["letters", "correspondence", "dedekind", "mittag-leffler",
                          "theologians", "colleagues"],
            notes="THE MOST VALUABLE SOURCE. Standard edition of letters. Springer.",
        ),
        Source(
            title="Cantor-Dedekind correspondence (Noether & Cavaillès edition)",
            author="Georg Cantor; Richard Dedekind",
            date="1937",
            tier=1, weight=1.0, language="de", format="collection",
            content_tags=["letters", "dedekind", "correspondence", "ideas_in_real_time"],
            notes="Original publication of the Cantor-Dedekind letters.",
        ),
        Source(
            title="Newly discovered letters (Goos, 2025-2026)",
            author="Georg Cantor; Richard Dedekind",
            date="2025-2026",
            tier=1, weight=1.0, language="de", format="letter",
            content_tags=["letters", "dedekind", "newly_discovered", "attribution",
                          "countability_proof"],
            notes="Breaking: Goos found previously lost letters via great-granddaughter Angelika Vahlen. Includes missing Nov 30, 1873 letter from Dedekind. Track Quanta Magazine coverage.",
        ),
        Source(
            title="Cantor-Mittag-Leffler correspondence (winter 1883-84)",
            author="Georg Cantor; Gösta Mittag-Leffler",
            date="1883-1884",
            tier=1, weight=1.0, language="de", format="letter",
            content_tags=["letters", "mittag-leffler", "divine_revelation",
                          "theology", "god"],
            notes="Contains explicit claim that transfinite content was given by God. Partly in Meschkowski & Nilson, partly at Institut Mittag-Leffler archives in Sweden.",
        ),
        Source(
            title="Letters to Catholic theologians (Esser, Jeiler, Gutberlet, Franzelin)",
            author="Georg Cantor",
            date="1885-1896",
            tier=1, weight=1.0, language="de", format="letter",
            content_tags=["letters", "theology", "actual_infinity", "neo-thomism",
                          "dominicans", "franciscans"],
            notes="Some in Tapp (2005), some in Bendiek (1965), some in Meschkowski & Nilson.",
        ),
        Source(
            title="Cantor-Jourdain correspondence",
            author="Georg Cantor; Philip Jourdain",
            date="1905+",
            tier=1, weight=1.0, language="en", format="letter",
            content_tags=["letters", "late_life", "history_of_set_theory", "religion"],
            notes="Late-life reflections. Jourdain was his British admirer and translator.",
        ),
        Source(
            title="Dedekind letters at TU Braunschweig",
            author="Georg Cantor; Richard Dedekind",
            date="various",
            tier=1, weight=1.0, language="de", format="letter",
            content_tags=["letters", "dedekind", "physical_archive"],
            url="https://faculty.evansville.edu/ck6/bstud/dedek.html",
            notes="Physical letters returned to Dedekind's university in 1995.",
        ),
    ]


def _tier2_sources() -> list[Source]:
    """Direct correspondents (weight 0.85)."""
    return [
        Source(
            title="Dedekind's replies to Cantor (from 1877 onward)",
            author="Richard Dedekind",
            date="1877+",
            tier=2, weight=0.85, language="de", format="letter",
            content_tags=["dedekind", "correspondence", "replies"],
            notes="Available in Noether-Cavaillès edition and Meschkowski-Nilson. Dedekind kept copies after the 1874 incident.",
        ),
        Source(
            title="Dedekind's private notes on Cantor's 1874 paper",
            author="Richard Dedekind",
            date="1874",
            tier=2, weight=0.85, language="de", format="other",
            content_tags=["dedekind", "private_notes", "1874_paper", "plagiarism_question"],
            notes="Where Dedekind recorded that his work appeared 'almost word for word' under Cantor's name.",
        ),
        Source(
            title="Hilbert's defense of Cantor and set theory",
            author="David Hilbert",
            date="various",
            tier=2, weight=0.85, language="de", format="paper",
            content_tags=["hilbert", "defense", "paradise", "set_theory"],
            notes="'No one shall expel us from the paradise that Cantor has created.'",
        ),
        Source(
            title="Hilbert's 1900 ICM address (Problem 1: Continuum Hypothesis)",
            author="David Hilbert",
            date="1900",
            tier=2, weight=0.85, language="de", format="paper",
            content_tags=["hilbert", "continuum_hypothesis", "23_problems", "ICM"],
            notes="CH as the first of 23 problems.",
        ),
        Source(
            title="Weierstrass's support for Cantor's publications",
            author="Karl Weierstrass",
            date="various",
            tier=2, weight=0.85, language="de", format="letter",
            content_tags=["weierstrass", "support", "crelle_journal"],
            notes="Weierstrass intervened on Cantor's behalf at Crelle's Journal.",
        ),
    ]


def _tier3_sources() -> list[Source]:
    """Mathematical opponents (weight 0.70)."""
    return [
        Source(
            title="Kronecker's finitist writings and objections",
            author="Leopold Kronecker",
            date="various",
            tier=3, weight=0.70, language="de", format="paper",
            content_tags=["kronecker", "finitism", "constructivism", "opposition"],
            notes="The opposition that shaped Cantor. 'God made the integers, all the rest is the work of man.'",
        ),
        Source(
            title="Poincaré's criticisms of set theory",
            author="Henri Poincaré",
            date="various",
            tier=3, weight=0.70, language="fr", format="paper",
            content_tags=["poincare", "criticism", "disease_metaphor"],
            notes="Called set theory 'a disease from which mathematics will eventually recover.'",
        ),
        Source(
            title="Brouwer's intuitionist critique",
            author="L.E.J. Brouwer",
            date="various",
            tier=3, weight=0.70, language="de", format="paper",
            content_tags=["brouwer", "intuitionism", "foundations"],
            notes="Later opposition, relevant to ongoing foundations debate.",
        ),
        Source(
            title="Wittgenstein's philosophical objections",
            author="Ludwig Wittgenstein",
            date="various",
            tier=3, weight=0.70, language="de", format="paper",
            content_tags=["wittgenstein", "philosophy", "critique"],
            notes="Philosophical rather than mathematical critique.",
        ),
    ]


def _tier4_sources() -> list[Source]:
    """Catholic theologians (weight 0.65)."""
    return [
        Source(
            title="Gutberlet's 1886 paper on actual infinity and God",
            author="Constantin Gutberlet",
            date="1886",
            tier=4, weight=0.65, language="de", format="paper",
            content_tags=["gutberlet", "actual_infinity", "god", "neo-thomism"],
            notes="First theological paper to appeal to Cantor's transfinites.",
        ),
        Source(
            title="Cardinal Franzelin's 1886 letter to Cantor",
            author="Johann Baptist Franzelin",
            date="1886",
            tier=4, weight=0.65, language="de", format="letter",
            content_tags=["franzelin", "cardinal", "pantheism", "transfinites", "god"],
            notes="Accepted transfinite theory as valid but warned against pantheism.",
        ),
        Source(
            title="Thomas Esser's correspondence with Cantor",
            author="Thomas Esser, O.P.",
            date="various",
            tier=4, weight=0.65, language="de", format="letter",
            content_tags=["esser", "dominicans", "theology", "infinite"],
            notes="Led a group of Dominicans studying theological implications.",
        ),
        Source(
            title="Ignatius Jeiler correspondence",
            author="Ignatius Jeiler, O.F.M.",
            date="various",
            tier=4, weight=0.65, language="de", format="letter",
            content_tags=["jeiler", "franciscans", "theology"],
            notes="Published in Bendiek (1965).",
        ),
        Source(
            title="Aeterni Patris",
            author="Pope Leo XIII",
            date="1879",
            tier=4, weight=0.65, language="la", format="paper",
            content_tags=["pope", "neo-thomism", "encyclical", "context"],
            notes="Context: the neo-Thomist revival creating the intellectual environment for Cantor's theological engagement.",
        ),
    ]


def _tier5_sources() -> list[Source]:
    """Serious historical scholarship, post-1970 (weight 0.55)."""
    return [
        Source(
            title="Georg Cantor: His Mathematics and Philosophy of the Infinite",
            author="Joseph Dauben",
            date="1979",
            tier=5, weight=0.55, language="en", format="book",
            content_tags=["biography", "mathematics", "philosophy", "theology", "standard"],
            notes="THE standard biography. Princeton University Press. 1979/1990.",
        ),
        Source(
            title="Georg Cantor and Pope Leo XIII: Mathematics, Theology, and the Infinite",
            author="Joseph Dauben",
            date="1977",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["theology", "pope", "infinite", "dauben"],
            notes="Journal of the History of Ideas 38(1), 1977, 85-108.",
        ),
        Source(
            title="Labyrinth of Thought: A History of Set Theory and Its Role in Modern Mathematics",
            author="José Ferreirós",
            date="1999",
            tier=5, weight=0.55, language="en", format="book",
            content_tags=["set_theory", "history", "context"],
            notes="Birkhäuser 1999/2007. Broader context but excellent on Cantor.",
        ),
        Source(
            title="On the relations between Georg Cantor and Richard Dedekind",
            author="José Ferreirós",
            date="1993",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["dedekind", "plagiarism_question", "relations"],
            notes="The paper accusing Cantor of plagiarism. ScienceDirect.",
        ),
        Source(
            title="Cantorian Set Theory and the Limitation of Size",
            author="Michael Hallett",
            date="1984",
            tier=5, weight=0.55, language="en", format="book",
            content_tags=["set_theory", "foundations", "limitation_of_size"],
            notes="Oxford: Clarendon. Deep analysis of mathematical and philosophical foundations.",
        ),
        Source(
            title="Probleme des Unendlichen: Werk und Leben Georg Cantors",
            author="Herbert Meschkowski",
            date="1967",
            tier=5, weight=0.55, language="de", format="book",
            content_tags=["biography", "infinity", "life_and_work"],
            notes="First serious modern study of Cantor's life and work.",
        ),
        Source(
            title="Towards a Biography of Georg Cantor",
            author="Ivor Grattan-Guinness",
            date="1971",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["biography", "bell_debunking", "manuscript_discovery"],
            notes="Debunked Bell's myths. Discovered previously unknown Cantor manuscript. Annals of Science.",
        ),
        Source(
            title="The Rediscovery of the Cantor-Dedekind Correspondence",
            author="Ivor Grattan-Guinness",
            date="1974",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["dedekind", "correspondence", "rediscovery"],
            notes="Jahresbericht der DMV 76, 1974/75, 104-139.",
        ),
        Source(
            title="Kardinalität und Kardinäle",
            author="Christian Tapp",
            date="2005",
            tier=5, weight=0.55, language="de", format="book",
            content_tags=["theology", "correspondence", "cardinals", "theologians"],
            notes="Detailed study of the Cantor-theologian correspondence. Franz Steiner Verlag.",
        ),
        Source(
            title="The negative theology of absolute infinity: Cantor, mathematics, and humility",
            author="Gutschmidt & Ged",
            date="2024",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["absolutum", "negative_theology", "recent"],
            notes="International Journal for Philosophy of Religion, 2024.",
        ),
        Source(
            title="Theological Reasoning of Cantor's Set Theory",
            author="(arxiv authors)",
            date="2024",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["theology", "set_theory", "interdisciplinary"],
            url="https://arxiv.org/abs/2407.18972",
            notes="arxiv:2407.18972. Recent interdisciplinary analysis.",
        ),
        Source(
            title="Was Cantor Surprised?",
            author="Fernando Gouvêa",
            date="2011",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["je_le_vois", "historical_analysis", "surprise"],
            notes="American Mathematical Monthly, March 2011. Analysis of 'Je le vois, mais je ne le crois pas'.",
        ),
        Source(
            title="The Man Who Stole Infinity (Quanta Magazine)",
            author="Demian Goos et al.",
            date="2026-02",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["goos", "newly_discovered", "letters", "breaking_news"],
            url="https://www.quantamagazine.org/",
            notes="Breaking coverage of the Goos discovery. Feb 25, 2026.",
        ),
        Source(
            title="Cantor, God, and Inconsistent Multiplicities",
            author="Aaron Thomas-Bolduc",
            date="2014",
            tier=5, weight=0.55, language="en", format="article",
            content_tags=["god", "inconsistent_multiplicities", "proper_classes", "absolutum"],
            notes="Analysis of Cantor's treatment of proper classes and the Absolute.",
        ),
    ]


def _tier6_sources() -> list[Source]:
    """Secondary mathematical exposition (weight 0.35)."""
    return [
        Source(
            title="Contributions to the Founding of the Theory of Transfinite Numbers (Jourdain translation)",
            author="Georg Cantor (trans. P. Jourdain)",
            date="1915",
            tier=6, weight=0.35, language="en", format="book",
            content_tags=["translation", "beitrage", "historical_introduction"],
            notes="English translation with 82-page historical introduction. Dover reprint. Use newer 2024 jamesrmeyer.com translation for accuracy.",
        ),
        Source(
            title="Textbook treatments of Cantor's diagonal argument",
            author="various",
            date="various",
            tier=6, weight=0.35, language="en", format="other",
            content_tags=["diagonal_argument", "textbook", "exposition"],
            notes="Standard math content. Captures results but not thinking process.",
        ),
        Source(
            title="Naïve Set Theory",
            author="Paul Halmos",
            date="1960",
            tier=6, weight=0.35, language="en", format="book",
            content_tags=["set_theory", "textbook", "exposition"],
            notes="Clean modern exposition of set theory basics.",
        ),
        Source(
            title="MacTutor biography of Georg Cantor",
            author="MacTutor History of Mathematics",
            date="various",
            tier=6, weight=0.35, language="en", format="web",
            content_tags=["biography", "chronology", "summary"],
            url="https://mathshistory.st-andrews.ac.uk/Biographies/Cantor/",
            notes="Solid summary, useful for chronology.",
        ),
    ]


def _tier7_sources() -> list[Source]:
    """Popular accounts (weight 0.15) — negative examples."""
    return [
        Source(
            title="'Cantor went mad because of infinity' pop narratives",
            author="various",
            date="various",
            tier=7, weight=0.15, language="en", format="other",
            content_tags=["pop_narrative", "madness_myth", "negative_example"],
            notes="Low weight. Include only to teach the model to reject these framings.",
        ),
        Source(
            title="Wikipedia article on Georg Cantor",
            author="Wikipedia",
            date="various",
            tier=7, weight=0.15, language="en", format="web",
            content_tags=["wikipedia", "mixed_quality"],
            url="https://en.wikipedia.org/wiki/Georg_Cantor",
            notes="Assigned 0.35 in seed doc but tier 7. Mix of sourced and unsourced claims.",
            acquisition_status="available",
        ),
    ]


def _tier8_sources() -> list[Source]:
    """E.T. Bell — EXCLUDED (weight 0.0)."""
    return [
        Source(
            title="Men of Mathematics",
            author="E.T. Bell",
            date="1937",
            tier=8, weight=0.0, language="en", format="book",
            content_tags=["bell", "fabricated", "oedipal", "false_jewish_heritage",
                          "romantic_madness", "EXCLUDE"],
            acquisition_status="excluded",
            notes="Actively harmful. Fabricated Oedipal narrative, false Jewish heritage claims, Romantic madness myth. Grattan-Guinness (1971) showed none of Bell's claims were true. EXCLUDE ENTIRELY or use only as explicit counter-examples.",
        ),
    ]


def get_all_seed_sources() -> list[Source]:
    sources: list[Source] = []
    sources.extend(_tier1_sources())
    sources.extend(_tier2_sources())
    sources.extend(_tier3_sources())
    sources.extend(_tier4_sources())
    sources.extend(_tier5_sources())
    sources.extend(_tier6_sources())
    sources.extend(_tier7_sources())
    sources.extend(_tier8_sources())
    return sources


def seed_database(db_path: Path | None = None) -> int:
    """Initialize the database and populate with all seed sources. Returns count inserted."""
    path = init_db(db_path)
    sources = get_all_seed_sources()
    count = add_sources_bulk(sources, db_path=path)
    return count
