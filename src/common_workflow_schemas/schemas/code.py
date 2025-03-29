import typing as t

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import SemanticModel
from common_workflow_schemas.common.types import UniqueIdentifier


class PackageManager(SemanticModel):
    _IRI = f"{BASE_PREFIX}/PackageManager"

    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the package manager.",
            iri=f"{_IRI}/Name",
        ),
    ]
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the package manager.",
            iri=f"{_IRI}/Metadata",
        ),
    ]


class Package(SemanticModel):
    _IRI = f"{BASE_PREFIX}/Package"

    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the package.",
            iri=f"{_IRI}/Name",
        ),
    ]
    package_manager: t.Annotated[
        PackageManager,
        MetadataField(
            description="The package manager from which to obtain the package.",
            iri=f"{_IRI}/PackageManager",
        ),
    ]
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the package.",
            iri=f"{_IRI}/Metadata",
        ),
    ]


class ExecutionEnvironment(SemanticModel):
    _IRI: str = f"{BASE_PREFIX}/ExecutionEnvironment"

    name: t.Annotated[
        t.Optional[str],
        MetadataField(
            description="The name of the execution environment.",
            iri=f"{_IRI}/Name",
        ),
    ] = None
    metadata: t.Annotated[
        dict,
        MetadataField(
            description="The metadata of the execution environment.",
            iri=f"{_IRI}/Metadata",
        ),
    ]


class Code(SemanticModel):
    _IRI: str = f"{BASE_PREFIX}/Code"

    identifier: t.Annotated[
        t.Optional[UniqueIdentifier],
        MetadataField(
            description="The unique identifier of the code.",
            iri=f"{BASE_PREFIX}/UniqueIdentifier",
        ),
    ] = None
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the code.",
            iri=f"{_IRI}/Name",
        ),
    ]
    package: t.Annotated[
        Package,
        MetadataField(
            description="The code package.",
            iri=f"{_IRI}/Package",
        ),
    ]
    executionEnvironment: t.Annotated[
        ExecutionEnvironment,
        MetadataField(
            description="The execution environment of the code.",
            iri=f"{_IRI}/ExecutionEnvironment",
        ),
    ]
