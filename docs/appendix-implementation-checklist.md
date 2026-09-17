# Appendix A — Infrastructure implementation checklist

This checklist is the operational companion to the SuperFedMMD README and Methods documentation.

It intentionally focuses on **federated architecture, Gefion execution, NVIDIA FLARE integration, reproducibility and documentation**. Model development is handled by the relevant model workstream.

## A. Repository and reproducibility

- [ ] Main branch contains the current architecture and documentation.
- [ ] Gefion execution scripts are version controlled.
- [ ] NVIDIA FLARE configuration is version controlled.
- [ ] Tested commands are documented exactly as executed.
- [ ] Git commit SHA is recorded for every demonstrable run.
- [ ] Runtime/container/environment identifier is recorded.
- [ ] Configuration files are separated from secrets/credentials.

## B. Gefion environment

- [ ] Gefion project/account access verified.
- [ ] Required software/modules available.
- [ ] NVIDIA FLARE version recorded.
- [ ] Python/runtime environment recorded.
- [ ] Scheduler submission path tested.
- [ ] Required CPU/GPU/memory resources documented.
- [ ] Logs persist after job completion.
- [ ] A minimal non-federated test job executes successfully.

## C. Federation/control plane

- [ ] NVIDIA FLARE server/coordinator can start successfully.
- [ ] Server identity/configuration is provisioned.
- [ ] Federation endpoint is reachable from intended clients.
- [ ] Job submission pathway is documented.
- [ ] Server-side aggregation step executes.
- [ ] Global model/state can be redistributed.
- [ ] Federation round metadata is logged.

## D. Client / secluded environments

For each participating or simulated environment:

- [ ] Client identity/configuration is provisioned.
- [ ] Client can connect to the federation.
- [ ] Local data remain within the environment.
- [ ] Local execution adapter is available.
- [ ] Supplied model/job can be invoked locally.
- [ ] Approved outputs can be returned.
- [ ] Disallowed patient-level/raw data are not part of the outbound payload.
- [ ] Client disconnect/reconnect behaviour is recorded where tested.

## E. Federation and data contract

- [ ] Contract version is defined.
- [ ] Local schema compatibility is checked before execution.
- [ ] Modality availability is represented explicitly.
- [ ] Permitted model/update objects are defined.
- [ ] Permitted metrics are defined.
- [ ] Prohibited outbound data are documented.
- [ ] Incompatible clients fail rather than silently reinterpret the schema.

## F. End-to-end infrastructure run

- [ ] Versioned job is created.
- [ ] Job is submitted through the federation.
- [ ] At least two independent/secluded clients participate.
- [ ] Global model/state reaches each participating client.
- [ ] Local execution completes.
- [ ] Approved updates return to the server.
- [ ] Server-side aggregation completes.
- [ ] New global state is generated.
- [ ] New global state can be redistributed.
- [ ] Entire round is represented in logs/provenance.

## G. Provenance record

For a final reproducible demonstration, record:

- [ ] Git commit SHA
- [ ] NVIDIA FLARE version
- [ ] Gefion environment / project
- [ ] scheduler/job identifier
- [ ] runtime/container identifier
- [ ] federation-contract version
- [ ] job/configuration identifier
- [ ] participating clients
- [ ] federation-round number
- [ ] input global-state identifier/hash
- [ ] output global-state identifier/hash
- [ ] execution timestamps
- [ ] final status

## H. Documentation

- [ ] README begins with user value / intended use.
- [ ] Quick Start contains only tested commands or clearly marked placeholders.
- [ ] High-level architecture matches the implementation.
- [ ] Methods distinguish target architecture from verified implementation.
- [ ] Original concept diagrams are retained as provenance.
- [ ] Known limitations are documented.
- [ ] Final demo pathway can be reproduced from the repository.

## I. Hackathon demonstration readiness

- [ ] One clean end-to-end execution path is demonstrated.
- [ ] Architecture can be explained in under two minutes.
- [ ] Data boundary can be explained clearly.
- [ ] Repository contains final commands/configuration used for the demo.
- [ ] README reflects what was actually implemented.
- [ ] Screenshots/log extracts/results needed for presentation are saved.
- [ ] No claim of production security or clinical validation is made without evidence.

## Infrastructure definition of done

The infrastructure milestone is met when the team can demonstrate:

```text
versioned job
    ->
Gefion / NVIDIA FLARE coordination
    ->
multiple secluded clients
    ->
site-local execution
    ->
approved outbound update
    ->
aggregation
    ->
updated global state
    ->
redistribution
    ->
auditable, reproducible run
```

without transferring raw patient-level source data between secluded environments.
