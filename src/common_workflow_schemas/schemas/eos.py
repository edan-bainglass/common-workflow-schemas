import typing as t

import pydantic as pdt
from optimade.models import StructureResource

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import SemanticModel, WithArbitraryTypes

from .composite import CompositeInputs, CompositeOutputs
from .relax import CommonRelaxInputs


class EosCommonRelaxInputs(CommonRelaxInputs):
    _IRI = f"{BASE_PREFIX}/common/relax/eos/Input"

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
            iri=f"{BASE_PREFIX}/scf/RelaxType",
        ),
    ]


class EosInputs(
    CompositeInputs[EosCommonRelaxInputs],
    SemanticModel,
    WithArbitraryTypes,
):
    _IRI = f"{BASE_PREFIX}/eos/Input"

    structure: t.Annotated[
        StructureResource,
        MetadataField(
            description="The input structure",
            iri=f"{BASE_PREFIX}/Structure",
        ),
    ]
    scale_factors: t.Annotated[
        t.Optional[list[pdt.PositiveFloat]],
        MetadataField(
            description=(
                "The scale factors at which the volume and total energy of the "
                "structure should be computed. This input is optional since the scale "
                "factors can be also set via the `scale_count` and `scale_increment` "
                "inputs."
            ),
            iri=f"{BASE_PREFIX}/eos/ScaleFactors",
        ),
    ]
    scale_count: t.Annotated[
        t.Optional[pdt.PositiveInt],
        MetadataField(
            description=(
                "The number of scale factors at which the volume and total energy of "
                "the structure should be computed, used in conjunction with "
                "`scale_increment`. This input is optional since the scale factors can "
                "be also set via the `scale_factors` input."
            ),
            iri=f"{BASE_PREFIX}/eos/ScaleCount",
        ),
    ]
    scale_increment: t.Annotated[
        t.Optional[pdt.PositiveFloat],
        MetadataField(
            description=(
                "The increment between the scale factors at which the volume and "
                "total energy of the structure should be computed, used in conjunction "
                "with `scale_count`. This input is optional since the scale factors "
                "can be also set via the `scale_factors` input."
            ),
            iri=f"{BASE_PREFIX}/eos/ScaleIncrement",
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


class EosOutputs(
    CompositeOutputs,
    SemanticModel,
    WithArbitraryTypes,
):
    structures: t.Annotated[
        list[StructureResource],
        MetadataField(
            description="The list of relaxed structures.",
            container=list,
        ),
    ]
