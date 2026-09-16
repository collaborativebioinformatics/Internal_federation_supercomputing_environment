# RADIANT-FL proof of concept

This directory describes a proof-of-concept for federated multimodal learning on the RADIANT pediatric low-grade glioma dataset, coordinated from the Gefion HPC environment and trained across multiple isolated/secluded environments.

## Objective

Demonstrate that multiple isolated environments can collaboratively train a multimodal progression-risk model without exchanging patient-level data.

The proof of concept uses RADIANT as the reference dataset and treats participating environments as virtual institutions with subject-disjoint, deliberately heterogeneous local cohorts.

### Primary prediction task

- progression-free survival / progression risk

### Initial modalities

- clinical variables
- MRI-derived radiomic features
- transcriptomics / RNA-seq

### Optional later extension

- WGS-derived features

## Experimental design

The original discovery/replication concept is preserved.

- Discovery data are partitioned into multiple virtual sites.
- Patient identities are mutually exclusive between sites.
- Site distributions are intentionally non-IID where practical.
- The replication cohort remains untouched by federated training and is reserved for final evaluation.

Three model settings should be compared:

1. **Local** — each site trains independently.
2. **Centralised** — pooled discovery data provide a reference baseline.
3. **Federated** — the same discovery subjects are distributed across sites and only approved model updates/metrics cross site boundaries.

## Definition of done

**Deadline: Friday 18 September 2026, 17:00 CEST**

A successful prototype demonstrates the complete path:

`global model -> site-local training -> approved update -> aggregation on Gefion -> redistributed global model -> local validation`

with:

- at least 3 simulated secluded environments
- subject-disjoint local cohorts
- multimodal inputs
- no transfer of raw patient-level data between environments
- reproducible configuration
- audit/logging of federation rounds
- independent evaluation on the held-out RADIANT replication cohort
- comparison of local, centralised and federated performance

## Delivery plan

| Time | Deliverable |
|---|---|
| Wednesday evening | Freeze task, modalities, patient manifest, discovery/replication logic and federation contract |
| Thursday morning | Central reference pipeline and baseline |
| Thursday afternoon | Three virtual secluded sites and first federated training loop |
| Thursday evening | End-to-end global -> local -> aggregate -> redistribute round |
| Friday morning | Missing-modality handling, non-IID split and Gefion-compatible execution |
| Friday 12:00–14:00 | Privacy boundary, failure/reconnect behaviour and audit logging |
| Friday 14:00–16:00 | Local vs centralised vs federated benchmark and held-out evaluation |
| Friday 16:00–17:00 | Freeze configuration, hashes, documentation and demonstration |

## Documentation

- [Development flowchart](development-flowchart.md)
- [Reference architecture](architecture.md)

## Primary references

- RADIANT paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11697432/
- Associated analysis repository: https://github.com/d3b-center/pLGG-immune-clinicoradiomics
