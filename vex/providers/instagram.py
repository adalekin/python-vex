import json
import datetime

from .base import BaseProvider


class InstagramProvider(BaseProvider):
    name = "instagram"

    def parse(self, url, proxy=None):
        hs, content = self._get_selector(url, proxy)
        data = content.split("window._sharedData = ")[1] \
                      .split(";</script>")[0]
        data = json.loads(data)
        # Error page
        if "DesktopPPage" not in data["entry_data"]:
            return None
        data = data["entry_data"]["DesktopPPage"][0]["media"]

        # Ensure that we try to parse a video
        if not data["is_video"]:
            return None

        return {
            "user": {
                "uid": data["owner"]["username"],
                "name": data["owner"]["username"],
                "image": data["owner"]["profile_pic_url"],
            },
            "thumbnail": data["display_src"],
            "remote": url,
            "remote_standard_resolution": data["video_url"],
            "description": data.get("caption", ""),
            "created_at": datetime.datetime.fromtimestamp(int(data["date"])),
            "watch_count": int(data["likes"]["count"]),
            "provider": self.name,
        }
