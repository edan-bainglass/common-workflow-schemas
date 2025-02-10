from __future__ import annotations

import typing as t

import pydantic as pdt

from .utils import MetadataField


class EngineModel(pdt.BaseModel):
    code: t.Annotated[
        str,
        MetadataField(
            description=(
                "An identifier (PK, UUID or full label) of a configured `Code`."
            ),
            iri="https://example.com/schemas/engine/code",
        ),
    ]
    options: t.Annotated[
        dict[str, t.Any],
        MetadataField(
            description="A dictionary of metadata options for the engine.",
            iri="https://example.com/schemas/engine/options",
        ),
    ]
