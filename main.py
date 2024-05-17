import json
from time import sleep
from typing import TYPE_CHECKING

import requests

from plugins.base import BasePlugin
from plugins.gelbooru import GelbooruPlugin

if TYPE_CHECKING:
    from plugins.base import BasePostInfo
    from typings import ConfigT_, ProviderConfig, WebhookConfig


def get_provider(config: "ProviderConfig") -> BasePlugin:
    match config["name"]:
        case _:
            return GelbooruPlugin(config["tags"], config["type"])


def check_config_valid(config: "ConfigT_"):
    if not config:
        raise ValueError("Config is empty")

    if not config.get("webhook_config") or not config.get("provider_config"):
        raise ValueError("Invalid config")

    webhook_config = config["webhook_config"]
    if not webhook_config.get("url"):
        raise ValueError("Invalid webhook url")

    provider_config = config["provider_config"]
    if provider_config.get("name") not in ["gelbooru"]:
        raise ValueError("Provider not supported")

    if provider_config.get("tags") and not isinstance(
        provider_config.get("tags"), list
    ):
        raise ValueError("Tags must be a list")

    if provider_config.get("type") not in ["sample", "file", "preview"]:
        raise ValueError("Invalid image type. Must be 'sample', 'file', or 'preview'")

    repeat = config.get("repeat") or 1
    if repeat > 10 or repeat < 1 or not isinstance(repeat, int):
        print("[Warning] Repeat value is too large or is not set. Set to 1.")
        config["repeat"] = repeat

    count = config.get("image_count") or 1
    if not isinstance(count, int):
        raise ValueError("Image count must be an integer")
    if count > 10:
        print(
            "[Warning] Discord not supporting more than 10 embeds per message. Set to 1."
        )
        config["image_count"] = count


def read_config() -> list["ConfigT_"]:
    with open("config.json") as f:
        return json.load(f)


def make_embed(data: "BasePostInfo"):
    desc = [f"[Post]({data.get_url()})"]
    if data.source_url and not data.source_url.startswith("file://"):
        desc.append(f"[Source]({data.get_source()})")
    desc.append(f"[Download]({data.file_url})")

    return {
        "url": data.get_url(),
        "image": {"url": data.file_url},
        "color": 10394673,
        "description": " | ".join(desc),
    }


def make_webhook_payload(config: "WebhookConfig", data: list["BasePostInfo"]):
    payload = {
        "username": config["username"],
        "avatar_url": config["avatar_url"],
        "embeds": [make_embed(post) for post in data],
    }

    return payload


def main():
    for config in read_config():
        try:
            check_config_valid(config)
        except ValueError as e:
            print(e)
            continue

        provider = get_provider(config["provider_config"])
        for _ in range(config["image_count"]):
            post = provider.run(config["image_count"])
            if not post:
                continue

            payload = make_webhook_payload(config["webhook_config"], post)
            webhook_resp = requests.post(config["webhook_config"]["url"], json=payload)
            webhook_resp.raise_for_status()

            sleep(1)


if __name__ == "__main__":
    main()
