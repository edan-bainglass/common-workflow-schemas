from __future__ import annotations

import typing as t

import pydantic as pdt

from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.types import UniqueIdentifier


class Code(pdt.BaseModel):
    identifier: t.Annotated[
        UniqueIdentifier | None,
        MetadataField(
            description="The unique identifier of the code.",
            iri="https://example.com/schemas/uniqueIdentifier",
        ),
    ]
    executed_by: t.Annotated[
        Executor,
        MetadataField(
            description="The executor of the code.",
            iri="https://example.com/schemas/simulation/engine/code/executedBy",
        ),
    ]
    executed_on: t.Annotated[
        ExecutionEnvironment,
        MetadataField(
            description="The execution environment of the code.",
            iri="https://example.com/schemas/simulation/engine/code/executedOn",
        ),
    ]
    executable_path: t.Annotated[
        str,
        MetadataField(
            description="The path to the executable code.",
            iri="https://example.com/schemas/simulation/engine/code/executablePath",
        ),
    ]


class Executor(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the executor.",
            iri="https://example.com/schemas/simulation/engine/executor/name",
        ),
    ]
    version: t.Annotated[
        str,
        MetadataField(
            description="The version of the executor.",
            iri="https://example.com/schemas/simulation/engine/executor/version",
        ),
    ]
    availability: t.Annotated[
        Availability,
        MetadataField(
            description="The availability of the executor.",
            iri="https://example.com/schemas/simulation/engine/executor/availability",
        ),
    ]


class ExecutionEnvironment(pdt.BaseModel):
    hostname: t.Annotated[
        str,
        MetadataField(
            description="The hostname of the execution environment.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/hostname",
        ),
    ]
    architecture: t.Annotated[
        str,
        MetadataField(
            description="The architecture of the execution environment.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/architecture",
        ),
    ]
    os: t.Annotated[
        OperatingSystem,
        MetadataField(
            description="The operating system of the execution environment.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/os",
        ),
    ]


class OperatingSystem(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the operating system.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/os/name",
        ),
    ]
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the operating system.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/os/metadata",
        ),
    ]


class Availability(pdt.BaseModel):
    package_manager: t.Annotated[
        PackageManager,
        MetadataField(
            description="The package manager used to install the executor.",
            iri="https://example.com/schemas/simulation/engine/executor/availability/packageManager",
        ),
    ]
    package: t.Annotated[
        str,
        MetadataField(
            description="The package name of the executor.",
            iri="https://example.com/schemas/simulation/engine/executor/availability/package",
        ),
    ]


class PackageManager(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the package manager.",
            iri="https://example.com/schemas/simulation/engine/executor/availability/packageManager/name",
        ),
    ]
    version: t.Annotated[
        str,
        MetadataField(
            description="The version of the package manager.",
            iri="https://example.com/schemas/simulation/engine/executor/availability/packageManager/version",
        ),
    ]
