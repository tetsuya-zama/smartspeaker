# -*- coding: utf-8 -*-
import unittest
import json
from speakers import conversationspeaker

class TestConversationSpeaker(unittest.TestCase):
    """TestConversationSpeaker
    ConversationSpeakerのunittestケース
    """

    def test_create(self):
        """test_create
        create関数でConversationSpeakerのインスタンスを取得するテスト
        """
        speaker = conversationspeaker.create()
        self.assertIsInstance(speaker,conversationspeaker.ConversationSpeaker)

    def test_single_condition(self):
        """test_single_condition
        conditionsが一つだけ設定されたsettingで正しい結果を返すテスト
        """

        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[{
         "word":"おはよう",
         "outputs":[{"serif":"おはようございます"}]
        }]
        }"""

        result = speaker.speak([u"おはよう"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"おはようございます",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        conditionsが複数設定されたsettingで正しい結果を返すテスト
        """
        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[
        {
         "word":"おはよう",
         "outputs":[{"serif":"おはようございます"}]
        },
        {
         "word":"バイバイ",
         "outputs":[{"serif":"お疲れ様です"}]
        }
        ]
        }"""

        result = speaker.speak([u"バイバイ"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"お疲れ様です",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_no_condition_match(self):
        """test_no_condition_match
        conditionsが複数されているが、ひとつもマッチしないパターンのテスト
        """
        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[
        {
         "word":"おはよう",
         "outputs":[{"serif":"おはようございます"}]
        },
        {
         "word":"バイバイ",
         "outputs":[{"serif":"お疲れ様です"}]
        }
        ]
        }"""

        result = speaker.speak([u"こんばんわ"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),0)

    def test_else_match(self):
        """test_else_match
        複数設定されたconditionsのうち、デフォルトのものを返すテスト
        """
        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[
        {
         "word":"おはよう",
         "outputs":[{"serif":"おはようございます"}]
        },
        {
         "word":"バイバイ",
         "outputs":[{"serif":"お疲れ様でした"}]
        },
        {
        "outputs":[{"serif":"お仕事頑張ってますね"}]
        }
        ]
        }"""

        result = speaker.speak([u"こんばんわ"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"お仕事頑張ってますね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_no_output(self):
        """test_no_output
        outputsが0個でもエラーにならないテスト
        """
        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[{
         "word":"おはよう",
         "outputs":[]
        }]
        }"""

        result = speaker.speak([u"おはよう"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),0)

        print json.dumps(result,ensure_ascii=False)

    def test_random_outputs(self):
        """test_random_outputs
        outputsに複数指定されている場合、その中からランダムで選択するテスト
        """
        speaker = conversationspeaker.create()

        setting_json = """{
        "speaker" : "conversation",
        "conditions":[{
         "word":"おはよう",
         "outputs":[{"serif":"おはようございます"},{"serif":"グッドモーニング"}]
        }]
        }"""

        result = speaker.speak([u"おはよう"],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertTrue(u"おはようございます" == result[0]["serif"] or u"グッドモーニング" == result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)
