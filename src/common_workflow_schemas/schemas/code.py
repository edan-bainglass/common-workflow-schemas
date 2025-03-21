from __future__ import annotations

import typing as t

import pydantic as pdt

from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.types import UniqueIdentifier


class Code(pdt.BaseModel):
    identifier: t.Annotated[
        t.Optional[UniqueIdentifier],
        MetadataField(
            description="The unique identifier of the code.",
            iri="https://example.com/schemas/uniqueIdentifier",
        ),
    ] = None
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the code.",
            iri="https://example.com/schemas/simulation/engine/code/name",
        ),
    ]
    package: t.Annotated[
        Package,
        MetadataField(
            description="The code package.",
            iri="https://example.com/schemas/simulation/engine/code/package",
        ),
    ]
    executed_on: t.Annotated[
        ExecutionEnvironment,
        MetadataField(
            description="The execution environment of the code.",
            iri="https://example.com/schemas/simulation/engine/code/executedOn",
        ),
    ]


class Package(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the package.",
            iri="https://example.com/schemas/simulation/engine/package/name",
        ),
    ]
    package_manager: t.Annotated[
        PackageManager,
        MetadataField(
            description="The package manager from which to obtain the package.",
            iri="https://example.com/schemas/simulation/engine/package/packageManager",
        ),
    ]
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the package.",
            iri="https://example.com/schemas/simulation/engine/package/metadata",
        ),
    ]


class PackageManager(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the package manager.",
            iri="https://example.com/schemas/simulation/engine/package/packageManager/name",
        ),
    ]
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the package manager.",
            iri="https://example.com/schemas/simulation/engine/package/packageManager/metadata",
        ),
    ]


class ExecutionEnvironment(pdt.BaseModel):
    name: t.Annotated[
        t.Optional[str],
        MetadataField(
            description="The name of the execution environment.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/name",
        ),
    ] = None
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the execution environment.",
            iri="https://example.com/schemas/simulation/engine/executionEnvironment/metadata",
        ),
    ]
