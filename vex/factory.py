import re
import requests
import hashlib
from PIL import Image, ImageOps
from cStringIO import StringIO

from .providers import *
from .utils import get_in_dict, set_in_dict


class URLExtractor(object):

    def __init__(self, regex, parser_class):
        self.regex = re.compile(regex)
        self.parser = parser_class()

    def extract(self, content, proxy=None):
        results = []
        for url in self.extract_urls(content):
            result = self.extract_from_url(url, proxy)
            if not result:
                continue
            results.append(result)
        return results

    def extract_from_url(self, url, proxy=None):
        if self.regex.match(url):
            return self.parser.parse(url, proxy=proxy)

    def extract_urls(self, content):
        return [self.parser.decorate(r) for r in self.regex.findall(content)]


class Factory(object):
    rules = (
        URLExtractor(
            '(?:http|https|)(?::\/\/|)(?:www.|)(?:youtu\.be\/|youtube\.com(?:\/embed\/|\/v\/|\/watch\?v=|\/ytscreeningroom\?v=|\/feeds\/api\/videos\/|\/user\S*[^\w\-\s]))([\w\-]{11})[a-z0-9;:@#?&%=+\/\$_.-]*',
            YouTubeProvider),
        URLExtractor("https?://(www\.facebook\.com/photo\.php.*|www\.facebook\.com/video/video\.php.*)", FacebookProvider),
        URLExtractor("https?://(?:www\.)?(vimeo\.com/(\d+))", VimeoProvider),
        URLExtractor("https?://(instagr\.am/p/.*|instagram\.com/p/.*)", InstagramProvider),
    )

    def __init__(self, proxy=None):
        self.proxy = proxy

    def extract_from_url(self, url):
        for url_extractor in self.rules:
            result = url_extractor.extract_from_url(url, self.proxy)

            if result:
                return result

    def extract(self, url):
        r = requests.get(url, proxies={'http': self.proxy} if self.proxy else None, verify=False)

        results = self.extract_from_url(r.url)
        if results:
            return [results]

        results = []
        for url_extractor in self.rules:
            results += url_extractor.extract(r.content, self.proxy)

        return results


class ThumbnailFactory(Factory):
    IMAGE_FIELDS = ("thumbnail", ("user", "image"))
    IMAGE_THUMBS = {
        'standard': {'suffix': '@2x',
                     'size': (640, 640), },
        'low': (320, 320),
        'thumbnail': (150, 150),
    }

    def __init__(self, storage, proxy=None):
        super(ThumbnailFactory, self).__init__(proxy)
        self.storage = storage

    def _full_file_path(self, url):
        image_guid = hashlib.sha1(url).hexdigest()
        return 'full/%s/%s/%s.jpg' % (image_guid[0], image_guid[1], image_guid)

    def _thumb_file_path(self, thumb_id, thumb_params, url):
        suffix = ""

        if isinstance(thumb_params, dict):
            if "suffix" in thumb_params:
                suffix = thumb_params["suffix"]

        thumb_guid = hashlib.sha1(url).hexdigest()
        return 'thumbs/%s/%s/%s/%s%s.jpg' % (thumb_id, thumb_guid[0], thumb_guid[1], thumb_guid, suffix)

    def _convert_image(self, image, size=None):
        if image.format == 'PNG' and image.mode == 'RGBA':
            background = Image.new('RGBA', image.size, (255, 255, 255))
            background.paste(image, image)
            image = background.convert('RGB')
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        if size:
            image = ImageOps.fit(image.copy(), size, Image.ANTIALIAS)

        buf = StringIO()
        image.save(buf, 'JPEG')
        return image, buf

    def _download_image(self, url):
        if not url:
            return None

        result = {"url": url,
                  "original": self._full_file_path(url), }

        r = requests.get(url, proxies={'http': self.proxy} if self.proxy else None, verify=False)
        orig_image = Image.open(StringIO(r.content))
        orig_image, orig_buffer = self._convert_image(orig_image)

        self.storage.save(result["original"], orig_buffer)

        for thumb_id, thumb_params in self.IMAGE_THUMBS.iteritems():
            if isinstance(thumb_params, dict):
                thumb_size = thumb_params["size"]
            else:
                thumb_size = thumb_params
            thumb_image, thumb_buffer = self._convert_image(orig_image, thumb_size)
            result[thumb_id] = self._thumb_file_path(thumb_id, thumb_params, result["url"])

            self.storage.save(result[thumb_id], thumb_buffer)
        return result

    def _download_all_images(self, video):
        for image_field in self.IMAGE_FIELDS:
            if isinstance(image_field, basestring):
                video[image_field] = self._download_image(video[image_field])
            if isinstance(image_field, tuple):
                set_in_dict(video,
                            image_field,
                            self._download_image(get_in_dict(video, image_field)))
        return video

    def extract(self, url):
        videos = super(ThumbnailFactory, self).extract(url)
        return [self._download_all_images(video) for video in videos] if videos else None
