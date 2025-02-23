import pydantic as pdt


class WithArbitraryTypes:
    model_config = pdt.ConfigDict(arbitrary_types_allowed=True)
