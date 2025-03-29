import typing as t

import pydantic as pdt
from optimade.models import StructureResource

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import SemanticModel, WithArbitraryTypes

from .composite import CompositeInputs, CompositeOutputs
from .relax import CommonRelaxInputs


BondDistance = t.Annotated[
    pdt.PositiveFloat,
    MetadataField(
        description="A bond distance in Ångstrom",
        iri=f"{BASE_PREFIX}/dc/Distance",
        units="Å",
    ),
]


class DcCommonRelaxInputs(CommonRelaxInputs):
    _IRI = f"{BASE_PREFIX}/relax/dc/Input"

    relax_type: t.Annotated[
        t.Literal["none"],
        MetadataField(
            default="none",
            description="This field is fixed to 'none' denoting a single-point calculation.",
            iri=f"{BASE_PREFIX}/scf/RelaxType",
            frozen=True,
        ),
    ] = "none"


class DcInput(
    CompositeInputs[DcCommonRelaxInputs],
    SemanticModel,
    WithArbitraryTypes,
):
    _IRI = f"{BASE_PREFIX}/dc/Input"

    molecule: t.Annotated[
        StructureResource,
        MetadataField(
            description="The input molecule",
            iri=f"{BASE_PREFIX}/Molecule",
        ),
    ]
    distances: t.Annotated[
        t.Optional[list[BondDistance]],
        MetadataField(
            description="The distances, in Ångstrom, at which the dissociation curve should be computed. This input is optional since the distances can be also set via the `distance_count` input.",
            container=list,
        ),
    ] = None
    distance_count: t.Annotated[
        pdt.PositiveInt,
        MetadataField(
            default=20,
            description="The number of distances at which the dissociation curve should be computed, used in conjunction with `distance_min` and `distance_max`. This input is optional since the distances can be also set via the `distances` input.",
            iri=f"{BASE_PREFIX}/dc/DistanceCount",
        ),
    ] = 20
    distance_min: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            default=0.5,
            description="The minimum distance, in Ångstrom, at which the dissociation curve should be computed, used in conjunction with `distance_max` and `distance_count`. This input is optional since the distances can be also set via the `distances` input.",
            iri=f"{BASE_PREFIX}/dc/DistanceMin",
            units="Å",
        ),
    ] = 0.5
    distance_max: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            default=3,
            description="The maximum distance, in Ångstrom, at which the dissociation curve should be computed, used in conjunction with `distance_min` and `distance_count`. This input is optional since the distances can be also set via the `distances` input.",
            iri=f"{BASE_PREFIX}/dc/DistanceMax",
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


class DcOutput(CompositeOutputs):
    _IRI = f"{BASE_PREFIX}/dc/Output"

    distances: t.Annotated[
        list[BondDistance],
        MetadataField(
            description="The distances, in Ångstrom, at which the dissociation curve was computed.",
            container=list,
        ),
    ]
