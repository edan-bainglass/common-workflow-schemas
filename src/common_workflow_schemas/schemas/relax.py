import typing as t

import pydantic as pdt
from optimade.models import StructureResource

from common_workflow_schemas.common.context import BASE_PREFIX
from common_workflow_schemas.common.field import MetadataField
from common_workflow_schemas.common.mixins import SemanticModel, WithArbitraryTypes
from common_workflow_schemas.common.types import FloatArray, UniqueIdentifier

from .engine import Engine

TotalEnergy = t.Annotated[
    float,
    MetadataField(
        description="The total energy associated to the relaxed structure (or initial structure in case no relaxation is performed.",
        iri=f"{BASE_PREFIX}/scf/TotalEnergy",
        units="eV",
    ),
]

TotalMagnetization = t.Annotated[
    float,
    MetadataField(
        description="The total magnetization of a system.",
        iri=f"{BASE_PREFIX}/scf/TotalMagnetization",
        units="μB",
    ),
]


class CommonRelaxInputs(SemanticModel):
    _IRI = f"{BASE_PREFIX}/relax/Input"

    engines: t.Annotated[
        dict[str, Engine],
        MetadataField(
            description="A dictionary specifying the codes and the corresponding computational resources for each step of the workflow.",
            iri=f"{_IRI}/Engines",
        ),
    ]
    protocol: t.Annotated[
        t.Literal[
            "fast",
            "moderate",
            "precise",
        ],
        MetadataField(
            description="A single string summarizing the computational accuracy of the underlying DFT calculation and relaxation algorithm. Three protocol names are defined and implemented for each code: 'fast', 'moderate' and 'precise'. The details of how each implementation translates a protocol string into a choice of parameters is code dependent, or more specifically, they depend on the implementation choices of the corresponding AiiDA plugin.",
            iri=f"{BASE_PREFIX}/scf/Protocol",
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
        MetadataField(
            description="The type of relaxation to perform, ranging from the relaxation of only atomic coordinates to the full cell relaxation for extended systems. The complete list of supported options is: 'none', 'positions', 'volume', 'shape', 'cell', 'positions_cell', 'positions_volume', 'positions_shape'. Each name indicates the physical quantities allowed to relax. For instance, 'positions_shape' corresponds to a relaxation where both the shape of the cell and the atomic coordinates are relaxed, but not the volume; in other words, this option indicates a geometric optimization at constant volume. On the other hand, the 'shape' option designates a situation when the shape of the cell is relaxed and the atomic coordinates are rescaled following the variation of the cell, not following a force minimization process. The term 'cell' is short-hand for the combination of 'shape' and 'volume'. The option 'none' indicates the possibility to calculate the total energy of the system without optimizing the structure. Not all options are available for each code. The 'none' and 'positions' options are shared by all codes.",
            iri=f"{BASE_PREFIX}/scf/RelaxType",
        ),
    ]
    threshold_forces: t.Annotated[
        t.Optional[pdt.PositiveFloat],
        MetadataField(
            description="A real positive number indicating the target threshold for the forces in eV/Å. If not specified, the protocol specification will select an appropriate value.",
            iri=f"{BASE_PREFIX}/scf/ThresholdForces",
            units="eV/Å",
        ),
    ] = None
    threshold_stress: t.Annotated[
        t.Optional[pdt.PositiveFloat],
        MetadataField(
            description="A real positive number indicating the target threshold for the stress in eV/Å^3. If not specified, the protocol specification will select an appropriate value.",
            iri=f"{BASE_PREFIX}/scf/ThresholdStress",
            units="eV/Å^3",
        ),
    ] = None
    electronic_type: t.Annotated[
        t.Optional[
            t.Literal[
                "metal",
                "insulator",
            ]
        ],
        MetadataField(
            description="An optional string to signal whether to perform the simulation for a metallic or an insulating system. It accepts only the 'insulator' and 'metal' values. This input is relevant only for calculations on extended systems. In case such option is not specified, the calculation is assumed to be metallic which is the safest assumption.",
            iri=f"{BASE_PREFIX}/scf/ElectronicType",
        ),
    ] = None
    spin_type: t.Annotated[
        t.Optional[
            t.Literal[
                "none",
                "collinear",
            ]
        ],
        MetadataField(
            description="An optional string to specify the spin degree of freedom for the calculation. It accepts the values 'none' or 'collinear'. These will be extended in the future to include, for instance, non-collinear magnetism and spin-orbit coupling. The default is to run the calculation without spin polarization.",
            iri=f"{BASE_PREFIX}/scf/SpinType",
        ),
    ] = None
    magnetization_per_site: t.Annotated[
        t.Optional[list[float]],
        MetadataField(
            description="An input devoted to the initial magnetization specifications. It accepts a list where each entry refers to an atomic site in the structure. The quantity is passed as the spin polarization in units of electrons, meaning the difference between spin up and spin down electrons for the site. This also corresponds to the magnetization of the site in Bohr magnetons (μB). The default for this input is the Python value None and, in case of calculations with spin, the None value signals that the implementation should automatically decide an appropriate default initial magnetization.",
            iri=f"{BASE_PREFIX}/Structure/Site/Magnetization",
            units="μB",
        ),
    ] = None
    reference_process: t.Annotated[
        t.Optional[UniqueIdentifier],
        MetadataField(
            description="The UUID of the process. When present, the interface returns a set of inputs which ensure that results of the new process (to be run) can be directly compared to the `reference_process`.",
            iri=f"{BASE_PREFIX}/ReferenceProcess",
        ),
    ] = None


class RelaxInputs(
    CommonRelaxInputs,
    WithArbitraryTypes,
):
    _IRI = f"{BASE_PREFIX}/relax/Input"

    structure: t.Annotated[
        StructureResource,
        MetadataField(
            description="The structure to relax.",
            iri=f"{BASE_PREFIX}/Structure",
        ),
    ]


class RelaxOutputs(
    SemanticModel,
    WithArbitraryTypes,
):
    _IRI = f"{BASE_PREFIX}/relax/Output"

    forces: t.Annotated[
        FloatArray,
        MetadataField(
            description="The forces on the atoms.",
            iri=f"{BASE_PREFIX}/Forces",
            units="eV/Å",
        ),
    ]
    relaxed_structure: t.Annotated[
        t.Optional[StructureResource],
        MetadataField(
            description="The relaxed structure, if relaxation was performed.",
            iri=f"{BASE_PREFIX}/Structure",
            units="Å",
        ),
    ] = None
    total_energy: TotalEnergy
    stress: t.Annotated[
        t.Optional[FloatArray],
        MetadataField(
            description="The final stress tensor in eV/Å^3, if relaxation was performed.",
            iri=f"{BASE_PREFIX}/relax/Stress",
            units="eV/Å^3",
        ),
    ]
    total_magnetization: t.Optional[TotalMagnetization] = None
    hartree_potential: t.Annotated[
        t.Optional[FloatArray],
        MetadataField(
            description="The Hartree potential.",
            iri=f"{BASE_PREFIX}/scf/HartreePotential",
            units="Rydberg",
        ),
    ] = None
    charge_density: t.Annotated[
        t.Optional[FloatArray],
        MetadataField(
            description="The total magnetization of the system in μB.",
            iri=f"{BASE_PREFIX}/scf/ChargeDensity",
            units="Rydberg",
        ),
    ] = None
