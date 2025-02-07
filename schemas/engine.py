from __future__ import annotations

import typing as t

import pydantic as pdt


class EngineModel(pdt.BaseModel):
    code: t.Annotated[
        str,
        pdt.Field(
            description=(
                "An identifier (PK, UUID or full label) of a configured `Code`."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/engine/code",
            },
        ),
    ]
    options: t.Annotated[
        dict[str, t.Any],
        pdt.Field(
            description="A dictionary of metadata options for the engine.",
            json_schema_extra={
                "iri": "https://example.com/schemas/engine/options",
            },
        ),
    ]
