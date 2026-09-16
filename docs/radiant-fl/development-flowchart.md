# Federated multimodal learning development flow

The diagram below defines the development and execution workflow for the RADIANT-FL proof of concept.

```mermaid
flowchart TD
    A[RADIANT public data] --> B[Verify patient IDs, outcomes and available modalities]
    B --> C[Build harmonised patient manifest]

    C --> C1[Clinical variables]
    C --> C2[MRI-derived radiomic features]
    C --> C3[Transcriptomics / RNA-seq]
    C --> C4[Optional WGS-derived features]

    C --> D{Original cohort role}

    D -->|Replication| R0[Lock replication cohort]
    R0 --> R1[No participation in training]
    R1 --> R2[Final independent evaluation]

    D -->|Discovery| E[Create subject-disjoint virtual institutions]
    E --> F1[Site A]
    E --> F2[Site B]
    E --> F3[Site C]

    F1 --> G1[Local data mapping and preprocessing]
    F2 --> G2[Local data mapping and preprocessing]
    F3 --> G3[Local data mapping and preprocessing]

    G1 --> H1[Local multimodal training]
    G2 --> H2[Local multimodal training]
    G3 --> H3[Local multimodal training]

    H1 --> P1[Policy / privacy filter]
    H2 --> P2[Policy / privacy filter]
    H3 --> P3[Policy / privacy filter]

    P1 --> U[Approved model updates and metrics only]
    P2 --> U
    P3 --> U

    U --> J[Gefion federation coordinator]
    J --> K[Aggregate updates: FedAvg / FedProx]
    K --> L[Global model N+1]

    L --> M1[Redistribute to Site A]
    L --> M2[Redistribute to Site B]
    L --> M3[Redistribute to Site C]

    M1 --> V[Local validation]
    M2 --> V
    M3 --> V

    V --> Q{Converged / quality gate passed?}
    Q -->|No| H1
    Q -->|No| H2
    Q -->|No| H3

    Q -->|Yes| Z[Freeze global candidate model]
    Z --> R2

    R2 --> S[Compare Local vs Centralised vs Federated]
    S --> T[Report C-index, Brier score, calibration and site-level performance]
    T --> END[PoC complete]

    subgraph Boundary["Federation rule"]
        X1[Raw patient-level data never leave the local site]
        X2[Only explicitly approved model parameters and metrics may cross the boundary]
    end
```

## Required comparison

The proof of concept should report three settings:

```mermaid
flowchart LR
    D[Same RADIANT discovery subjects] --> L[LOCAL<br/>Independent model per site]
    D --> C[CENTRALISED<br/>Pooled reference baseline]
    D --> F[FEDERATED<br/>Subject-disjoint sites]

    L --> E[Compare performance]
    C --> E
    F --> E

    E --> R[Held-out RADIANT replication cohort]
```

## Success criterion

The principal systems-level success criterion is:

> The federated model approaches the centralised reference performance while no raw patient-level data are transferred between secluded environments.

The first PoC is intended to prove the architecture and execution model, not to constitute a clinically validated model.
