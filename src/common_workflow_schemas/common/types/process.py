import typing as t

import pydantic as pdt

from common_workflow_schemas.utils.metadata import MetadataField

PK = t.Annotated[
    int,
    MetadataField(
        default=None,
        description="Unique database primary key identifier",
        iri="https://example.com/schemas/pk",
    ),
]

UUID = t.Annotated[
    pdt.UUID4,
    MetadataField(
        default=None,
        description="Unique UUID identifier",
        iri="https://example.com/schemas/uuid",
    ),
]
