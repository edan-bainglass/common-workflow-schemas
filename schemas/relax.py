import typing as t

from optimade.models import StructureResource
import pydantic as pdt

from .engine import EngineModel
from .utils import FloatArray, MetadataField, WithArbitraryTypes


class CommonRelaxInputsModel(
    pdt.BaseModel,
    WithArbitraryTypes,
):
    engines: t.Annotated[
        dict[str, EngineModel],
        MetadataField(
            description=(
                "A dictionary specifying the codes and the corresponding computational "
                "resources for each step of the workflow."
            ),
            iri="https://example.com/schemas/simulation/engines",
        ),
    ]
    protocol: t.Annotated[
        t.Literal[
            "fast",
            "moderate",
            "precise",
        ],
        MetadataField(
            description=(
                "A single string summarizing the computational accuracy of the "
                "underlying DFT calculation and relaxation algorithm. Three protocol "
                "names are defined and implemented for each code: 'fast', 'moderate' "
                "and 'precise'. The details of how each implementation translates a "
                "protocol string into a choice of parameters is code dependent, or "
                "more specifically, they depend on the implementation choices of the "
                "corresponding AiiDA plugin."
            ),
            iri="https://example.com/schemas/simulation/scf/protocol",
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
            iri="https://example.com/schemas/simulation/scf/relax/relax_type",
        ),
    ]
    threshold_forces: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            description=(
                "A real positive number indicating the target threshold for the forces "
                "in eV/Å. If not specified, the protocol specification will select an "
                "appropriate value."
            ),
            iri="https://example.com/schemas/simulation/scf/relax/threshold_forces",
            units="eV/Å",
        ),
    ]
    threshold_stress: t.Annotated[
        pdt.PositiveFloat,
        MetadataField(
            description=(
                "A real positive number indicating the target threshold for the stress "
                "in eV/Å^3. If not specified, the protocol specification will select "
                "an appropriate value."
            ),
            iri="https://example.com/schemas/simulation/scf/relax/threshold_stress",
            units="eV/Å^3",
        ),
    ]
    electronic_type: t.Annotated[
        t.Literal[
            "metal",
            "insulator",
        ]
        | None,
        MetadataField(
            description=(
                "An optional string to signal whether to perform the simulation for a "
                "metallic or an insulating system. It accepts only the 'insulator' and "
                "'metal' values. This input is relevant only for calculations on "
                "extended systems. In case such option is not specified, the "
                "calculation is assumed to be metallic which is the safest assumption."
            ),
            iri="https://example.com/schemas/simulation/scf/electronic_type",
        ),
    ] = None
    spin_type: t.Annotated[
        t.Literal[
            "none",
            "collinear",
        ]
        | None,
        MetadataField(
            description=(
                "An optional string to specify the spin degree of freedom for the "
                "calculation. It accepts the values 'none' or 'collinear'. These will "
                "be extended in the future to include, for instance, non-collinear "
                "magnetism and spin-orbit coupling. The default is to run the "
                "calculation without spin polarization."
            ),
            iri="https://example.com/schemas/simulation/scf/spin_type",
        ),
    ] = None
    magnetization_per_site: t.Annotated[
        list[float] | None,
        MetadataField(
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
            iri="https://example.com/schemas/simulation/structure/site/magnetization",
            units="μB",
        ),
    ] = None
    reference_process: t.Annotated[
        str | None,
        MetadataField(
            description=(
                "A unique string identifier of the process, such as a PK or UUID. When "
                "present, the interface returns a set of inputs which ensure that "
                "results of the new process (to be run) can be directly compared to "
                "the `reference_process`. The field is given as a string representing "
                "the unique identifier of the process, such as PK or UUID."
            ),
            iri="https://example.com/schemas/simulation/process/orchestrator",
        ),
    ] = None


class RelaxInputsModel(CommonRelaxInputsModel):
    structure: t.Annotated[
        StructureResource,
        MetadataField(
            description="The structure to relax.",
            iri="https://example.com/schemas/simulation/structure",
        ),
    ]


class RelaxOutputsModel(
    pdt.BaseModel,
    WithArbitraryTypes,
):
    forces: t.Annotated[
        FloatArray,
        MetadataField(
            description="The forces on the atoms.",
            iri="https://example.com/schemas/simulation/relax/forces",
            units="eV/Å",
        ),
    ]
    structure: t.Annotated[
        StructureResource | None,
        MetadataField(
            description="The relaxed structure, if relaxation was performed.",
            iri="https://example.com/schemas/simulation/relax/structure",
            units="Å",
        ),
    ]
    total_energy: t.Annotated[
        float,
        MetadataField(
            description=(
                "The total energy in eV associated to the relaxed structure (or "
                "initial structure in case no relaxation is performed)."
            ),
            iri="https://example.com/schemas/simulation/scf/total_energy",
            units="eV",
        ),
    ]
    stress: t.Annotated[
        FloatArray | None,
        MetadataField(
            description=(
                "The final stress tensor in eV/Å^3, if relaxation was performed."
            ),
            iri="https://example.com/schemas/simulation/relax/stress",
            units="eV/Å^3",
        ),
    ]
    total_magnetization: t.Annotated[
        float | None,
        MetadataField(
            description="The total magnetization of the system in μB.",
            iri="https://example.com/schemas/simulation/total_magnetization",
            units="μB",
        ),
    ]
