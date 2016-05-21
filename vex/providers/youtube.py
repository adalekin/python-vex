import pytz
import dateutil.parser
import re
import datetime
import requests
import json
import pafy
from pafy.pafy import g
from urllib2 import build_opener, ProxyHandler

from .base import BaseProvider

REGEX_YOUTUBE_VIDEO_ID = re.compile(
    "(?:^|[^\w-]+)(?P<video_id>[\w-]{11})(?:[^\w-]+|$)")


class YouTubeProvider(BaseProvider):
    name = "youtube"

    def parse(self, url, proxy=None):
        # FIXME: useless for the concurrent processing
        if proxy:
            proxy_handler = ProxyHandler({'http': proxy})
            g.opener = build_opener(proxy_handler)

        result = {}

        try:
            video_id = REGEX_YOUTUBE_VIDEO_ID.search(url)
            video = pafy.new(
                self.decorate(video_id.group("video_id")))
        except IOError, exc:
            raise ValueError(unicode(exc))

        result["user"] = {
            "uid": video.username,
            "name": video.username,
            "image": None
        }

        standard_resolution_stream = \
            video.getbest(preftype="mp4")
        result["standard_resolution"] = self._stream_to_dict(
            standard_resolution_stream
        )

        low_resolution_stream = \
            [stream for stream in video.streams
                if stream.resolution == "640x360" and stream.extension == "mp4"][0]
        result["low_resolution"] = self._stream_to_dict(
            low_resolution_stream
        )

        result["thumbnail"] = \
            "http://img.youtube.com/vi/%s/maxresdefault.jpg" % video.videoid

        proxies = None
        if proxy:
            proxies = {'http': proxy}
        r = requests.head(result["thumbnail"], proxies=proxies)
        # If maxresdefault is a placeholder get the bigest thumbnail
        if r.status_code == 404:
            result["thumbnail"] = \
                "http://img.youtube.com/vi/%s/0.jpg" % video.videoid

        result["remote"] = "http://youtube.com/watch?v=%s" % video.videoid
        result["title"] = video.title
        if video.description:
            result["description"] = video.description
        result["category"] = video.category
        result["keywords"] = video.keywords

        # Fix a wrong date format
        published = video.published
        if published.endswith(':'):
            published += '00'

        result["created_at"] = datetime.datetime.strptime(
            published, "%Y-%m-%d %H:%M:%S")

        result["watch_count"] = video.viewcount
        result["provider"] = self.name

        return result

    def decorate(self, url):
        return "http://youtube.com/watch?v=%s" % url

    @staticmethod
    def _stream_to_dict(stream):
        width, height = stream.resolution.split("x")
        return {
            "url": stream.url,
            "width": width,
            "height": height,
        }
