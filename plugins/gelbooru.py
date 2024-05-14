from random import randint
from typing import TYPE_CHECKING
import requests

from plugins.base import BasePlugin, BasePostInfo
from .errors import EmptyResponse, NoImageFound

if TYPE_CHECKING:
    from typings import ImageType


class GelbooruPost(BasePostInfo):
    def get_url(self):
        return f"https://gelbooru.com/index.php?page=post&s=view&id={self.post_id}"


class GelbooruPlugin(BasePlugin):
    url = "https://gelbooru.com/index.php"

    def __init__(
        self,
        tags: list[str] = [],
        image_type: "ImageType" = "sample",
    ):
        super().__init__(tags, image_type)

    def select_image(self, data: dict):
        post: dict
        for post in data.get("post", [{}]):
            if not post:
                continue

            if not post.get(self.image_type):
                continue

            return GelbooruPost(
                post_id=post["id"],
                source_url=post.get("source", ""),
                file_url=post[self.image_type],
                title=post.get("title", ""),
                tags=post["tags"],
                uploader=post.get("owner", ""),
            )

    def get_tags_count(self) -> int:
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "tags": self.parsed_tags,
            "limit": 1,
        }

        response = requests.get(
            self.url, params="&".join("%s=%s" % (k, v) for k, v in params.items())
        )
        response.raise_for_status()

        data = response.json()
        count = data["@attributes"]["count"]
        if count == 0:
            raise NoImageFound()

        return count

    def get_random_image(self) -> BasePostInfo | None:
        params = {
            "page": "dapi",
            "s": "post",
            "q": "index",
            "json": 1,
            "tags": self.parsed_tags,
            "limit": 1,
            "pid": randint(1, self.get_tags_count()),
        }

        response = requests.get(
            self.url, params="&".join("%s=%s" % (k, v) for k, v in params.items())
        )
        if not response or not response.ok:
            raise EmptyResponse()

        data = response.json()
        if not data or not data.get("post"):
            raise EmptyResponse()

        return self.select_image(data)

    def run(self):
        for _ in range(5):
            try:
                response = self.get_random_image()
            except EmptyResponse:
                continue
            except NoImageFound:
                return

            if response:
                break

        return response
