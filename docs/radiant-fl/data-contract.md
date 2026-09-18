# SuperFedMMD proof-of-concept data and federation contract

> **Path note:** This file is retained under the historical `docs/radiant-fl/` path for compatibility. The current contract is no longer RADIANT-specific.

This document defines the common interface for the current two-client SuperFedMMD proof of concept on Gefion.

The purpose of the contract is to make local client workloads interchangeable while ensuring that the NVIDIA FLARE workflow does not require the client training datasets to be combined.

## 1. Contract principles

Every participating client must agree on:

- contract version;
- client/site identity;
- workload/model version;
- input and label semantics;
- preprocessing rules;
- local data-path semantics;
- local training entry point;
- Slurm submission interface;
- trainable/federated parameter schema;
- outbound payload allow-list;
- aggregate evaluation metrics; and
- software/configuration versions.

A client must refuse execution if it cannot satisfy the active contract.

## 2. Logical client identity

The current proof of concept uses at least two logical clients.

Example:

```text
client_a
client_b
```

Each client must have:

```text
client_id
FLARE client identity/configuration
client-local data path
workload/model revision
runtime/environment identifier
```

The clients represent independent sites at the **workflow level**, but they are hosted within the same shared Gefion environment for the hackathon demonstration.

## 3. Client-local data paths

Each client must be configured with its own training-data location.

Conceptually:

```text
client_a -> /path/to/client_a/data
client_b -> /path/to/client_b/data
```

The client workflow must not require a shared training-data directory containing both sites' training records.

A client configuration should expose only the path required for that client's workload.

> This is logical data separation for the proof of concept. It is not a claim that a privileged Gefion user is technically prevented from accessing both directories.

## 4. Dataset partition contract

The demonstration dataset and source are documented in the top-level README.

The federation contract requires that:

- client A and client B use distinct training partitions;
- partition generation is reproducible;
- the partition definition is versioned or hashed;
- record overlap between client training partitions is checked where record identity is available; and
- the active partition identifiers are recorded with the run.

Recommended metadata:

```text
dataset_version
partition_version
client_id
record_count
partition_hash
```

## 5. Descriptive data checks

Before federation, record workload-relevant descriptive statistics for each client.

Examples include:

- number of records;
- positive/negative label counts where applicable;
- image/category counts where applicable;
- modality availability;
- missingness; and
- class or category imbalance.

The exact statistics depend on the active Multimodal Healthcare workload and must not be assumed when they are not present in the selected dataset/component.

## 6. Modality/input contract

The current workload is sourced from the [Multimodal Healthcare](https://github.com/multimodal-healthcare) project.

The exact model-facing schema must be frozen for the active demonstration.

At minimum, the run configuration must define:

```text
active modalities
input field/tensor names
input shapes/dtypes
label field and coding
missing-value representation
preprocessing version
feature ordering where applicable
```

**Exact active schema:** `[TO CONFIRM FROM FINAL FUSION WORKLOAD]`

The infrastructure contract remains model-agnostic beyond requiring that all participating clients expose compatible inputs to the same workload revision.

## 7. Local preprocessing contract

Preprocessing is executed locally for each client.

Required metadata:

```text
contract_version
dataset_version
partition_version
preprocessing_version
model/workload_version
software/runtime_version
config_hash
```

A client must fail closed if its local data do not conform to the active contract.

## 8. Local training contract

Each client must provide a reproducible training entry point that can be launched through Slurm.

The launcher must define:

```text
client_id
data_path
model/workload_version
training configuration
Slurm resource request
output directory
```

The local training process must not require access to the other client's training-data directory.

## 9. Slurm contract

For every client-local training execution, capture:

```text
client_id
Slurm job ID
partition
allocated node
requested CPU
requested GPU
requested memory
wall-time
runtime/environment
exit status
output/model artifact path
```

The exact Gefion Slurm flags and output locations are recorded after successful testing.

## 10. Model/update contract

The NVIDIA FLARE workflow must define the exact model object or update schema exchanged between server and clients.

The contract must specify:

- model/configuration version;
- federated parameter names;
- tensor shapes/dtypes;
- full parameters vs. deltas/updates;
- aggregation weight semantics;
- local epochs/steps;
- optimiser behaviour where relevant; and
- global-state version/hash.

**Exact federated update schema:** `[TO CONFIRM]`

## 11. Allowed outbound payload

A logical client may transmit only approved:

- model parameters / updates / deltas;
- aggregation weights where required;
- global/local model identifiers or hashes;
- federation-round identifier;
- sample count where required for aggregation;
- aggregate loss;
- approved aggregate evaluation metrics; and
- technical federation/Slurm status metadata.

No raw training record is part of the default federation payload.

## 12. Prohibited outbound payload

The following must not leave the client workload through the federation interface unless explicitly added to a later reviewed contract:

- raw training examples;
- raw MRI or other imaging source files;
- raw genomic/sequencing source data;
- record-level clinical source data;
- direct identifiers;
- client-local source identifiers;
- arbitrary files;
- unrestricted embeddings;
- unapproved intermediate activations; and
- record-level predictions/metrics.

The outbound interface is deny-by-default.

## 13. Federation-round contract

Recommended round metadata:

```text
round_id
global_model_version_in
global_model_hash_in
contract_version
participating_client_ids
client Slurm job IDs
aggregation_method
client weighting method
global_model_version_out
global_model_hash_out
metrics_schema_version
timestamp
status
```

## 14. Aggregation contract

The active configuration must define:

- aggregation algorithm;
- client weighting;
- minimum participating clients;
- handling of missing/failed clients;
- handling of incomplete updates;
- convergence/stop criterion; and
- model-state versioning.

For the current demonstration:

```text
minimum participating clients = 2
aggregation algorithm = [TO CONFIRM]
```

## 15. Model artifact contract

Each completed local training job should produce a traceable model artifact or update.

Record:

```text
client_id
Slurm job ID
artifact path
artifact filename
artifact hash
model/workload version
federation round
```

**Gefion artifact/output location:** `[TO CONFIRM]`

## 16. Validation contract

The infrastructure demonstration should report technical validation separately from predictive-model performance.

Technical checks include:

- both clients connected;
- both clients received the intended global state/job;
- both clients used distinct configured data paths;
- Slurm jobs completed;
- model/update artifacts were found;
- approved updates returned;
- aggregation completed; and
- updated global state was redistributed.

Any predictive metrics included in the demo must use the definitions provided by the active workload rather than legacy RADIANT-specific metrics.

## 17. Versioning

Recommended contract identifier:

```text
superfedmmd-poc-contract-v0.2
```

Increment the contract version for changes to:

- dataset partition semantics;
- input/label schema;
- preprocessing;
- workload/model architecture;
- federated parameter schema;
- outbound allow-list;
- Slurm execution interface; or
- metrics schema.

## 18. Client conformance gate

Before a client may participate:

```text
contract_version matches
dataset/partition version accepted
model/workload version matches
input schema valid
config hash accepted
client-local data path configured
Slurm launcher configured
outbound allow-list active
```

If any check fails, the client should refuse the round rather than silently modifying the contract.

## 19. Security boundary

The current proof of concept demonstrates **logical separation**, not security isolation against privileged users of Gefion.

Because the server and clients operate within a shared HPC environment, a sufficiently privileged user may have access beyond the boundaries visible to the application-level client workflow.

A production deployment would additionally require:

- institutional identity and access management;
- least-privilege filesystem permissions;
- authenticated and authorised client/server communication;
- network isolation where appropriate;
- hardened credential/key management;
- audit and operational monitoring;
- governance and institutional agreements; and
- formal security/privacy assessment.

## 20. Proof-of-concept boundary

This contract is intentionally scoped to the hackathon demonstration.

The current claim is limited to showing that two logically separated clients can train on distinct local datasets, execute their local workloads through Slurm and participate in a common NVIDIA FLARE federation without combining their training datasets in the workflow.
