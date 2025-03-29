import datetime
import enum
import typing as t

import pydantic as pdt


def serialize_model(model: pdt.BaseModel) -> dict:
    """Serialize fields of a Pydantic model to a dictionary."""

    def serialize_field(obj: t.Any) -> t.Any:
        if isinstance(obj, dict):
            return {k: serialize_field(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [serialize_field(v) for v in obj]
        elif isinstance(obj, enum.Enum):
            return obj.value
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return obj

    return {k: serialize_field(v) for k, v in model.model_dump().items()}


StructureSerializer = pdt.PlainSerializer(
    serialize_model,
    return_type=dict,
    when_used="always",
)
