import re


def extractor(tree, selector):
    """
    Helper function that extract info from tree object
    using the selector constrains.
    """
    val = tree.xpath(selector)
    return val[0] if val else None


def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] + list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) + [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))


def html_attribute_value(html, attribute):
    return re.findall(r'%s=\"(.*?)\"' % attribute, html)


def json_attribute_value(json, attribute):
    return re.findall(r'"(%s)":"((\\"|[^"])*)"' % attribute, json)
