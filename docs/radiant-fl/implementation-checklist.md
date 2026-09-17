# RADIANT-FL implementation checklist

This checklist turns the existing SuperFedMMD architecture and development flow into an executable proof-of-concept plan for the RADIANT multimodal federated-learning use case.

**Prototype deadline:** Friday 18 September 2026, 17:00 CEST

## 1. Scope freeze

- [ ] Confirm primary task: progression-free survival / progression-risk modelling.
- [ ] Confirm initial modalities:
  - [ ] clinical variables
  - [ ] MRI-derived radiomic features
  - [ ] transcriptomics / RNA-seq
- [ ] Keep WGS-derived features optional for the first end-to-end milestone.
- [ ] Confirm discovery cohort is used for development/training.
- [ ] Confirm replication cohort is held out from federated training.
- [ ] Freeze the common data/model contract in `data-contract.md`.

## 2. Data inventory and harmonisation

- [ ] Build a subject-level manifest with one row per patient.
- [ ] Record modality availability for each subject.
- [ ] Record outcome and censoring status.
- [ ] Verify that subject identifiers are consistent across modalities.
- [ ] Define a deterministic modality-presence mask.
- [ ] Define missing-value handling for each modality.
- [ ] Define normalisation / transformation rules once and apply the same contract at every site.
- [ ] Record feature version, source file and transformation version.

### Minimum manifest fields

```text
subject_id
cohort_role
site_id
has_clinical
has_radiomics
has_rnaseq
has_wgs
outcome_time
outcome_event
```

## 3. Create virtual secluded environments

- [ ] Partition discovery subjects into at least three mutually exclusive sites.
- [ ] Verify that no subject appears at more than one site.
- [ ] Preserve the replication cohort outside the federation.
- [ ] Prefer deliberately non-IID site distributions where feasible.
- [ ] Document site-level subject count, event rate, age distribution, tumour-location distribution, modality availability, and relevant molecular/subtype distribution.

## 4. Centralised reference pipeline

- [ ] Implement the same model architecture intended for federation.
- [ ] Train on pooled discovery data.
- [ ] Save configuration, random seed, software/container version, model hash, and evaluation metrics.
- [ ] Use this only as a reference baseline, not as the federated execution path.

## 5. Local reference models

For each virtual site:

- [ ] Train a local-only model.
- [ ] Evaluate on that site's validation partition.
- [ ] Record the same metrics used for the centralised and federated models.
- [ ] Keep local patient-level data and intermediate files inside the site boundary.

## 6. NVIDIA FLARE federation skeleton

- [ ] Configure Gefion-side federation coordinator.
- [ ] Configure one FLARE client per secluded environment.
- [ ] Establish site identity / authentication.
- [ ] Distribute the initial global model.
- [ ] Verify clients can receive an approved training job.
- [ ] Verify clients return only approved model updates and metrics.
- [ ] Log every federation round.

### Round-level audit record

```text
round_id
global_model_hash_in
site_ids_participating
client_config_hashes
aggregation_method
global_model_hash_out
metrics_returned
timestamp
status
```

## 7. First end-to-end federated round

- [ ] Global model N is distributed.
- [ ] Local training runs independently at each participating site.
- [ ] Local validation completes.
- [ ] Policy filter validates outbound payload.
- [ ] Site updates reach Gefion.
- [ ] Gefion aggregates the updates.
- [ ] Global model N+1 is created.
- [ ] Global model N+1 is redistributed.
- [ ] Model/config hashes are recorded.

**Milestone:** one complete `global -> local -> aggregate -> global` cycle without patient-level data leaving a site.

## 8. Multimodal / missing-modality behaviour

- [ ] Support subjects with incomplete modality sets.
- [ ] Pass an explicit modality-presence mask to the fusion layer.
- [ ] Ensure a site can participate even when it lacks one or more modalities.
- [ ] Define which model components each site is permitted to update.
- [ ] Verify aggregation does not require every site to update every modality-specific component.

## 9. Federation behaviour

- [ ] Start with a documented aggregation strategy such as FedAvg or FedProx.
- [ ] Record client weighting strategy.
- [ ] Test one deliberately heterogeneous / non-IID split.
- [ ] Test client dropout or one missing client round if time permits.
- [ ] Verify restart/reconnect behaviour if time permits.

## 10. Privacy boundary checks

- [ ] No raw MRI crosses the boundary.
- [ ] No raw RNA-seq crosses the boundary.
- [ ] No raw WGS crosses the boundary.
- [ ] No patient-level clinical record crosses the boundary.
- [ ] No direct identifiers cross the boundary.
- [ ] No unrestricted embeddings or arbitrary local files are returned.
- [ ] Outbound payload matches the allow-list in `data-contract.md`.

Secure aggregation / differential privacy can be added later; they are not prerequisites for proving the first execution path unless explicitly required by the team.

## 11. Evaluation

Compare:

1. local-only models
2. centralised reference model
3. federated global model

- [ ] Evaluate on the held-out replication cohort.
- [ ] Report C-index.
- [ ] Report Brier score where implemented.
- [ ] Report calibration where implemented.
- [ ] Report site-level validation performance.
- [ ] Report convergence across federation rounds.
- [ ] Report the centralised-to-federated performance delta.

## 12. Reproducibility package

Before the final presentation:

- [ ] Pin code commit SHA.
- [ ] Pin container / environment version.
- [ ] Save training configuration.
- [ ] Save site-partition definition.
- [ ] Save data-contract version.
- [ ] Save global model hash.
- [ ] Save federation-round logs.
- [ ] Update GitHub README with final status and results.
- [ ] Verify all commands required for the demo are documented.

## 13. Friday definition of done

The PoC is complete when the team can demonstrate:

```text
RADIANT discovery data
        ->
subject-disjoint secluded environments
        ->
local multimodal training
        ->
approved FLARE model update
        ->
Gefion aggregation
        ->
new global model
        ->
redistribution
        ->
held-out evaluation
```

with no raw patient-level data exchanged between secluded environments.

The first milestone demonstrates technical feasibility and reproducibility; it is not a clinical validation claim.
