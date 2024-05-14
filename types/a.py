from typing import Literal, TypedDict


ImageType = Literal["sample", "file", "preview"]
ConfigT_ = TypedDict(
    "ConfigT_",
    {
        "name": str,
        "weebhook_url": str,
        "tags": list[str],
        "provider": str,
        "type": ImageType,
    },
)
