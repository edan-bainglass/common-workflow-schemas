import typing as t

import pydantic as pdt
from pydantic._internal._model_construction import ModelMetaclass

from common_workflow_schemas.common.context import build_context


class ModelConfigMetaclass(ModelMetaclass):
    """Metaclass to merge model_config from all mixins."""

    def __new__(cls, name, bases, _dict):
        merged_config = pdt.ConfigDict()

        for base in reversed(bases):
            base_config = getattr(base, "model_config", None)
            if isinstance(base_config, t.Mapping):
                merged_config = cls._deep_merge(merged_config, base_config)

        if "model_config" in _dict and isinstance(_dict["model_config"], t.Mapping):
            merged_config = cls._deep_merge(merged_config, _dict["model_config"])

        _dict["model_config"] = pdt.ConfigDict(**merged_config)
        return super().__new__(cls, name, bases, _dict)

    @staticmethod
    def _deep_merge(d1: dict, d2: dict):
        """Recursively merge two dictionaries."""
        merged = dict(d1)
        for key, value in d2.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = ModelConfigMetaclass._deep_merge(merged[key], value)
            else:
                merged[key] = value
        return merged


class BaseModel(pdt.BaseModel, metaclass=ModelConfigMetaclass):
    """Base class that consolidates `ConfigDict` entries."""


class WithArbitraryTypes:
    model_config = pdt.ConfigDict(
        arbitrary_types_allowed=True,
    )


class SemanticMetaclass(ModelConfigMetaclass):
    """Metaclass to add the defined IRI as an `@id` field in the JSON schema."""

    def __new__(cls, name: str, bases: tuple, _dict: dict):
        if class_iri := _dict.get("_IRI"):
            _dict["model_config"] = pdt.ConfigDict(
                json_schema_extra={
                    "@id": class_iri,
                },
            )
        # TODO add <object-IRI/field-name> IRI to model fields that do not provide one
        return super().__new__(cls, name, bases, _dict)


class SemanticModel(BaseModel, metaclass=SemanticMetaclass):
    _IRI = ""

    def model_oo_ld(self):
        schema = self.model_json_schema()
        return {
            "@context": build_context(schema),
            **schema,
        }
