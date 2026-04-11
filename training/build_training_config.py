#!/usr/bin/env python3
"""Create a training config that combines Tribe V2 and open fMRI registry sources."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "open_fmri_registry.json"
OUT = ROOT / "training_config.generated.json"


def main() -> None:
    registry = json.loads(REGISTRY.read_text())

    config = {
        "pipeline": "tribe_v2_outcome_ranker_v1",
        "representation_pretraining": {
            "enabled": True,
            "datasets": [d["name"] for d in registry["datasets"]],
            "objective": "temporal_contrastive",
        },
        "finetuning": {
            "enabled": True,
            "source": "tribe_v2",
            "targets": [
                "virality",
                "conversion",
                "retention",
                "brand_fit",
                "novelty",
            ],
        },
        "evaluation": {
            "metrics": ["ndcg_at_10", "calibration_error", "lift_vs_baseline"],
            "splits": ["creator_holdout", "campaign_holdout", "vertical_holdout"],
        },
    }

    OUT.write_text(json.dumps(config, indent=2))
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    main()
