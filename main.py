import json
from typing import TYPE_CHECKING

import requests

from plugins.base import BasePlugin
from plugins.gelbooru import GelbooruPlugin

if TYPE_CHECKING:
    from plugins.base import BasePostInfo
    from types.a import ConfigT_


def get_provider(config: "ConfigT_") -> BasePlugin | None:
    match config["provider"]:
        case "gelbooru":
            return GelbooruPlugin(config["tags"], config["type"])


def read_config() -> list["ConfigT_"]:
    with open("config.json") as f:
        return json.load(f)


def make_webhook_payload(config: "ConfigT_", data: "BasePostInfo") -> dict:
    desc = [f"[Post]({data.get_url()})"]
    if data.source_url:
        desc.append(f"[Source]({data.get_source()})")
    desc.append(f"[Download]({data.file_url})")

    payload = {
        "username": config["name"],
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
    configs = read_config()
    for config in configs:
        provider = get_provider(config)
        if not provider:
            continue

        post = provider.run()
        if not post:
            continue

        payload = make_webhook_payload(config, post)
        requests.post(config["weebhook_url"], json=payload)


if __name__ == "__main__":
    main()
