# Common Workflow Schemas

This repository houses Pydantic models for inputs/outputs of common workflows for materials science. The models were adapted from those of the [AiiDA Common Workflows](https://github.com/aiidateam/aiida-common-workflows) (ACWF) project. Models are exportable to OO-LD format using `Model.model_oo_ld()`, where `Model` is any components of the schemas.

An [example notebook](./examples/relax.ipynb) is provided as a showcase of the schemas' interoperability features applied to a common structure geometry optimization (relaxation) workflow using the [AiiDA](https://aiida.net) workflow engine.

This work was developed as part of the [PREMISE](https://ord-premise.org) project, an [ETH Board ORD Program](https://ethrat.ch/en/eth-domain/open-research-data/) Establish Project.
