from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

if TYPE_CHECKING:
    from typings import ImageType


@dataclass(init=True, slots=True)
class BasePostInfo:
    post_id: int
    source_url: str
    file_url: str
    title: str
    tags: str
    uploader: str

    def get_url(self) -> str:
        raise NotImplementedError

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


class BasePlugin:
    def __init__(
        self,
        tags: list[str] = [],
        image_type: "ImageType" = "sample",
    ):
        self.tags = tags
        self.parsed_tags = "+".join(self.tags)
        self.image_type = f"{image_type.lower()}_url"

    def run(self, repeat: int = 1) -> list[BasePostInfo]:
        posts = []
        try:
            for _ in range(repeat):
                post = self._run()
                if post:
                    posts.append(post)

        except Exception as e:
            print(f"Error_{e.__class__}: {e}")

        return posts

    def _run(self) -> BasePostInfo | None:
        raise NotImplementedError
