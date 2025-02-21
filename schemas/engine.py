import typing as t

import pydantic as pdt

from .utils import MetadataField


class EngineModel(pdt.BaseModel):
    code: t.Annotated[
        str,
        MetadataField(
            description=(
                "An identifier of the code to be used for the engine. This can be a ",
                "unique identifier (PK, UUID, etc.), a label, or an executable path. ",
                "The workflow manager is responsible for resolving this identifier.",
            ),
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
