import typing as t

import pydantic as pdt

from common_workflow_schemas.common.field import MetadataField

from .code import Code


class Engine(pdt.BaseModel):
    code: t.Annotated[
        Code,
        MetadataField(
            description="A code that can execute the engine workflow.",
            iri="https://example.com/schemas/simulation/engine/code",
        ),
    ]
    options: t.Annotated[
        dict[str, t.Any],
        MetadataField(
            description=(
                "A dictionary of metadata options for the engine, such as ",
                "computational resources, parallelization, etc. These usually depend ",
                "on the job scheduler of the machine on which the code is executed.",
            ),
            iri="https://example.com/schemas/simulation/engine/options",
        ),
    ]
