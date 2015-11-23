# -*- coding: utf-8 -*-
import unittest
import json
from speakers import emotionspeaker

class TestEmotionSpeaker(unittest.TestCase):
    def test_create(self):
        """test_create
        create関数でEmotionSpeakerのインスタンスを取得する
        """
        speaker = emotionspeaker.create()
        self.assertIsInstance(speaker,emotionspeaker.EmotionSpeaker)

    def test_single_condition(self):
        """test_single_condition
        1つだけ設定したconditionにマッチして正しいものを返すテスト
        """
        speaker = emotionspeaker.create()

        setting_json = """{
         "speaker":"emotion",
         "conditions":[{
          "emotion":{
           "gt":0.7
          },
          "outputs":[
           {"serif":"今日は元気そうですね!"}
          ]
         }]
        }"""

        result = speaker.speak({"emotion":0.8},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"今日は元気そうですね!",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        複数のconditionからマッチしたものを正しく返すテスト
        """
        speaker = emotionspeaker.create()

        setting_json = """{
         "speaker":"emotion",
         "conditions":[
         {
          "emotion":{
           "gt":0.7
          },
          "outputs":[
           {"serif":"今日は元気そうですね!"}
          ]
         },
         {
          "emotion":{
           "lt":0.3
          },
          "outputs":[
           {"serif":"今日は元気無いですね。"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"emotion":0.2},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"今日は元気無いですね。",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_match(self):
        """test_not_match
        conditionに１つもマッチしないケースのテスト
        """
        speaker = emotionspeaker.create()

        setting_json = """{
         "speaker":"emotion",
         "conditions":[
         {
          "emotion":{
           "gt":0.7
          },
          "outputs":[
           {"serif":"今日は元気そうですね!"}
          ]
         },
         {
          "emotion":{
           "lt":0.3
          },
          "outputs":[
           {"serif":"今日は元気無いですね。"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"emotion":0.4},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),0)

    def test_else_match(self):
        """test_else_match
        条件を指定しないデフォルトにマッチするテスト
        """
        speaker = emotionspeaker.create()

        setting_json = """{
         "speaker":"emotion",
         "conditions":[
         {
          "emotion":{
           "gt":0.7
          },
          "outputs":[
           {"serif":"今日は元気そうですね!"}
          ]
         },
         {
          "emotion":{
           "lt":0.3
          },
          "outputs":[
           {"serif":"今日は元気無いですね。"}
          ]
         },
         {
          "outputs":[
           {"serif":"いつも通りですね。"}
          ]
         }
         ]
        }"""

        result = speaker.speak({"emotion":0.4},json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"いつも通りですね。",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)
