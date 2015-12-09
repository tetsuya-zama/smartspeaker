# -*- coding: utf-8 -*-
import unittest
import json
from speakers import genderspeaker

class TestGenderSpeaker(unittest.TestCase):
    """TestGenderSpeaker
    GenderSpeakerのunittestケース
    """

    def test_create(self):
        """test_create
        create関数でGenderSpeakerのインスタンスを取得するテスト
        """
        speaker = genderspeaker.create()
        self.assertIsInstance(speaker,genderspeaker.GenderSpeaker)

    def test_single_condition(self):
        """test_single_condition
        1つだけ設定したconditionにマッチして正しいものを返すテスト
        """
        speaker = genderspeaker.create()

        setting_json = """{
         "speaker":"gender",
         "conditions":[{
          "gender":1,
          "outputs":[
           {"serif":"イケメンですね!"}
          ]
         }]
        }"""

        result = speaker.speak({"gender":1},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"イケメンですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        複数のconditionからマッチしたものを正しく返すテスト
        """
        speaker = genderspeaker.create()

        setting_json = """{
         "speaker":"gender",
         "conditions":[
         {
          "gender":1,
          "outputs":[
           {"serif":"男前ですね!"}
          ]
         },
         {
          "gender":0,
          "outputs":[
           {"serif":"美人さんですね!"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"gender":0},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"美人さんですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_match(self):
        """test_not_match
        conditionに１つもマッチしないケースのテスト
        """
        speaker = genderspeaker.create()

        setting_json = """{
         "speaker":"gender",
         "conditions":[{
          "gender":1,
          "outputs":[
           {"serif":"イケメンですね!"}
          ]
         }]
        }"""

        result = speaker.speak({"gender":0},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),0)
