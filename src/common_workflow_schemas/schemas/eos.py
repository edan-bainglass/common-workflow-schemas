import typing as t

import pydantic as pdt
from optimade.models import StructureResource

from common_workflow_schemas.common.mixins import WithArbitraryTypes
from common_workflow_schemas.utils.metadata import MetadataField

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
        MetadataField(
            description=(
                "The type of relaxation to perform, limited to fixed-volume "
                "relaxations."
            ),
            # TODO should iri extend the base relax_type iri?
            iri="https://example.com/schemas/simulation/eos/relax_type",
        ),
    ]


class EosInputsModel(
    CompositeInputsModel[EosCommonRelaxInputsModel],
    WithArbitraryTypes,
):
    structure: t.Annotated[
        StructureResource,
        MetadataField(
            description="The input structure",
            iri="https://example.com/schemas/simulation/structure",
        ),
    ]
    scale_factors: t.Annotated[
        list[pdt.PositiveFloat] | None,
        MetadataField(
            description=(
                "The scale factors at which the volume and total energy of the "
                "structure should be computed. This input is optional since the scale "
                "factors can be also set via the `scale_count` and `scale_increment` "
                "inputs."
            ),
            iri="https://example.com/schemas/simulation/eos/scale_factors",
        ),
    ]
    scale_count: t.Annotated[
        pdt.PositiveInt | None,
        MetadataField(
            description=(
                "The number of scale factors at which the volume and total energy of "
                "the structure should be computed, used in conjunction with "
                "`scale_increment`. This input is optional since the scale factors can "
                "be also set via the `scale_factors` input."
            ),
            iri="https://example.com/schemas/simulation/eos/scale_count",
        ),
    ]
    scale_increment: t.Annotated[
        pdt.PositiveFloat | None,
        MetadataField(
            description=(
                "The increment between the scale factors at which the volume and "
                "total energy of the structure should be computed, used in conjunction "
                "with `scale_count`. This input is optional since the scale factors "
                "can be also set via the `scale_factors` input."
            ),
            iri="https://example.com/schemas/simulation/eos/scale_increment",
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


class EosOutputsModel(
    CompositeOutputsModel,
    WithArbitraryTypes,
):
    structures: t.Annotated[
        list[StructureResource],
        MetadataField(
            description="The list of relaxed structures.",
            iri="https://example.com/schemas/simulation/eos/structures",
        ),
    ]
