# -*- coding: utf-8 -*-
import unittest
import json
import datetime
from speakers import timespeaker
from speakers.timezone import JST

class TestTimeSpeaker(unittest.TestCase):
    """TestTimeSpeaker
    TimeSpeakerのunittest
    """
    def test_create(self):
        """test_create
        create関数からTimeSpeakerを取得するテスト
        """
        speaker = timespeaker.create()
        self.assertIsInstance(speaker,timespeaker.TimeSpeaker)

    def test_single_condition(self):
        """test_single_condition
        conditionsにひとつだけ設定されたsettingから正しい結果を返すテスト
        """
        timespeaker.TimeSpeaker.DEBUG_TIME = datetime.time(6,0,0)
        speaker = timespeaker.create()

        setting_json="""{
        "speaker":"time",
        "conditions":[
         {
            "from":"06:00",
            "to":"11:00",
            "outputs":[
                {"serif":"おはようございます"}
            ]
         }
        ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"おはようございます",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        conditionsに複数指定されているsettingから正しいものを返すテスト
        """
        timespeaker.TimeSpeaker.DEBUG_TIME = datetime.time(17,29,0)
        speaker = timespeaker.create()

        setting_json="""{
        "speaker":"time",
        "conditions":[
         {
            "from":"06:00",
            "to":"11:00",
            "outputs":[
                {"serif":"おはようございます"}
            ]
         },
         {
            "from":"11:00",
            "to":"17:30",
            "outputs":[
                {"serif":"お疲れ様です"}
            ]
         },
         {
            "from":"17:30",
            "to":"22:00",
            "outputs":[
                {"serif":"遅くまでお疲れ様です"}
            ]
         }
        ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"お疲れ様です",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_match_else(self):
        """test_match_else
        複数設定されたconditionsのうち、デフォルトのものを返すパターンのテスト
        """
        timespeaker.TimeSpeaker.DEBUG_TIME = datetime.time(0,0,0)
        speaker = timespeaker.create()

        setting_json="""{
        "speaker":"time",
        "conditions":[
         {
            "from":"06:00",
            "to":"11:00",
            "outputs":[
                {"serif":"おはようございます"}
            ]
         },
         {
            "from":"11:00",
            "to":"17:30",
            "outputs":[
                {"serif":"お疲れ様です"}
            ]
         },
         {
            "from":"17:30",
            "to":"22:00",
            "outputs":[
                {"serif":"遅くまでお疲れ様です"}
            ]
         },
         {
            "outputs":[
                {"serif":"こんな時間にどうしたんですか？"}
            ]
         }
        ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"こんな時間にどうしたんですか？",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_match(self):
        """
        conditionsにひとつもマッチしないパターンのテスト
        """
        timespeaker.TimeSpeaker.DEBUG_TIME = datetime.time(0,0,0)
        speaker = timespeaker.create()

        setting_json="""{
        "speaker":"time",
        "conditions":[
         {
            "from":"06:00",
            "to":"11:00",
            "outputs":[
                {"serif":"おはようございます"}
            ]
         }
        ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),0)

        print json.dumps(result,ensure_ascii=False)
