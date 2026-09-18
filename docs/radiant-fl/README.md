# SuperFedMMD federated workflow proof of concept

> **Path note:** This document is retained under the historical `docs/radiant-fl/` path to avoid breaking existing repository links. The active proof of concept is no longer RADIANT-specific.

## Objective

Demonstrate that **two logically independent data sites can participate in a federated learning workflow coordinated on Gefion without combining their training datasets**, using NVIDIA FLARE as the federation layer.

The current proof of concept uses client-specific data partitions and a multimodal model workload derived from the [Multimodal Healthcare](https://github.com/multimodal-healthcare) project.

The demonstration dataset itself is described in the top-level README and is not repeated here.

## Current proof-of-concept topology

The hackathon implementation represents independent sites as **logically separated NVIDIA FLARE clients inside a shared Gefion environment**.

Each client should:

- have its own FLARE identity/configuration;
- use its own client-specific training-data directory;
- not be configured with access to a shared training-data folder;
- submit compute-intensive local training through Slurm; and
- return only approved model updates/parameters and aggregate metrics.

The NVIDIA FLARE server/coordinator manages federation state and aggregation.

```text
Gefion access environment
    |
    +-- NVIDIA FLARE server / coordinator
    |
    +-- Client A control process
    |      |
    |      +-- client A data only
    |      +-- Slurm training job
    |
    +-- Client B control process
           |
           +-- client B data only
           +-- Slurm training job

Slurm
    |
    +-- allocates compute resources for client-local training
```

## Reference workload

The current model workload is based on components from:

- https://github.com/multimodal-healthcare

The infrastructure treats the model as a pluggable workload. The exact fusion-model revision, active modalities, labels and preprocessing configuration used in the final demo must be recorded with the run.

## Dataset inspection

Before federated execution, the client partitions should be characterised with reproducible analysis code.

Useful descriptive checks include:

- record count per client;
- positive/negative label counts where applicable;
- image/category distributions where applicable;
- modality availability;
- missingness; and
- verification that client A and client B use distinct local data partitions.

## Definition of done

A successful proof of concept demonstrates the complete path:

```text
global model/state
    ->
two FLARE clients
    ->
client-local Slurm training
    ->
approved update/metrics
    ->
FLARE aggregation
    ->
updated global state
    ->
redistribution
```

with:

- at least **2 logically independent clients**;
- distinct client-local training datasets;
- no shared training-data directory required by the client configuration;
- NVIDIA FLARE coordinating the federation;
- local compute submitted through Slurm;
- model/update exchange and aggregation demonstrated;
- no raw training records transferred through the federation;
- reproducible configuration and logs; and
- final model/output artifacts located and documented.

## Security interpretation

The current Gefion demonstration provides **logical workload and data separation**, not independent institutional security boundaries.

A privileged user of the shared Gefion environment may have permissions that would not exist across separately administered hospitals or biobanks. The proof of concept therefore must not be presented as demonstrating protection against a privileged user of the underlying shared environment.

A production deployment would additionally require:

- institution-specific identity and access management;
- network/security isolation;
- hardened credentials and key management;
- least-privilege filesystem permissions;
- governance and institutional agreements;
- security and privacy assessment; and
- operational monitoring.

## Documentation

- [Reference architecture](architecture.md)
- [Development flowchart](development-flowchart.md)
- [Data and federation contract](data-contract.md)
- [Infrastructure Methods](../methods.md)

## Legacy material

The directory name and some retained image assets originate from the earlier RADIANT-oriented design phase. They are kept as project provenance but should not be interpreted as the active demonstration workload.
