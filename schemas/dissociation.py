from __future__ import annotations

import typing as t

import pydantic as pdt
from aiida import orm

from .composite import CompositeInputsModel, CompositeOutputsModel
from .relax import CommonRelaxInputsModel
from .utils import WithArbitraryTypes


class DcCommonRelaxInputsModel(CommonRelaxInputsModel):
    relax_type: t.Annotated[
        str,
        pdt.Field(
            "none",
            frozen=True,
            description=(
                "This field is fixed to 'none' denoting a single-point calculation."
            ),
        ),
    ] = "none"


class DcInputModel(
    CompositeInputsModel[DcCommonRelaxInputsModel],
    WithArbitraryTypes,
):
    molecule: t.Annotated[
        orm.StructureData,
        pdt.Field(
            description="The input molecule",
        ),
    ]
    distances: t.Annotated[
        list[pdt.PositiveFloat] | None,
        pdt.Field(
            description=(
                "The distances, in Ångstrom, at which the dissociation curve should be "
                "computed. This input is optional since the distances can be also set "
                "via the `distance_count` input."
            ),
        ),
    ] = None
    distance_count: t.Annotated[
        pdt.PositiveInt,
        pdt.Field(
            default=20,
            description=(
                "The number of distances at which the dissociation curve should be "
                "computed, used in conjunction with `distance_min` and `distance_max`. "
                "This input is optional since the distances can be also set via the "
                "`distances` input."
            ),
        ),
    ] = 20
    distance_min: t.Annotated[
        pdt.PositiveFloat,
        pdt.Field(
            default=0.5,
            description=(
                "The minimum distance, in Ångstrom, at which the dissociation curve  "
                "should be computed, used in conjunction with `distance_max` and  "
                "`distance_count`. This input is optional since the distances can be  "
                "also set via the `distances` input."
            ),
        ),
    ] = 0.5
    distance_max: t.Annotated[
        pdt.PositiveFloat,
        pdt.Field(
            default=3,
            description=(
                "The maximum distance, in Ångstrom, at which the dissociation curve "
                "should be computed, used in conjunction with `distance_min` and "
                "`distance_count`. This input is optional since the distances can be "
                "also set via the `distances` input."
            ),
        ),
    ] = 3

    @pdt.model_validator(mode="before")
    def _validate_min_max_distance(self, data: dict):
        if self.distance_min >= self.distance_max:
            raise ValueError(
                "The minimum distance should be smaller than the maximum distance"
            )
        return self


class DcOutputModel(CompositeOutputsModel):
    distances: t.Annotated[
        list[pdt.PositiveFloat],
        pdt.Field(
            description=(
                "The distances, in Ångstrom, at which the dissociation curve was "
                "computed."
            ),
        ),
    ]
