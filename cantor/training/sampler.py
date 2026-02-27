"""Weighted tier sampling for training data construction."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

from cantor.db.schema import DB_PATH, get_connection

_TIER_WEIGHTS: dict[int, float] = {
    1: 1.00,
    2: 0.85,
    3: 0.70,
    4: 0.65,
    5: 0.55,
    6: 0.35,
    7: 0.15,
    8: 0.00,
}


class WeightedSampler:
    """Builds a training pool from segments with tier-based weighting.

    Tier 1 (Cantor's own words) is oversampled by ``oversample_tier1``.
    Tiers 2-6 are included proportionally to their weight.
    Tier 7 is kept only as negative examples.
    Tier 8 (E.T. Bell) is excluded entirely.
    """

    def __init__(
        self,
        oversample_tier1: float = 3.0,
        db_path: Path | None = None,
    ) -> None:
        self.oversample_tier1 = oversample_tier1
        self.db_path = db_path or DB_PATH

    def get_weighted_segments(self) -> list[dict]:
        """Fetch all segments joined with their source tier/weight and annotations."""
        conn = get_connection(self.db_path)
        rows = conn.execute(
            """
            SELECT
                seg.id          AS segment_id,
                seg.content     AS content,
                src.title       AS source_title,
                src.tier        AS tier,
                src.weight      AS weight,
                seg.segment_type AS segment_type,
                seg.language    AS language,
                seg.sender      AS sender,
                seg.recipient   AS recipient
            FROM segments seg
            JOIN sources src ON seg.source_id = src.id
            ORDER BY src.tier, seg.id
            """
        ).fetchall()

        segment_ids = [r["segment_id"] for r in rows]
        annotations_by_seg: dict[int, list[dict]] = {}

        if segment_ids:
            placeholders = ",".join("?" for _ in segment_ids)
            ann_rows = conn.execute(
                f"""
                SELECT
                    id, segment_id, dimension, subtags,
                    math_topics, psych_state, confidence,
                    contradiction_flag, notes
                FROM annotations
                WHERE segment_id IN ({placeholders})
                ORDER BY segment_id
                """,
                segment_ids,
            ).fetchall()
            for ar in ann_rows:
                ann = dict(ar)
                for json_field in ("subtags", "math_topics"):
                    raw = ann.get(json_field)
                    if raw and isinstance(raw, str):
                        try:
                            ann[json_field] = json.loads(raw)
                        except (json.JSONDecodeError, TypeError):
                            pass
                annotations_by_seg.setdefault(ann["segment_id"], []).append(ann)

        conn.close()

        segments: list[dict] = []
        for row in rows:
            seg = dict(row)
            seg["annotations"] = annotations_by_seg.get(seg["segment_id"], [])
            segments.append(seg)

        return segments

    def build_training_pool(self) -> list[dict]:
        """Apply tier weights to build the final training pool.

        - Tier 1: duplicated ``oversample_tier1`` times (rounded up).
        - Tiers 2-6: each segment included ``ceil(weight * oversample_tier1)``
          times so higher tiers appear proportionally more often.
        - Tier 7: included once, marked ``negative_example=True``.
        - Tier 8: excluded.
        """
        segments = self.get_weighted_segments()
        pool: list[dict] = []

        for seg in segments:
            tier = seg["tier"]

            if tier == 8:
                continue

            if tier == 7:
                entry = {**seg, "negative_example": True}
                pool.append(entry)
                continue

            if tier == 1:
                copies = math.ceil(self.oversample_tier1)
            else:
                copies = max(1, math.ceil(seg["weight"] * self.oversample_tier1))

            for _ in range(copies):
                pool.append({**seg, "negative_example": False})

        return pool

    def split_train_val(
        self,
        val_ratio: float = 0.1,
        seed: int = 42,
    ) -> tuple[list[dict], list[dict]]:
        """Split the training pool into train/validation sets, stratified by tier."""
        pool = self.build_training_pool()

        by_tier: dict[int, list[dict]] = {}
        for seg in pool:
            by_tier.setdefault(seg["tier"], []).append(seg)

        rng = random.Random(seed)
        train: list[dict] = []
        val: list[dict] = []

        for tier in sorted(by_tier):
            items = by_tier[tier]
            rng.shuffle(items)
            n_val = max(1, round(len(items) * val_ratio))
            val.extend(items[:n_val])
            train.extend(items[n_val:])

        rng.shuffle(train)
        rng.shuffle(val)
        return train, val
