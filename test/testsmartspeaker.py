# -*- coding: utf-8 -*-
import unittest
import json
import smartspeaker
import datetime
from smartspeaker import SmartSpeaker

class TestSmartSpeaker(unittest.TestCase):
    """TestSmartSpeaker
    SmartSpeakerのunitttest
    """
    def test_create(self):
        """test_create
        create関数からSmartSpeakerのインスタンスを取得するテスト
        """
        speaker = smartspeaker.create()
        self.assertIsInstance(speaker,SmartSpeaker)

    def test_single_speaker(self):
        """test_single_speaker
        speakerがひとつだけ設定されているパターンで設定されているspeakerを実行するテスト
        """
        setting_json="""{
         "speaker":"conversation",
         "conditions":[
           {
             "word":"おはよう",
             "outputs":[
               {"serif":"おはようございます"}
             ]
           }
         ]
        }"""

        speaker = SmartSpeaker(json.loads(setting_json,"utf-8"))

        results = speaker.speak({"word":u"おはよう"})

        self.assertEqual(len(results),1)
        self.assertEqual(u"おはようございます",results[0]["serif"])

        print json.dumps(results,ensure_ascii=False)

    def test_single_with_append(self):
        """test_single_with_append
        appendが設定されているspeakerを実行する
        """
        setting_json="""{
         "speaker":"conversation",
         "conditions":[
           {
             "word":"おはよう",
             "outputs":[
               {"serif":"おはようございます"}
             ],
             "append":{
              "speaker":"time",
              "conditions":[
               {
                "from":"12:00",
                "to":"23:59",
                "outputs":[
                 {"serif":"業界の方ですか？"}
                ]
               },
               {
                "outputs":[{"serif":"今何時だろう?"}]
               }
              ]
             }
           }
         ]
        }"""

        speaker = SmartSpeaker(json.loads(setting_json,"utf-8"))

        results = speaker.speak({"word":u"おはよう"})

        self.assertEqual(len(results),2)
        self.assertEqual(u"おはようございます",results[0]["serif"])
        self.assertTrue(u"業界の方ですか？" == results[1]["serif"] or u"今何時だろう?" == results[1]["serif"])

        print json.dumps(results,ensure_ascii=False)

    def test_single_with_multi_append(self):
        """test_single_with_multi_append
        appendが複数設定されたspeakerを実行する
        *appendが複数設定されている場合は、配列のはじめから順次実行する
        """
        setting_json="""{
         "speaker":"conversation",
         "conditions":[
           {
             "word":"おはよう",
             "outputs":[
               {"serif":"おはようございます"}
             ],
             "append":[
             {
              "speaker":"time",
              "conditions":[
               {
                "from":"12:00",
                "to":"23:59",
                "outputs":[
                 {"serif":"業界の方ですか？"}
                ]
               },
               {
                "outputs":[{"serif":"今何時だろう?"}]
               }
              ]
             },
             {
              "speaker":"time",
              "conditions":[
               {
                "from":"12:00",
                "to":"13:00",
                "outputs":[
                 {"serif":"お昼ご飯の時間ですね"}
                ]
               },
               {
                "outputs":[{"serif":"時計忘れちゃった"}]
               }
              ]
             }
             ]
           }
         ]
        }"""

        speaker = SmartSpeaker(json.loads(setting_json,"utf-8"))

        results = speaker.speak({"word":u"おはよう"})

        self.assertEqual(len(results),3)
        self.assertEqual(u"おはようございます",results[0]["serif"])
        self.assertTrue(u"業界の方ですか？" == results[1]["serif"] or u"今何時だろう?" == results[1]["serif"])
        self.assertTrue(u"お昼ご飯の時間ですね" == results[2]["serif"] or u"時計忘れちゃった" == results[2]["serif"])

        print json.dumps(results,ensure_ascii=False)

    def test_single_with_random_append(self):
        """test_single_with_random_append
        append_randomが指定されたspeakerを実行する
        *append_randomは指定されたもののうちひとつをランダムで実行する
        """
        setting_json="""{
         "speaker":"conversation",
         "conditions":[
           {
             "word":"おはよう",
             "outputs":[
               {"serif":"おはようございます"}
             ],
             "append_random":[
             {
              "speaker":"time",
              "conditions":[
               {
                "from":"12:00",
                "to":"23:59",
                "outputs":[
                 {"serif":"業界の方ですか？"}
                ]
               },
               {
                "outputs":[{"serif":"今何時だろう?"}]
               }
              ]
             },
             {
              "speaker":"time",
              "conditions":[
               {
                "from":"12:00",
                "to":"13:00",
                "outputs":[
                 {"serif":"お昼ご飯の時間ですね"}
                ]
               },
               {
                "outputs":[{"serif":"時計忘れちゃった"}]
               }
              ]
             }
             ]
           }
         ]
        }"""

        speaker = SmartSpeaker(json.loads(setting_json,"utf-8"))

        results = speaker.speak({"word":u"おはよう"})

        self.assertEqual(len(results),2)
        self.assertEqual(u"おはようございます",results[0]["serif"])
        self.assertTrue(u"業界の方ですか？" == results[1]["serif"] or u"今何時だろう?" == results[1]["serif"] or u"お昼ご飯の時間ですね" == results[1]["serif"] or u"時計忘れちゃった" == results[1]["serif"])

        print json.dumps(results,ensure_ascii=False)

    def test_mutil_speaker(self):
        """test_mutil_speaker
        配列で設定された複数のspeakerを実行する
        *配列で指定されたspeakerは配列のはじめから順次実行する
        """
        setting_json="""[
        {
         "speaker":"conversation",
         "conditions":[
           {
             "word":"おはよう",
             "outputs":[
               {"serif":"おはようございます"}
             ]
           }
         ]
        },
        {
         "speaker":"time",
         "conditions":[
         {
          "from":"12:00",
          "to":"13:00",
          "outputs":[
           {"serif":"お昼ご飯の時間ですね"}
          ]
         },
         {
          "outputs":[{"serif":"時計忘れちゃった"}]
         }
         ]
        }
        ]"""

        speaker = SmartSpeaker(json.loads(setting_json,"utf-8"))

        results = speaker.speak({"word":u"おはよう"})

        self.assertEqual(len(results),2)
        self.assertEqual(u"おはようございます",results[0]["serif"])
        self.assertTrue(u"お昼ご飯の時間ですね" == results[1]["serif"] or u"時計忘れちゃった" == results[1]["serif"])

        print json.dumps(results,ensure_ascii=False)
