import typing as t

import pydantic as pdt
from optimade.models import StructureResource

from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import WithArbitraryTypes

from .composite import CompositeInputsModel, CompositeOutputsModel
from .relax import CommonRelaxInputsModel


class DcCommonRelaxInputsModel(CommonRelaxInputsModel):
    relax_type: t.Annotated[
        t.Literal["none"],
        MetadataField(
            default="none",
            description=(
                "This field is fixed to 'none' denoting a single-point calculation."
            ),
            iri="https://example.com/schemas/simulation/dc/relaxType",
            frozen=True,
        ),
    ] = "none"


class DcInputModel(
    CompositeInputsModel[DcCommonRelaxInputsModel],
    WithArbitraryTypes,
):
    molecule: t.Annotated[
        StructureResource,
        MetadataField(
            description="The input molecule",
            iri="https://example.com/schemas/simulation/molecule",
        ),
    ]
    distances: t.Annotated[
        t.Optional[list[pdt.PositiveFloat]],
        MetadataField(
            description=(
                "The distances, in Ångstrom, at which the dissociation curve should be "
                "computed. This input is optional since the distances can be also set "
                "via the `distance_count` input."
            ),
            iri="https://example.com/schemas/simulation/dc/distances",
            units="Å",
        ),
    ] = None
    distance_count: t.Annotated[
        pdt.PositiveInt,
        MetadataField(
            default=20,
            description=(
                "The number of distances at which the dissociation curve should be "
                "computed, used in conjunction with `distance_min` and `distance_max`. "
                "This input is optional since the distances can be also set via the "
                "`distances` input."
            ),
            iri="https://example.com/schemas/simulation/dc/distanceCount",
        ),
    ] = 20
    distance_min: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            default=0.5,
            description=(
                "The minimum distance, in Ångstrom, at which the dissociation curve  "
                "should be computed, used in conjunction with `distance_max` and  "
                "`distance_count`. This input is optional since the distances can be  "
                "also set via the `distances` input."
            ),
            iri="https://example.com/schemas/simulation/dc/distanceMin",
            units="Å",
        ),
    ] = 0.5
    distance_max: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            default=3,
            description=(
                "The maximum distance, in Ångstrom, at which the dissociation curve "
                "should be computed, used in conjunction with `distance_min` and "
                "`distance_count`. This input is optional since the distances can be "
                "also set via the `distances` input."
            ),
            iri="https://example.com/schemas/simulation/dc/distanceMax",
            units="Å",
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
        MetadataField(
            description=(
                "The distances, in Ångstrom, at which the dissociation curve was "
                "computed."
            ),
            iri="https://example.com/schemas/simulation/dc/distances",
            units="Å",
        ),
    ]
