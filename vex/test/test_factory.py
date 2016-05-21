#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from vex.factory import Factory


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory()

    def test_youtube(self):
        regex = self.factory.rules[0].regex
        self.assertFalse(regex.match("http://youtube.com"))
        self.assertTrue(regex.match("http://youtube.com/watch?v=XRlKyl6lov8"))
        self.assertTrue(regex.match("http://www.youtube.com/watch?v=XRlKyl6lov8"))

    def test_links_youtube(self):
        extractor = self.factory.rules[0]
        self.assertListEqual(extractor.extract_urls(
            u"""
    	    Ракета-носитель “Союз 2.1б” с разгонным блоком “Фрегат” стартовала с группой космических аппаратов. Основная нагрузка ракеты — это двухтонный метеорологический спутник “Метеор-М №2”. Попутно этим же рейсом летят шесть малых спутников, и один из них — наш DX1.<br/>
            <br/>
            <iframe width="560" height="349" src="//www.youtube.com/embed/NU-RWrDH3w4?wmode=opaque" frameborder="0" allowfullscreen></iframe><br/>
            <br/>
            По этому случаю, сегодня я пишу с Байконура. Да, сегодня Zelenyikot близок к космосу как никогда, и, во многом, благодаря Хабру. Поэтому сегодня я расскажу каково это — оказаться рядом с взлетающей ракетой, и ощутить, как на ней в космос отправляется аппарат, к созданию которого ты причастен. Конечно, моя причастность только в том, что я рассказывал как его создают. Настоящие создатели: руководитель проекта DX1 Александр Малинин и ведущий инженер-конструктор Петр Кудряшов стоят рядом со мной, они помогут в репортаже. Остальные сотрудники «Даурии» — находятся в сколковском офисе в Москве, ждут первых сигналов, которые поймают сами, и ждут известий от радиолюбителей, которых мы <a href="http://habrahabr.ru/company/dauria/blog/228669/">попросили</a> помочь.<br/>
            <a name="habracut"></a><br/>
            """), ["http://youtube.com/watch?v=NU-RWrDH3w4"])

    def test_facebook(self):
        regex = self.factory.rules[1].regex
        self.assertFalse(regex.match("http://facebook.com"))
        self.assertTrue(regex.match("https://www.facebook.com/photo.php?v=10153730280070161&set=vb.92304305160&type=2&theater"))
        self.assertTrue(regex.match("https://www.facebook.com/photo.php?v=10153730280070161"))

    def test_vimeo(self):
        regex = self.factory.rules[2].regex
        self.assertFalse(regex.match("http://vimeo.com"))
        self.assertFalse(regex.match("http://vemeo.com"))
        self.assertTrue(regex.match("http://vimeo.com/99681835"))
        self.assertFalse(regex.match("http://vimeo.com/channels/lautrec"))

    def test_instagram(self):
        regex = self.factory.rules[3].regex
        self.assertFalse(regex.match("http://instagram.com"))
        self.assertFalse(regex.match("http://instagr.am"))
        self.assertTrue(regex.match("http://instagram.com/p/iooF4VuGtp/"))
        self.assertTrue(regex.match("http://instagram.com/p/iooF4VuGtp"))
        self.assertFalse(regex.match("http://instagram.com/iooF4VuGtp/"))
