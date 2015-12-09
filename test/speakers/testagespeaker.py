# -*- coding: utf-8 -*-
import unittest
import json
from speakers import agespeaker

class TestAgeSpeaker(unittest.TestCase):
    """TestAgeSpeaker
    AgeSpeakerのunittestケース
    """

    def test_create(self):
        """test_create
        create関数でAgeSpeakerのインスタンスを取得するテスト
        """
        speaker = agespeaker.create()
        self.assertIsInstance(speaker,agespeaker.AgeSpeaker)

    def test_single_condition(self):
        """test_single_condition
        1つだけ設定したconditionにマッチして正しいものを返すテスト
        """
        speaker = agespeaker.create()

        setting_json = """{
         "speaker":"age",
         "conditions":[{
          "age":{
           "gt":60
          },
          "outputs":[
           {"serif":"かっこいい歳の取り方ですね!"}
          ]
         }]
        }"""

        result = speaker.speak({"age":62},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"かっこいい歳の取り方ですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        複数のconditionからマッチしたものを正しく返すテスト
        """
        speaker = agespeaker.create()

        setting_json = """{
         "speaker":"age",
         "conditions":[
         {
          "age":{
           "gt":60
          },
          "outputs":[
           {"serif":"かっこいい歳の取り方ですね!"}
          ]
         },
         {
          "age":{
           "lt":20
          },
          "outputs":[
           {"serif":"お若いですね!"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"age":19},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"お若いですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_match(self):
        """test_not_match
        conditionに１つもマッチしないケースのテスト
        """
        speaker = agespeaker.create()

        setting_json = """{
         "speaker":"age",
         "conditions":[
         {
          "age":{
           "gt":60
          },
          "outputs":[
           {"serif":"かっこいい歳の取り方ですね!"}
          ]
         },
         {
          "age":{
           "lt":20
          },
          "outputs":[
           {"serif":"お若いですね!"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"age":21},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),0)

    def test_else_match(self):
        """test_else_match
        条件を指定しないデフォルトにマッチするテスト
        """
        speaker = agespeaker.create()

        setting_json = """{
         "speaker":"age",
         "conditions":[
         {
          "age":{
           "gt":60
          },
          "outputs":[
           {"serif":"かっこいい歳の取り方ですね!"}
          ]
         },
         {
          "age":{
           "lt":20
          },
          "outputs":[
           {"serif":"お若いですね!"}
          ]
         },
         {
          "outputs":[
           {"serif":"現役バリバリですね!"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"age":59},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"現役バリバリですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)
