from typing import Literal, TypedDict


ImageType = Literal["sample", "file", "preview"]
WebhookConfig = TypedDict(
    "WebhookConfig", {"url": str, "avatar_url": str | None, "username": str | None}
)
ProviderConfig = TypedDict(
    "ProviderConfig",
    {
        "name": Literal["gelbooru", "danbooru", "konachan", "yandere"],
        "tags": list[str],
        "type": ImageType,
    },
)
ConfigT_ = TypedDict(
    "ConfigT_",
    {
        "webhook_config": WebhookConfig,
        "provider_config": ProviderConfig,
        "repeat": int,
        "image_count": int,
    },
)
