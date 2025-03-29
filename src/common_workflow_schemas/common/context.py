from __future__ import annotations

BASE_PREFIX = "https://example.com/commonWorkflows"


def reduce_iri(iri: str) -> str:
    if iri.startswith(BASE_PREFIX):
        return iri.replace(f"{BASE_PREFIX}/", "cw:")
    elif iri.startswith("https://example.com/"):
        return iri.replace("https://example.com/", "ex:")
    return iri


def reduce_to_prefixes(context: dict) -> None:
    for key, value in context.items():
        if isinstance(value, dict):
            if "@id" in value:
                value["@id"] = reduce_iri(value["@id"])
            if "@context" in value:
                reduce_to_prefixes(value["@context"])
        elif isinstance(value, str):
            context[key] = reduce_iri(value)


def extract_context_from_class_definition(
    class_key: str,
    classes: dict,
    visited: set,
    flat_context: dict,
) -> dict | None:
    if class_key in visited:
        return None
    visited.add(class_key)

    def_schema = classes.get(class_key)
    if not def_schema or "@id" not in def_schema:
        return None

    this_context = {}
    for prop, prop_def in def_schema.get("properties", {}).items():
        if isinstance(prop_def, dict):
            if "@id" in prop_def:
                this_context[prop] = prop_def.pop("@id")
            if "$ref" in prop_def:
                inner_ref: str = prop_def["$ref"]
                inner_def_key = inner_ref.split("/")[-1]
                if inner_def_key not in this_context:
                    extract_context_from_class_definition(
                        inner_def_key,
                        classes,
                        visited,
                        flat_context,
                    )

    flat_context[class_key] = {
        "@id": def_schema.pop("@id"),
        "@context": this_context,
    }

    return flat_context[class_key]


def build_context(object_name: str, schema: dict) -> dict:
    context = {
        object_name: schema.pop("@id"),
    }

    classes = schema.get("$defs", {})
    visited_classes = set()
    flat_context = {}

    for class_key in classes:
        extract_context_from_class_definition(
            class_key,
            classes,
            visited_classes,
            flat_context,
        )

    def walk(entry, parent_key=None):
        if isinstance(entry, dict):
            if "@id" in entry:
                iri = entry.pop("@id")
                if parent_key:
                    context[parent_key] = iri

            if "@container" in entry:
                container_value = entry.pop("@container")
                if parent_key:
                    context[parent_key] = {"@container": container_value}

            for k, v in entry.items():
                walk(v, parent_key=k)

        elif isinstance(entry, list):
            for item in entry:
                walk(item)

    walk(schema.get("properties", {}))
    context.update(flat_context)
    reduce_to_prefixes(context)

    return {
        "@vocab": "https://example.com/",
        "ex": "https://example.com/",
        "cw": "ex:commonWorkflows/",
        **context,
    }
