import typing as t
import uuid

import pydantic as pdt

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField

UUIDHex = t.Annotated[
    str,
    pdt.AfterValidator(lambda s: uuid.UUID(s, version=4)),
    pdt.PlainSerializer(lambda uuid_: str(uuid_)),
]

UniqueIdentifier = t.Annotated[
    t.Union[UUIDHex, pdt.UUID4],
    MetadataField(
        description="Unique UUID identifier",
        iri=f"{BASE_PREFIX}/UUID",
        default=None,
    ),
]
