# -*- coding: utf-8 -*-
import unittest
import json
import datetime
from speakers import eventspeaker
from speakers.timezone import JST

class TestEventSpeaker(unittest.TestCase):
    """TestEventSpeaker
    EventSpeakerのunittest
    """
    def test_create(self):
        """test_create
        create関数でEventSpeakerのインスタンスを取得する
        """
        speaker = eventspeaker.create()
        self.assertIsInstance(speaker,eventspeaker.EventSpeaker)

    def test_single_condition(self):
        """test_single_condition
        conditionsにひとつ設定されているsettingで正しい結果を返すテスト
        """
        eventspeaker.EventSpeaker.DEBUG_DATETIME = datetime.datetime(2016,1,1,8,0,0,tzinfo=JST())
        speaker = eventspeaker.create()

        setting_json="""{
         "speaker":"event",
         "conditions":[
          {
           "from":"2016/01/01 00:00:00",
           "to":"2016/01/03 23:59:59",
           "outputs":[
            {"serif":"あけましておめでとう"}
           ]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"あけましておめでとう",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_multi_condition(self):
        """test_multi_condition
        複数設定されているconditionsのうち正しいもの返すテスト
        """
        eventspeaker.EventSpeaker.DEBUG_DATETIME = datetime.datetime(2016,8,31,23,59,59,tzinfo=JST())
        speaker = eventspeaker.create()

        setting_json="""{
         "speaker":"event",
         "conditions":[
          {
           "from":"2016/01/01 00:00:00",
           "to":"2016/01/04 00:00:00",
           "outputs":[
            {"serif":"あけましておめでとう"}
           ]
          },
          {
           "from":"2016/08/01 00:00:00",
           "to":"2016/09/01 00:00:00",
           "outputs":[
            {"serif":"夏休み満喫してる？"}
           ]
          },
          {
           "from":"2016/12/01 00:00:00",
           "to":"2016/12/31 23:59:59",
           "outputs":[
            {"serif":"もうすぐ今年も終わりだね"}
           ]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"夏休み満喫してる？",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_else_match(self):
        """
        複数設定されているconsitionsのうちデフォルトのものを返すテスト
        """
        eventspeaker.EventSpeaker.DEBUG_DATETIME = datetime.datetime(2016,9,1,0,0,0,tzinfo=JST())
        speaker = eventspeaker.create()

        setting_json="""{
         "speaker":"event",
         "conditions":[
          {
           "from":"2016/01/01 00:00:00",
           "to":"2016/01/03 23:59:59",
           "outputs":[
            {"serif":"あけましておめでとう"}
           ]
          },
          {
           "from":"2016/08/01 00:00:00",
           "to":"2016/08/31 23:59:59",
           "outputs":[
            {"serif":"夏休み満喫してる？"}
           ]
          },
          {
           "from":"2016/12/01 00:00:00",
           "to":"2016/12/31 23:59:59",
           "outputs":[
            {"serif":"もうすぐ今年も終わりだね"}
           ]
          },
          {
           "outputs":[
            {"serif":"なんでも無い日常が幸せだよね"}
           ]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"なんでも無い日常が幸せだよね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_match(self):
        """test_not_match
        複数設定されているconditionsのうちひとつもマッチしないパターンのテスト
        """
        eventspeaker.EventSpeaker.DEBUG_DATETIME = datetime.datetime(2016,9,1,0,0,0,tzinfo=JST())
        speaker = eventspeaker.create()

        setting_json="""{
         "speaker":"event",
         "conditions":[
          {
           "from":"2016/01/01 00:00:00",
           "to":"2016/01/03 23:59:59",
           "outputs":[
            {"serif":"あけましておめでとう"}
           ]
          },
          {
           "from":"2016/08/01 00:00:00",
           "to":"2016/08/31 23:59:59",
           "outputs":[
            {"serif":"夏休み満喫してる？"}
           ]
          },
          {
           "from":"2016/12/01 00:00:00",
           "to":"2016/12/31 23:59:59",
           "outputs":[
            {"serif":"もうすぐ今年も終わりだね"}
           ]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])
        self.assertEqual(len(result),0)
