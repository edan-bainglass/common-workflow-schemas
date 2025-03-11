import typing as t

import pydantic as pdt


def MetadataField(
    iri: t.Optional[str] = None,
    units: t.Optional[str] = None,
    **kwargs,
) -> t.Any:
    """Wraps around `pydantic.Field` with metadata slots.

    Parameters
    ----------
    `iri` : `str`, optional
        The IRI of the field.
    `units` : `str`, optional
        The units of the field.
    `kwargs`
        `pydantic.Field` keyword arguments.

    Returns
    -------
    `pydantic.Field`
        The field with metadata slots.
    """
    return pdt.Field(
        json_schema_extra={
            **kwargs.pop("json_schema_extra", {}),
            "iri": iri,
            "units": units,
        },
        **kwargs,
    )
