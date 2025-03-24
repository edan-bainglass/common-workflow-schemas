import re

BASE_PREFIX = "https://example.com/commonWorkflows"


def build_context(schema):
    context = {
        "ex": "https://example.com/",
    }

    def snake_case(class_name):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

    def walk(entry, parent_key=None):
        if isinstance(entry, dict):
            if "@id" in entry:
                iri = entry.pop("@id")
                if parent_key:
                    context[snake_case(parent_key)] = iri

            if "@container" in entry:
                container_value = entry.pop("@container")
                if parent_key:
                    context[snake_case(parent_key)] = {"@container": container_value}

            for k, v in entry.items():
                walk(v, parent_key=k)

        elif isinstance(entry, list):
            for item in entry:
                walk(item)

    walk(schema)

    return context
