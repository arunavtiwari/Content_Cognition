# Tribe V2 + Open fMRI Data Training Plan

This plan defines how to strengthen Content Cognition's idea-ranking model using:
1. **Your proprietary Meta Tribe V2 features** (primary signal source), and
2. **Open naturalistic fMRI datasets** where participants consume rich content (movies, narratives, clips).

## 1) Training objective

Train an outcome-conditioned ranker that predicts which content idea structures are most likely to optimize:
- virality
- conversion
- retention
- brand fit
- novelty

## 2) Data sources

### A) Primary proprietary source
- `tribe_v2_events` (required): frame-level or segment-level cognitive response features for content playback.
- `tribe_v2_outcomes` (required): engagement/conversion labels tied to content outcomes.

### B) Open datasets to strengthen representation learning

The following datasets are relevant because they involve people **watching/listening to naturalistic content**:

1. **StudyForrest** (movie + audio movie fMRI, eyegaze, physiology)
   - https://studyforrest.org/
   - https://studyforrest.org/data.html

2. **The Grand Budapest Hotel fMRI dataset (OpenNeuro ds003017)**
   - https://openneuro.org/datasets/ds003017

3. **Naturalistic movie watching + narrated recall (OpenNeuro ds004042)**
   - https://openneuro.org/datasets/ds004042

4. **Naturalistic movie-watching dataset (OpenNeuro ds001132)**
   - https://openneuro.org/datasets/ds001132

5. **Algonauts / CNeuroMod movie stimuli brain data**
   - https://algonautsproject.com/braindata.html
   - https://algonautsproject.com/2025/challenge.html

6. **Natural Scenes Dataset (NSD)** (large-scale natural image viewing fMRI)
   - https://naturalscenesdataset.org/

## 3) Harmonization strategy

Create a shared feature table with these canonical columns:
- `stimulus_id`
- `stimulus_modality` (video/audio/image/text)
- `time_idx`
- `attention_proxy`
- `emotion_proxy`
- `novelty_proxy`
- `memory_boundary_proxy`
- `arousal_proxy`
- `label_virality`, `label_conversion`, `label_retention`

Map each open dataset into proxies that align with Tribe V2 semantics.

## 4) Two-stage training

### Stage A — Representation pretraining (open data)
- Learn robust temporal embeddings from naturalistic neural response dynamics.
- Target: next-segment prediction / contrastive alignment across modalities.

### Stage B — Outcome fine-tuning (Tribe V2)
- Fine-tune model heads on proprietary business outcomes.
- Keep a frozen/shared trunk plus trainable outcome heads.

## 5) Evaluation

- In-domain: Tribe V2 holdout by campaign and creator.
- Out-of-domain: evaluate on unseen verticals and platforms.
- Metrics: NDCG@K, calibration error, lift over baseline heuristic ranker.

## 6) Safety and governance

- Keep open datasets for representation learning only unless licenses allow direct supervised commercialization.
- Maintain lineage metadata for each sample.
- Store dataset-level license in registry before use.
