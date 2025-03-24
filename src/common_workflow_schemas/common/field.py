import typing as t

import pydantic as pdt


def MetadataField(
    iri: t.Optional[str] = None,
    units: t.Optional[str] = None,
    container: t.Optional[t.Type[t.Union[set, list]]] = None,
    **kwargs,
) -> t.Any:
    """Wraps around `pydantic.Field` with metadata slots.

    Parameters
    ----------
    `iri` : `str`, optional
        The IRI of the field.
    `units` : `str`, optional
        The units of the field.
    `container` : `type`, optional
        If provided, defines the container type of the field.
    `kwargs`
        `pydantic.Field` keyword arguments.

    Returns
    -------
    `pydantic.Field`
        The field with metadata slots.
    """
    json_schema_extra = kwargs.pop("json_schema_extra", {})

    if iri:
        json_schema_extra["@id"] = iri

    if units:
        json_schema_extra["units"] = units

    if container:
        json_schema_extra["@container"] = f"@{container.__qualname__}"

    return pdt.Field(
        json_schema_extra=json_schema_extra,
        **kwargs,
    )
