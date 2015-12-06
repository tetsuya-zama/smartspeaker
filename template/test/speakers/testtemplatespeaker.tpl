# -*- coding: utf-8 -*-
import unittest
import json
from speakers import ${PKG_NAME}

class Test${CLASS_NAME}(unittest.TestCase):
    """Test${CLASS_NAME}
    ${CLASS_NAME}のunittestケース
    """

    def test_create(self):
        """test_create
        create関数で${CLASS_NAME}のインスタンスを取得するテスト
        """
        speaker = ${PKG_NAME}.create()
        self.assertIsInstance(speaker,${PKG_NAME}.${CLASS_NAME})
