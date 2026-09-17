# Methods

## Infrastructure and federated execution

### Study objective

Team 6 developed a proof-of-concept infrastructure for federated execution of multimodal biomedical models using the Gefion high-performance computing environment. The work focused on the architecture, orchestration and reproducibility required to execute an externally supplied model across multiple isolated or secluded data environments. Development of the predictive model itself was treated as a separate workstream.

The principal systems objective was to establish whether a common, version-controlled model job could be distributed to multiple local execution environments, executed against site-local multimodal data, and coordinated through a federated workflow without transferring raw patient-level source data between environments.

### System design

The infrastructure was designed as a separation between a **federation/control plane** and multiple **local execution planes**.

The federation/control plane is coordinated through Gefion and is responsible for federated job orchestration, participant configuration, model-state coordination, aggregation and execution provenance. Local execution planes represent isolated institutional environments. Each local environment contains its own biomedical source data, a local data/execution adapter, the externally supplied model component and a NVIDIA FLARE client.

The interface between these planes is intentionally narrow. Raw source data remain within the local environment, while only explicitly permitted model objects, updates and aggregate technical or evaluation metrics may cross the federation boundary.

### Federation framework

NVIDIA FLARE was selected as the federation framework for the proof of concept. The architecture uses the server/client abstraction to separate central federation orchestration from site-local execution. Each participating environment is represented by a FLARE client, while the server-side federation workflow is coordinated through the Gefion execution environment.

The model itself is not embedded in the infrastructure design. Instead, local training or inference code is treated as a pluggable execution component called from the local federated client workflow.

The exact NVIDIA FLARE version and Gefion runtime configuration are recorded for the final reproducible experiment.

**NVIDIA FLARE version:** `[TO CONFIRM]`  
**Gefion project / execution environment:** `[TO CONFIRM]`  
**Scheduler configuration:** `[TO CONFIRM]`  
**Runtime / container environment:** `[TO CONFIRM]`

### Local execution abstraction

Each participating environment implements a common local execution pathway:

1. access site-local biomedical data;
2. map local representations to the agreed federation/data contract;
3. invoke the supplied model implementation;
4. calculate approved local outputs;
5. validate the outbound payload against the federation allow-list; and
6. return the approved model state, update and/or aggregate metrics to the federation.

This separation enables different multimodal model implementations to use the same federation infrastructure, provided they implement the agreed execution and update interfaces.

### Reference multimodal use case

The RADIANT paediatric low-grade glioma resource was selected as the initial multimodal reference use case. It provides clinical, imaging-derived and molecular information and is therefore suitable for exercising multimodal data interfaces and heterogeneous site configurations.

For infrastructure testing, subjects from the development cohort can be assigned to mutually exclusive virtual sites representing separate institutions. Patient-level source data remain local to their assigned environment. The original replication cohort can remain outside federated training for downstream model evaluation.

RADIANT is used to validate the systems architecture rather than to define the infrastructure around one specific predictive model.

### Data harmonisation and federation contract

A versioned federation contract defines the interface shared by all participating environments. The contract specifies cohort and subject semantics, modality schemas, preprocessing and harmonisation behaviour, missing-modality representation, model/configuration compatibility, permitted outbound model objects and metrics, and provenance metadata.

Local sites may differ in data distribution or modality availability. Harmonisation therefore aims to provide a common model-facing interface without requiring raw source datasets to be centralised.

The contract is validated before execution. An incompatible site should fail the compatibility check rather than silently modifying its interpretation of the shared schema.

### Federation boundary

Patient-level biomedical source data are retained within the originating execution environment.

The following classes of information are outside the default federation payload:

- raw medical imaging;
- raw sequencing data;
- patient-level clinical records;
- direct patient identifiers;
- local source-system identifiers;
- arbitrary local files;
- unapproved intermediate representations.

Outbound communication is deny-by-default. Only the model objects, updates, aggregate metrics and technical metadata explicitly required by the active federation configuration are permitted to cross the boundary.

### Federated execution workflow

A federated run begins from version-controlled source code and configuration. A NVIDIA FLARE job is prepared together with the federation contract and participant configuration. The server and client environments are then provisioned and connected.

The federation server distributes the active job and global model state to participating clients. Each client performs the local execution procedure using only local data and returns the approved outbound payload. Server-side logic combines the returned model information according to the aggregation configuration and produces the next global model state.

The updated state can then be redistributed for another federation round. Configuration, participant status, model-state identifiers, hashes and execution metadata are recorded throughout the run.

The aggregation algorithm and predictive-model optimisation strategy belong to the model/federation configuration and are not fixed by the infrastructure itself.

**Aggregation strategy:** `[TO CONFIRM BY MODEL WORKSTREAM]`  
**Number of federation rounds:** `[TO CONFIRM]`  
**Minimum participating clients:** `[TO CONFIRM]`

### Gefion execution

Gefion provides the target high-performance computing environment for the federation/control-plane components and related execution workload.

The final implementation record will include:

```text
Gefion project / account
scheduler configuration
requested compute resources
wall-time
software environment
NVIDIA FLARE version
runtime / container identifier
Git commit SHA
job configuration
participant configuration
```

At the time of writing, the Gefion-specific execution pathway is under active implementation. Methods text will be updated from future/target wording to completed-experiment wording only after the corresponding execution step has been verified.

### Reproducibility and provenance

All project source code, configurations and documentation are maintained under version control.

For each reproducible federation run, the infrastructure is designed to record at least:

```text
Git commit SHA
federation contract version
NVIDIA FLARE version
runtime / environment identifier
job configuration
participant/client identities
model/configuration identifier
federation round
input global-state identifier/hash
output global-state identifier/hash
timestamps
execution status
```

This enables the infrastructure execution to be reconstructed independently of later source-code changes.

### Technical evaluation

Infrastructure evaluation is separated from predictive-model evaluation.

The primary technical endpoint is successful demonstration of the complete execution path:

```text
versioned job
    ->
Gefion / federation coordinator
    ->
multiple isolated clients
    ->
site-local model execution
    ->
approved outbound update
    ->
server-side aggregation
    ->
new global state
    ->
redistribution
```

Additional systems-level observations include successful client participation, deterministic configuration, auditability, recovery or reconnect behaviour where tested, and confirmation that raw patient-level source data do not traverse the federation boundary.

Model accuracy and disease-specific predictive performance are evaluated separately by the model-development workstream.

### Scope and limitations

The hackathon implementation is a technical proof of concept. It is intended to demonstrate architecture and execution feasibility rather than production security, clinical validation or institutional deployment readiness.

Production use would require additional governance, information-security assessment, institutional agreements, identity and key-management procedures, operational monitoring, privacy-risk assessment and application-specific validation.
