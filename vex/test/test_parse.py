#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from vex.providers import InstagramProvider, FacebookProvider, YouTubeProvider


class TestInstagramProvider(unittest.TestCase):
    def setUp(self):
        self.provider = InstagramProvider()

    def test_photo(self):
        self.assertIsNone(
            self.provider.parse(url="http://instagram.com/p/qvwHJymYdm"))

    def test_not_found(self):
        self.assertIsNone(
            self.provider.parse(url="http://instagram.com/p/qvrxqpsEM5"))


class TestFacebookProvider(unittest.TestCase):
    def setUp(self):
        self.provider = FacebookProvider()

    def test_description(self):
        self.assertIsNotNone(
            self.provider.parse(
                url="https://www.facebook.com/photo.php?v=596614120387204"))


class TestYouTubeProvider(unittest.TestCase):
    def setUp(self):
        self.provider = YouTubeProvider()

    def test_seek(self):
        self.assertIsNotNone(
            self.provider.parse(
                url="http://www.youtube.com/embed/0Rnq1NpHdmw?start=0&amp"))
