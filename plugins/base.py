from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from types.a import ImageType


class BasePlugin:
    def __init__(
        self,
        tags: list[str] = [],
        image_type: "ImageType" = "sample",
    ):
        self.tags = tags
        self.parsed_tags = "+".join(self.tags)
        self.image_type = f"{image_type.lower()}_url"

    def run(self):
        raise NotImplementedError


@dataclass(init=True, slots=True)
class BasePostInfo:
    post_id: int
    source_url: str
    file_url: str
    title: str
    tags: str
    uploader: str

    def get_url(self):
        return f"https://gelbooru.com/index.php?page=post&s=view&id={self.post_id}"

    def get_file(self):
        response = requests.get(self.file_url)
        response.raise_for_status()

        return response.content

    def get_title(self):
        return self.title or ":3"

    def get_source(self):
        return self.source_url or self.get_url()

    def get_uploader(self):
        return self.uploader or "unknown"
