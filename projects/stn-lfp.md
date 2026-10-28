# STN-LFP medication-state decoding

Master's thesis in Biomedical Engineering, Universidad Pública de Navarra.

Classify medication OFF/ON states from subthalamic local field potentials in Parkinson's disease, using spectral and temporal signal representations.

## Method

- 28 participants and 64 recording segments
- Participant-held-out evaluation, keeping each person's segments together
- Learned transformations fitted within the corresponding training partition
- Spectral means compared with distributional and temporal representations
- Nested selection among 12 candidates
- Temporal-order and duration controls to test what the representation captures

Implementation: Python, NumPy, SciPy and scikit-learn. Analysis covers preprocessing, feature extraction, classification, evaluation and reproducible reporting.

## Aggregate results

The metric is mean balanced accuracy across participants. Bootstrap intervals resample participants over held-out predictions.

| Procedure | Mean balanced accuracy | 95% bootstrap interval |
| --- | ---: | ---: |
| Spectral means, fixed parameters | 0.750 | 0.661–0.839 |
| Nested selection, 12 candidates | 0.848 | 0.759–0.929 |

## Interpretation

The nested selection rule was defined after exploring this cohort, so these results remain exploratory. They have no external-cohort validation. Preprocessing uses bidirectional filtering; the evaluation is offline.

This page shares methodology and aggregate results only. Clinical recordings and participant-level outputs are not distributed.
