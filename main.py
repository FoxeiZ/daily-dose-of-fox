import json
from typing import TYPE_CHECKING

import requests

from plugins.base import BasePlugin
from plugins.gelbooru import GelbooruPlugin

if TYPE_CHECKING:
    from plugins.base import BasePostInfo
    from types.a import ConfigT_, ProviderConfig, WebhookConfig


def get_provider(config: "ProviderConfig") -> BasePlugin | None:
    match config["name"]:
        case "gelbooru":
            return GelbooruPlugin(config["tags"], config["type"])


def read_config() -> list["ConfigT_"]:
    with open("config.json") as f:
        return json.load(f)


def make_webhook_payload(config: "WebhookConfig", data: "BasePostInfo") -> dict:
    desc = [f"[Post]({data.get_url()})"]
    if data.source_url:
        desc.append(f"[Source]({data.get_source()})")
    desc.append(f"[Download]({data.file_url})")

    payload = {
        "username": config["username"],
        "avatar_url": config["avatar_url"],
        "embeds": [
            {
                "url": data.get_url(),
                "image": {"url": data.file_url},
                "color": 10394673,
                "description": " | ".join(desc),
            }
        ],
    }

    return payload


def main():
    for config in read_config():
        if (
            not config
            or not config.get("webhook_config")
            or not config.get("provider_config")
        ):
            print("Invalid config")
            continue

        provider = get_provider(config["provider_config"])
        if not provider:
            continue

        post = provider.run()
        if not post:
            continue

        payload = make_webhook_payload(config["webhook_config"], post)
        webhook_resp = requests.post(config["webhook_config"]["url"], json=payload)
        webhook_resp.raise_for_status()


if __name__ == "__main__":
    main()
