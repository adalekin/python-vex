import requests
import lxml.html


# noinspection PyMethodMayBeStatic
class BaseProvider(object):
    name = ""

    def parse(self, url, proxy=None):
        raise NotImplementedError('Implement in subclass')

    def decorate(self, url):
        return url

    def _get_content(self, url, proxy=None):
        proxies = None
        if proxy:
            proxies = {'http': proxy}
        r = requests.get(url, proxies=proxies, verify=False)
        return r.content

    def _get_selector(self, url, proxy=None):
        content = self._get_content(url, proxy)
        doc = lxml.html.document_fromstring(content)
        return doc, content
