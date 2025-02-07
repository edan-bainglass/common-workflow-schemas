from __future__ import annotations

import typing as t

import pydantic as pdt
from aiida import orm
from numpy.typing import NDArray

from .engine import EngineModel
from .utils import WithArbitraryTypes


class CommonRelaxInputsModel(
    pdt.BaseModel,
    WithArbitraryTypes,
):
    engines: t.Annotated[
        dict[str, EngineModel],
        pdt.Field(
            description=(
                "A dictionary specifying the codes and the corresponding computational "
                "resources for each step of the workflow."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/engines",
            },
        ),
    ]
    protocol: t.Annotated[
        t.Literal[
            "fast",
            "moderate",
            "precise",
        ],
        pdt.Field(
            description=(
                "A single string summarizing the computational accuracy of the "
                "underlying DFT calculation and relaxation algorithm. Three protocol "
                "names are defined and implemented for each code: 'fast', 'moderate' "
                "and 'precise'. The details of how each implementation translates a "
                "protocol string into a choice of parameters is code dependent, or "
                "more specifically, they depend on the implementation choices of the "
                "corresponding AiiDA plugin."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/protocol",
            },
        ),
    ]
    relax_type: t.Annotated[
        t.Literal[
            "none",
            "positions",
            "volume",
            "shape",
            "cell",
            "positions_cell",
            "positions_volume",
            "positions_shape",
        ],
        pdt.Field(
            description=(
                "The type of relaxation to perform, ranging from the relaxation of "
                "only atomic coordinates to the full cell relaxation for extended "
                "systems. The complete list of supported options is: 'none', "
                "'positions', 'volume', 'shape', 'cell', 'positions_cell', "
                "'positions_volume', 'positions_shape'. Each name indicates the "
                "physical quantities allowed to relax. For instance, 'positions_shape' "
                "corresponds to a relaxation where both the shape of the cell and the "
                "atomic coordinates are relaxed, but not the volume; in other words, "
                "this option indicates a geometric optimization at constant volume. "
                'On the other hand, the "shape" option designates a situation when '
                "the shape of the cell is relaxed and the atomic coordinates are "
                "rescaled following the variation of the cell, not following a force "
                "minimization process. The term “cell” is short-hand for the "
                'combination of "shape" and "volume". The option "none" indicates the '
                "possibility to calculate the total energy of the system without "
                "optimizing the structure. Not all options are available for each "
                'code. The "none" and "positions" options are shared by all codes.'
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/relax_type",
            },
        ),
    ]
    threshold_forces: t.Annotated[
        pdt.PositiveFloat,
        pdt.Field(
            description=(
                "A real positive number indicating the target threshold for the forces "
                "in eV/Å. If not specified, the protocol specification will select an "
                "appropriate value."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/threshold_forces",
            },
        ),
    ]
    threshold_stress: t.Annotated[
        pdt.PositiveFloat,
        pdt.Field(
            description=(
                "A real positive number indicating the target threshold for the stress "
                "in eV/Å^3. If not specified, the protocol specification will select "
                "an appropriate value."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/threshold_stress",
            },
        ),
    ]
    electronic_type: t.Annotated[
        t.Literal[
            "metal",
            "insulator",
        ]
        | None,
        pdt.Field(
            description=(
                "An optional string to signal whether to perform the simulation for a "
                "metallic or an insulating system. It accepts only the 'insulator' and "
                "'metal' values. This input is relevant only for calculations on "
                "extended systems. In case such option is not specified, the "
                "calculation is assumed to be metallic which is the safest assumption."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/electronic_type",
            },
        ),
    ]
    spin_type: t.Annotated[
        t.Literal[
            "none",
            "collinear",
        ]
        | None,
        pdt.Field(
            description=(
                "An optional string to specify the spin degree of freedom for the "
                "calculation. It accepts the values 'none' or 'collinear'. These will "
                "be extended in the future to include, for instance, non-collinear "
                "magnetism and spin-orbit coupling. The default is to run the "
                "calculation without spin polarization."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/spin_type",
            },
        ),
    ]
    magnetization_per_site: t.Annotated[
        list[float] | None,
        pdt.Field(
            description=(
                "An input devoted to the initial magnetization specifications. It "
                "accepts a list where each entry refers to an atomic site in the "
                "structure. The quantity is passed as the spin polarization in units "
                "of electrons, meaning the difference between spin up and spin down "
                "electrons for the site. This also corresponds to the magnetization "
                "of the site in Bohr magnetons (μB). The default for this input is "
                "the Python value None and, in case of calculations with spin, the "
                "None value signals that the implementation should automatically "
                "decide an appropriate default initial magnetization."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/magnetization_per_site",
            },
        ),
    ]
    reference_workchain: t.Annotated[
        orm.WorkChainNode | None,
        pdt.Field(
            description=(
                "When this input is present, the interface returns a set of inputs "
                "which ensure that results of the new `WorkChain` (to be run) can be "
                "directly compared to the reference_workchain."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/common_relax/reference_workchain",
            },
        ),
    ]


class RelaxInputsModel(CommonRelaxInputsModel):
    structure: t.Annotated[
        orm.StructureData,
        pdt.Field(
            description="The structure to relax.",
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/structure",
            },
        ),
    ]


class RelaxOutputsModel(
    pdt.BaseModel,
    WithArbitraryTypes,
):
    forces: t.Annotated[
        NDArray,
        pdt.Field(
            description="The forces on the atoms.",
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/forces",
            },
        ),
    ]
    structure: t.Annotated[
        orm.StructureData | None,
        pdt.Field(
            description="The relaxed structure, if relaxation was performed.",
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/structure",
            },
        ),
    ]
    total_energy: t.Annotated[
        float,
        pdt.Field(
            description=(
                "The total energy in eV associated to the relaxed structure (or "
                "initial structure in case no relaxation is performed)."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/total_energy",
            },
        ),
    ]
    stress: t.Annotated[
        NDArray | None,
        pdt.Field(
            description=(
                "The final stress tensor in eV/Å^3, if relaxation was performed."
            ),
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/stress",
            },
        ),
    ]
    total_magnetization: t.Annotated[
        float | None,
        pdt.Field(
            description="The total magnetization of the system.",
            json_schema_extra={
                "iri": "https://example.com/schemas/relax/total_magnetization",
            },
        ),
    ]
