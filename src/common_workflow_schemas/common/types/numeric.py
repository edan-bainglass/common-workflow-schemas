import typing as t

import numpy as np
import numpy.typing as npt
import pydantic as pdt

FloatArray = t.Annotated[
    npt.NDArray[np.float64],
    pdt.WithJsonSchema(
        {
            "type": "array",
            "items": {"type": "number"},
        }
    ),
]
