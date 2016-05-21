import json
import datetime
from urllib import unquote_plus

import dateutil
import pytz
import re
import html2text
import requests

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

from .base import BaseProvider
from .utils import extractor, stringify_children, html_attribute_value, \
    json_attribute_value

REGEX_FACEBOOK_VIDEO_ID = re.compile("v=(?P<video_id>[^&]*)")


class FacebookProvider(BaseProvider):
    name = "facebook"

    def parse(self, url, proxy=None):
        hs, content = self._get_selector(url, proxy)

        try:
            # TODO: regexp
            data = content.split("[[\"params\",\"")[1].split("\"]")[0]
            data = data.decode('unicode_escape')
            data = json.loads(unquote_plus(data))
        except IndexError:
            return None

        match = re.search(
            r'feedbacktargets\":\[(?P<feedback>.+?})\],\"comments\"', content)
        feedback_data = json.loads(match.group("feedback"))

        uid = content.split("\"actorid\":\"")[1].split("\",")[0]
        description_node = extractor(hs, "//span[@id='fbPhotoPageCaption']")
        if description_node:
            description = html2text.html2text(
                stringify_children(description_node)).strip(' \t\n\r')
        r = requests.get(
            "http://graph.facebook.com/%s/picture?redirect=0&height=640&type=normal&width=640" % uid,
            proxies={'http': proxy} if proxy else None)

        return {
            "user": {
                "uid": uid,
                "name": extractor(
                    hs, "//div[@id='fbPhotoPageAuthorName']/a/text()"),
                "image": json.loads(r.content)["data"]["url"]
            },

            "thumbnail": self._strip_thumbnail(self._find_thumbnail_url(content)),
            "remote": feedback_data["permalink"].replace("\\", ""),
            "remote_standard_resolution": data["video_data"]['progressive'][0]["hd_src"].replace("\\", ""),
            "remote_low_resolution": data["video_data"]['progressive'][0]["sd_src"].replace("\\", ""),
            "description": description,
            "created_at": datetime.datetime.fromtimestamp(
                int(html_attribute_value(content, "utime")[0])),
            "watch_count": feedback_data["likecount"],
            "provider": self.name,
        }

    @staticmethod
    def _strip_thumbnail(image_url):
        if image_url:
            return image_url.replace("_t", "_b").replace("p32x32/", "")

    @staticmethod
    def _find_thumbnail_url(html):
        thumbnail_url = None

        REGEX_URL = re.compile(
            r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
        for url in REGEX_URL.findall(html):
            if '_b.jpg' in url[0]:
                thumbnail_url = url[0]

        if thumbnail_url:
            h = HTMLParser()
            thumbnail_url = h.unescape(thumbnail_url)
        return thumbnail_url
