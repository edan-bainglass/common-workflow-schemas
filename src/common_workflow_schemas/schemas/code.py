import typing as t

import pydantic as pdt

from common_workflow_schemas.common.field import MetadataField


class Code(pdt.BaseModel):
    name: t.Annotated[
        str,
        MetadataField(
            description="The name of the code.",
            iri="https://example.com/schemas/simulation/engine/code/name",
        ),
    ]
    executable_path: t.Annotated[
        str,
        MetadataField(
            description="The path to the code executable.",
            iri="https://example.com/schemas/simulation/engine/code/executable_path",
        ),
    ]
