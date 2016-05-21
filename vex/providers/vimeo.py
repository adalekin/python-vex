import dateutil
import requests
import json

from .base import BaseProvider
from .utils import extractor


class VimeoProvider(BaseProvider):
    name = "vimeo"

    def parse(self, url, proxy=None):
        hs, content = self._get_selector(url, proxy)

        r = requests.get(
            "http://vimeo.com/api/oembed.json?url=%s" % url,
            proxies={'http': proxy} if proxy else None)
        data = json.loads(r.text)

        like_count = \
            int(extractor(
                hs,
                "//meta[contains(@content, 'UserLikes')]/@content").split(
                    ":")[-1])
        comment_count = \
            int(extractor(
                hs,
                "//meta[contains(@content, 'UserComment')]/@content").split(
                    ":")[-1])
        return {
            "user": {
                "uid": data["author_url"].split("/")[-1],
                "name": data["author_name"],
                "image": None,
            },
            "thumbnail": data["thumbnail_url"],
            "remote": "http://vimeo.com/%s" % data["video_id"],
            "description": data["description"],
            "created_at": dateutil.parser.parse(extractor(hs, "//div[@class='video_meta']//time/@datetime")),
            "watch_count": int(extractor(hs, "//meta[contains(@content, 'UserPlays')]/@content").split(":")[-1]),
            "provider": self.name,
        }
