# RADIANT-FL reference architecture

## System topology

```mermaid
flowchart TB
    subgraph GEFION["GEFION HPC — federation / control plane"]
        COORD[Federation coordinator]
        AGG[Model aggregation]
        REG[Global model registry]
        AUDIT[Round audit / provenance]
        EVAL[Global evaluation orchestration]

        COORD --> AGG
        AGG --> REG
        REG --> COORD
        COORD --> AUDIT
        REG --> EVAL
    end

    subgraph A["Secluded environment A"]
        AC[FL client]
        AD[Local RADIANT partition]
        AT[Local trainer]
        AM[Local validation]
        AD --> AT
        AC --> AT
        AT --> AM
    end

    subgraph B["Secluded environment B"]
        BC[FL client]
        BD[Local RADIANT partition]
        BT[Local trainer]
        BM[Local validation]
        BD --> BT
        BC --> BT
        BT --> BM
    end

    subgraph C["Secluded environment C"]
        CC[FL client]
        CD[Local RADIANT partition]
        CT[Local trainer]
        CM[Local validation]
        CD --> CT
        CC --> CT
        CT --> CM
    end

    COORD <-->|signed model + approved updates / metrics| AC
    COORD <-->|signed model + approved updates / metrics| BC
    COORD <-->|signed model + approved updates / metrics| CC
```

## Multimodal model concept

The initial model should support different modality availability between institutions and patients.

```mermaid
flowchart LR
    RI[Radiomics] --> RE[Radiomics encoder]
    CL[Clinical variables] --> CE[Clinical encoder]
    RNA[RNA-seq] --> TE[Transcriptomic encoder]
    WGS[Optional WGS features] --> WE[Genomic encoder]

    RE --> F[Fusion layer]
    CE --> F
    TE --> F
    WE --> F

    MASK[Modality-presence mask] --> F
    F --> H[Survival / progression-risk head]
```

A site does not need to contain every modality in order to participate, provided the common model/update contract explicitly defines which components it may train and return.

## Federation contract

Every environment must share the same versioned contract for:

- patient identifier handling
- feature schemas
- outcome definition
- preprocessing rules
- train/validation partition semantics
- missing-modality representation
- model architecture and trainable parameter allow-list
- optimiser and local training configuration
- metrics allowed to leave the site
- parameters allowed to leave the site
- software/container version
- model and configuration hashes

## Privacy and security boundary

Allowed to cross the federation boundary:

- signed global model parameters
- explicitly approved local parameter updates
- approved aggregate/local validation metrics
- technical telemetry required for federation health

Not allowed to cross the boundary:

- raw MRI
- raw RNA-seq
- raw WGS
- patient-level clinical records
- direct identifiers
- unrestricted embeddings or intermediate representations
- arbitrary local files

Secure aggregation and/or additional privacy mechanisms can be enabled as the federation moves beyond the initial systems PoC.

## Virtual-site simulation

For the initial RADIANT PoC, secluded environments are simulated using mutually exclusive subject partitions from the discovery cohort.

The partitions should be intentionally non-IID when feasible, for example by varying:

- patient age distribution
- tumor location distribution
- outcome/progression prevalence
- molecular subtype prevalence
- modality availability

This is preferable to a purely random equal split because it exercises a central challenge of real multi-institution federation: heterogeneous local data distributions.

## Evaluation

The held-out replication cohort is never used for federation training.

Primary comparison:

- Local models
- Centralised reference model
- Federated global model

Suggested metrics:

- concordance index (C-index)
- Brier score
- calibration
- site-level validation performance
- convergence across federation rounds
- centralised-to-federated performance delta

The first milestone demonstrates technical feasibility and reproducibility; it is not a clinical validation claim.
