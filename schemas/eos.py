from __future__ import annotations

import typing as t

import pydantic as pdt
from aiida import orm

from .composite import CompositeInputsModel, CompositeOutputsModel
from .relax import CommonRelaxInputsModel


class EosCommonRelaxInputsModel(CommonRelaxInputsModel):
    relax_type: t.Annotated[
        t.Literal[
            "none",
            "positions",
            "shape",
            "positions_shape",
        ],
        pdt.Field(
            description=(
                "The type of relaxation to perform, limited to fixed-volume "
                "relaxations."
            ),
        ),
    ]


class EosInputsModel(CompositeInputsModel[EosCommonRelaxInputsModel]):
    structure: t.Annotated[
        orm.StructureData,
        pdt.Field(description="The input structure"),
    ]
    scale_factors: t.Annotated[
        list[pdt.PositiveFloat] | None,
        pdt.Field(
            description=(
                "The scale factors at which the volume and total energy of the "
                "structure should be computed. This input is optional since the scale "
                "factors can be also set via the `scale_count` and `scale_increment` "
                "inputs."
            )
        ),
    ]
    # TODO does this (and increment) need to be AiiDA types?
    scale_count: t.Annotated[
        pdt.PositiveInt | None,
        pdt.Field(
            description=(
                "The number of scale factors at which the volume and total energy of "
                "the structure should be computed, used in conjunction with "
                "`scale_increment`. This input is optional since the scale factors can "
                "be also set via the `scale_factors` input."
            )
        ),
    ]
    scale_increment: t.Annotated[
        pdt.PositiveFloat | None,
        pdt.Field(
            description=(
                "The increment between the scale factors at which the volume and "
                "total energy of the structure should be computed, used in conjunction "
                "with `scale_count`. This input is optional since the scale factors "
                "can be also set via the `scale_factors` input."
            )
        ),
    ]

    @pdt.model_validator(mode="before")
    def _validate_scale_factors_inputs(self, data: dict):
        if not self.scale_factors and not (self.scale_count and self.scale_increment):
            raise ValueError(
                "Either `scale_factors` or both `scale_count` and `scale_increment` "
                "should be specified."
            )
        return self

    @pdt.field_validator("scale_factors")
    def _validate_scale_factors(self, scale_factors):
        if scale_factors is None:
            return scale_factors
        if not all(isinstance(factor, float | int) for factor in scale_factors):
            raise ValueError(
                "`scale_factors` should be an AiiDA `List` of integers or floats"
            )
        if any(factor <= 0 for factor in scale_factors):
            raise ValueError("Scale factors must be positive")
        return scale_factors


class EosOutputsModel(CompositeOutputsModel):
    structures: t.Annotated[
        list[orm.StructureData],
        pdt.Field(description="The list of relaxed structures."),
    ]
