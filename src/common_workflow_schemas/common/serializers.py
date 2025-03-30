import datetime
import enum
import typing as t

import numpy as np
import pydantic as pdt


def serialize_field(obj: t.Any) -> t.Any:
    if isinstance(obj, dict):
        return {k: serialize_field(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_field(v) for v in obj]
    elif isinstance(obj, enum.Enum):
        return obj.value
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj


def serialize_model(model: pdt.BaseModel) -> dict:
    """Serialize fields of a Pydantic model to a dictionary."""
    return {k: serialize_field(v) for k, v in model.model_dump().items()}
