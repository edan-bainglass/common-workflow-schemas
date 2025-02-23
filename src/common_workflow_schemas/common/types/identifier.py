import typing as t
import uuid

import pydantic as pdt

from common_workflow_schemas.common.field import MetadataField

UUIDHex = t.Annotated[
    str,
    pdt.AfterValidator(lambda s: uuid.UUID(s, version=4)),
]


class UniqueIdentifier(pdt.BaseModel):
    identifier: t.Annotated[
        UUIDHex | pdt.UUID4,
        MetadataField(
            default=None,
            description="Unique UUID identifier",
            iri="https://example.com/schemas/uuid",
        ),
    ]
