import typing as t

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import SemanticModel

from .code import Code


class Engine(SemanticModel):
    _IRI = f"{BASE_PREFIX}/Engine"

    code: t.Annotated[
        Code,
        MetadataField(
            description="A code that can execute the engine workflow.",
        ),
    ]
    options: t.Annotated[
        dict[str, t.Any],
        MetadataField(
            description="A dictionary of metadata options for the engine, such as computational resources, parallelization, etc. These usually depend on the job scheduler of the machine on which the code is executed.",
            iri=f"{_IRI}/Options",
        ),
    ]
