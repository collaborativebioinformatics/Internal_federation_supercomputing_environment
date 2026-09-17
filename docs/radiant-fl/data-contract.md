# RADIANT-FL data and federation contract

This document defines the common interface that every SuperFedMMD secluded environment must implement for the RADIANT proof of concept.

The purpose of the contract is to make local implementations interchangeable while ensuring that raw patient-level data remain under the control of the originating environment.

## 1. Contract principles

Every site must agree on:

- subject identity semantics
- cohort role
- modality schemas
- outcome definition
- preprocessing rules
- missing-modality representation
- train/validation semantics
- model architecture version
- trainable parameter allow-list
- outbound payload allow-list
- evaluation metrics
- software/configuration versions

A site may hold a different subset of modalities, but it must implement the same contract version.

## 2. Subject identity

- `subject_id` is unique within the project.
- The same subject must never be assigned to more than one federated site.
- Direct identifiers must not be used as `subject_id`.
- The replication cohort must never be assigned to a training site.
- Site-local source identifiers may be retained locally but must not be transmitted.

| Field | Type | Description |
|---|---|---|
| `subject_id` | string | Project-scoped pseudonymous identifier |
| `cohort_role` | enum | `discovery` or `replication` |
| `site_id` | string | Virtual or real participating site |
| `split` | enum | `train`, `validation`, or `test` |

## 3. Modality availability

Each subject has an explicit modality-presence record.

| Field | Type |
|---|---|
| `has_clinical` | boolean |
| `has_radiomics` | boolean |
| `has_rnaseq` | boolean |
| `has_wgs` | boolean |

The model must not infer missingness from arbitrary sentinel values. Missing modalities are represented explicitly through a modality-presence mask.

## 4. Clinical feature contract

Initial clinical variables should follow the variables used in the RADIANT clinicoradiomic work where available, including:

- sex
- age at diagnosis
- tumour location
- NF1 status
- extent of tumour resection
- chemotherapy status
- radiation-treatment status

Each variable must have a canonical field name, data type, allowed values/coding, missing-value policy, unit where applicable, and transformation/normalisation rule.

## 5. Radiomics feature contract

For the initial PoC, use the published processed MRI-derived radiomic feature representation rather than requiring raw-image preprocessing at every site.

Each site must agree on:

- exact feature list and order
- feature-generation version/source
- normalisation rule
- handling of missing radiomic features
- whether normalisation parameters are fixed from a reference set or estimated locally

Raw MRI data remain local and are outside the first PoC federation payload.

## 6. Transcriptomics / RNA-seq contract

Each site must use the same transcriptomic representation.

The contract must define:

- reference gene identifiers
- exact gene ordering
- count / TPM / transformed representation
- filtering rule
- normalisation / transformation rule
- missing-value policy
- feature-selection rule if dimensionality reduction is used

If dimensionality reduction is used, its parameters and version must be frozen and reproducible.

## 7. Optional WGS-derived feature contract

WGS-derived features are optional for the first milestone.

If enabled, the contract must define a derived feature representation rather than transferring raw genomic files.

The following must remain local:

- FASTQ
- BAM / CRAM
- patient-level VCF unless explicitly transformed into an approved derived representation
- sample-level variant metadata not present on the federation allow-list

## 8. Outcome contract

Primary task:

**progression-free survival / progression risk**

| Field | Type | Description |
|---|---|---|
| `outcome_time` | numeric | Time-to-event using one agreed unit |
| `outcome_event` | boolean | Event/progression indicator |

All sites must use the same time origin, time unit, event definition, censoring definition, and handling of invalid or missing outcome values.

## 9. Local preprocessing contract

Every site executes preprocessing locally.

Required metadata:

```text
contract_version
preprocessing_version
feature_schema_version
software_version
container_hash
config_hash
```

A site must fail closed if its local data do not conform to the active contract.

## 10. Model-input contract

The local trainer receives a structure logically equivalent to:

```text
subject_id
clinical_tensor        optional
radiomics_tensor       optional
rnaseq_tensor          optional
wgs_tensor             optional
modality_mask
outcome_time
outcome_event
```

`subject_id` is used for local bookkeeping only and must not be included in model updates.

## 11. Model architecture contract

Conceptually:

```text
clinical      -> clinical encoder ------\
radiomics     -> radiomics encoder ------\
RNA-seq       -> transcriptomic encoder ---> fusion -> survival/risk head
WGS optional  -> genomic encoder --------/
modality mask --------------------------/
```

The contract must define architecture version, trainable components, frozen components, parameter names, tensor shapes, optimiser configuration, local epochs/steps, and learning-rate policy.

## 12. Trainable-parameter allow-list

Example policy:

```text
ALLOW:
- modality adapters
- fusion layer
- task head

OPTIONAL:
- selected encoder layers

DENY BY DEFAULT:
- arbitrary tensors
- cached activations
- embeddings not explicitly approved
- local optimiser state unless explicitly required
```

The exact allow-list must be versioned.

## 13. Allowed outbound payload

A secluded environment may transmit only approved:

- model parameter updates / deltas
- aggregation weights
- model/configuration hashes
- federation round identifier
- sample count
- aggregate loss
- validation metrics
- technical federation health/status

No record-level metric export is permitted.

## 14. Prohibited outbound payload

The following must not leave the secluded environment:

- raw MRI
- raw RNA-seq
- raw WGS
- direct identifiers
- patient-level clinical records
- subject-level prediction tables unless explicitly approved for a later experiment
- arbitrary files
- unrestricted embeddings
- unapproved intermediate activations
- local source-system identifiers

The outbound interface should be deny-by-default.

## 15. Federation-round contract

```text
round_id
global_model_version_in
global_model_hash_in
contract_version
participating_site_ids
aggregation_method
site_weighting_method
global_model_version_out
global_model_hash_out
metrics_schema_version
timestamp
status
```

## 16. Aggregation contract

The first PoC may use a documented standard method such as FedAvg or FedProx.

The active configuration must define:

- aggregation algorithm
- client weighting
- minimum participating clients
- handling of missing clients
- handling of modality-specific parameter updates
- convergence / stop criterion

## 17. Validation contract

Suggested initial metrics:

- C-index
- Brier score
- calibration metric / calibration plot where implemented
- local validation loss
- site-level sample count

The final held-out replication evaluation must use the same outcome definition and feature contract as training.

## 18. Versioning

Recommended contract identifier:

```text
radiant-fl-contract-v0.1
```

Increment the contract version for changes to feature names/order, outcome definition, preprocessing, missing-modality semantics, model architecture, trainable-parameter allow-list, outbound allow-list, or metrics schema.

## 19. Site conformance gate

Before a site may participate in a federation round:

```text
contract_version matches
feature_schema_version matches
model_version matches
config hash accepted
local data schema valid
outbound allow-list active
```

If any check fails, the client should refuse the round rather than attempting an implicit conversion.

## 20. PoC boundary

This contract is intentionally scoped to the hackathon proof of concept.

A production biomedical federation would additionally require formal governance, information-security review, institutional agreements, privacy-risk assessment, hardened identity/key management, operational monitoring and clinically appropriate model validation.
