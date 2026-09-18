# Methods

## Infrastructure and federated execution

### Study objective

The SuperFedMMD team is developing a proof-of-concept infrastructure for federated execution of multimodal biomedical models using the Gefion high-performance computing environment.

The principal systems objective is to demonstrate that **two logically independent data sites can participate in a federated learning workflow coordinated on Gefion without combining their training datasets**, using NVIDIA FLARE as the federation layer.

The predictive model is treated as a pluggable workload. The infrastructure work focuses on federation, orchestration, Slurm-backed execution, data separation, model/update exchange, aggregation and reproducibility.

### Proof-of-concept scope

The current Gefion implementation uses **logically separated client workloads within a shared computing environment**.

For the hackathon proof of concept:

- at least two NVIDIA FLARE clients represent independent participating sites;
- each client is configured with its own client-specific training-data directory;
- a client should not be configured with access to a shared training-data directory;
- NVIDIA FLARE coordinates the federated workflow;
- local model training is submitted to Slurm for execution on allocated compute resources;
- only approved model objects, updates and aggregate metrics are returned through the federation.

This setup demonstrates federated orchestration and logical separation of client datasets. It does **not** reproduce the administrative, network or security isolation of independently operated hospitals, biobanks or institutional enclaves.

### System design

The architecture separates a **federation/control plane** from **client-local execution workloads**.

For the current proof of concept, the NVIDIA FLARE server/coordinator and client control processes are intended to run within the Gefion access environment, while compute-intensive local training is submitted through Slurm.

> **Implementation status:** The exact placement and lifetime of FLARE server/client processes, including whether they may remain on Gefion login nodes, must follow Gefion operating policy and is recorded only after successful testing.

Each logical client has:

1. an NVIDIA FLARE client identity/configuration;
2. a client-specific local data path;
3. the supplied multimodal model workload;
4. a local launcher or execution adapter; and
5. a Slurm submission path for compute-intensive training.

The federation server coordinates job/state distribution and aggregation. Slurm is responsible for assigning suitable compute nodes to local training jobs.

### Federation framework

NVIDIA FLARE is used as the federation layer for the proof of concept. Its server/client abstraction separates federation coordination from client-local execution.

The infrastructure is designed around the following exchange:

```text
global model / state
        ->
FLARE clients
        ->
client-local Slurm training jobs
        ->
approved model update + aggregate metrics
        ->
FLARE server / aggregation
        ->
updated global model / state
        ->
redistribution
```

Raw training data are not intended to be transferred through the NVIDIA FLARE federation.

The exact NVIDIA FLARE version and communication configuration are recorded for the final reproducible experiment.

**NVIDIA FLARE version:** `[TO CONFIRM]`  
**Gefion project / execution environment:** `[TO CONFIRM]`  
**FLARE server/client communication configuration:** `[TO CONFIRM]`  
**Scheduler configuration:** `[TO CONFIRM]`  
**Runtime / container environment:** `[TO CONFIRM]`

### Local execution abstraction

Each participating client implements a common local execution pathway:

1. access only its configured client-local training data;
2. validate the active data/model contract;
3. invoke the supplied multimodal model workload;
4. submit compute-intensive training through Slurm;
5. persist approved model artifacts and logs to the configured job/output location;
6. validate the outbound payload; and
7. return only the approved model state/update and aggregate metrics to the federation.

The exact location in which completed Slurm jobs persist trained model artifacts is recorded as part of the implementation.

**Slurm model-output location:** `[TO CONFIRM]`

### Reference multimodal workload

The current reference workload is based on components from the [Multimodal Healthcare](https://github.com/multimodal-healthcare) project.

The repository contains modality-specific and fusion components that can be used to exercise the SuperFedMMD infrastructure without making the federation dependent on one particular model architecture.

The demonstration dataset is described separately in the top-level README. This Methods document therefore treats the dataset and fusion model as an **external workload supplied to the federation infrastructure**, rather than repeating the dataset description here.

For the final demonstration, the active modalities, label definition, preprocessing configuration and exact fusion-model revision must be recorded with the run.

### Dataset inspection

Before federated execution, the demonstration data should be inspected with reproducible analysis code.

The current demonstration plan includes descriptive statistics such as:

- number of records per client;
- positive/negative label counts where applicable;
- image/category distributions where applicable;
- modality availability;
- missingness or other workload-relevant summary statistics.

These summaries are used to document the logical client partitions and verify that each client operates on its intended local subset.

### Data and federation contract

A versioned contract defines the interface shared by all participating clients.

The contract specifies:

- client/site identity;
- client-local data-path semantics;
- workload/model version;
- modality and input schema;
- label/outcome semantics;
- preprocessing behaviour;
- Slurm execution interface;
- permitted outbound model objects;
- permitted aggregate metrics;
- artifact and provenance metadata; and
- federation-round identifiers.

A client must fail rather than silently reinterpret an incompatible contract.

### Federation boundary

The federation is deny-by-default with respect to client training data.

The following classes of information are outside the default federation payload:

- raw imaging;
- raw sequencing/genomic source data;
- patient-level or record-level clinical source data;
- direct identifiers;
- local source-system identifiers;
- arbitrary local files;
- client-local training examples;
- unrestricted embeddings or intermediate activations.

Only model objects, updates, aggregate metrics and technical metadata explicitly required by the active federation configuration may cross the federation boundary.

### Federated execution workflow

A federated run begins from version-controlled source code and configuration.

The intended proof-of-concept execution sequence is:

1. prepare two client-specific data directories;
2. start or connect the NVIDIA FLARE server/coordinator;
3. start or connect two logically independent NVIDIA FLARE clients;
4. distribute the active model/job or global state;
5. submit each client's local training workload through Slurm;
6. collect the approved model update and aggregate metrics from each client;
7. aggregate the returned updates through the federation workflow;
8. produce the next global model/state; and
9. redistribute the updated state.

The aggregation algorithm belongs to the model/federation configuration and is not fixed by the infrastructure itself.

**Aggregation strategy:** `[TO CONFIRM]`  
**Number of federation rounds:** `[TO CONFIRM]`  
**Minimum participating clients:** `2` for the current demonstration

### Gefion and Slurm execution

Gefion provides the shared HPC environment used for the hackathon proof of concept.

Slurm is used to request compute resources for training workloads rather than running compute-intensive training directly on the login environment.

The final implementation record should include:

```text
Gefion project / account
Slurm partition
Slurm job ID
requested CPU / GPU / memory
wall-time
compute node
software environment
NVIDIA FLARE version
runtime / container identifier
Git commit SHA
job configuration
client configuration
client-local data path identifier
model artifact/output path
```

### Reproducibility and provenance

All project source code, configurations and documentation are maintained under version control.

For each reproducible federation run, record at least:

```text
Git commit SHA
federation-contract version
NVIDIA FLARE version
runtime / environment identifier
FLARE communication configuration
job configuration
participating client IDs
client-local dataset/partition identifiers
model/configuration identifier
Slurm job IDs
allocated compute nodes
federation round
input global-state identifier/hash
output global-state identifier/hash
model artifact/output paths
timestamps
execution status
```

### Technical evaluation

Infrastructure evaluation is separated from predictive-model evaluation.

The primary technical endpoint is successful demonstration of:

```text
versioned workload
    ->
Gefion / NVIDIA FLARE coordination
    ->
two logically separated clients
    ->
distinct client-local training data
    ->
Slurm-backed local model training
    ->
approved model/update exchange
    ->
aggregation
    ->
updated global state
    ->
redistribution
```

A successful systems proof of concept should additionally show that the client configuration does not require a shared training-data folder and that raw client training examples are not part of the federation payload.

Model accuracy is secondary to demonstrating that the federated execution path works end to end.

### Scope and limitations

The hackathon implementation is a technical proof of concept.

The participating federation sites are **logically separated workloads within a shared Gefion computing environment**. They are not equivalent to independently administered institutional environments or security-isolated enclaves.

The experiment can therefore demonstrate:

- federated orchestration;
- logical separation of client-specific training datasets;
- local model execution through Slurm;
- model/update exchange;
- aggregation;
- redistribution; and
- reproducible execution metadata.

It does **not** by itself demonstrate protection against a privileged user with access to the underlying shared Gefion environment.

A production deployment across independent institutions would additionally require appropriate network isolation, identity and access management, credential/key management, governance, institutional agreements, information-security assessment, operational monitoring, privacy-risk assessment and application-specific validation.
