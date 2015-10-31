# -*- coding: utf-8 -*-
import unittest
import json
from speakers import weatherspeaker

class TestWeatherSpeaker(unittest.TestCase):
    def test_create(self):
        """test_create
        create関数からWeatherSpeakerを取得するテスト
        """
        speaker = weatherspeaker.create()
        self.assertIsInstance(speaker,weatherspeaker.WeatherSpeaker)

    def test_api_temp(self):
        """test_api
        DEBUG_OWM_RESULTを使用せずにAPIとの疎通してtempの挙動を見るテスト
        """

        speaker = weatherspeaker.create()

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "temp":{
            "gt":30
           },
           "outputs":[{"serif":"暑いですね"}]
          },
          {
           "temp":{
            "lt":30,
            "gt":15
           },
           "outputs":[{"serif":"涼しいですね"}]
          },
          {
           "temp":{
            "lt":15
           },
           "outputs":[{"serif":"寒いですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertTrue(u"暑いですね" == result[0]["serif"] or u"涼しいですね" == result[0]["serif"] or u"寒いですね" == result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_api_weather(self):
        """test_api
        DEBUG_OWM_RESULTを使用せずにAPIとの疎通してweatherの挙動を見るテスト
        """

        speaker = weatherspeaker.create()

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "weather":[500,501,502,503,504,511,520,521,522,531],
           "outputs":[{"serif":"雨ですね"}]
          },
          {
           "weather":[800],
           "outputs":[{"serif":"晴れてますね"}]
          },
          {
           "weather":[801,802,803,804],
           "outputs":[{"serif":"曇ってますね"}]
          },
          {
           "outputs":[{"serif":"特殊ですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertTrue(u"雨ですね" == result[0]["serif"] or u"晴れてますね" == result[0]["serif"] or u"曇ってますね" == result[0]["serif"] or u"特殊ですね" == result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_temp_gt(self):
        """test_temp_gt
        tempのgtが正しく動作するかテストする
        """

        speaker = weatherspeaker.create()

        debug_respose = """{
         "weather":[{"id":803}],
         "main":{"temp":30.1}
        }"""

        weatherspeaker.WeatherSpeaker.DEBUG_OWM_RESULT = json.loads(debug_respose)

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "temp":{
            "gt":30
           },
           "outputs":[{"serif":"暑いですね"}]
          },
          {
           "temp":{
            "lt":30,
            "gt":15
           },
           "outputs":[{"serif":"涼しいですね"}]
          },
          {
           "temp":{
            "lt":15
           },
           "outputs":[{"serif":"寒いですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"暑いですね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_temp_lt(self):
        """test_temp_lt
        tempのltが正しく動作するかテスト
        """

        speaker = weatherspeaker.create()

        debug_respose = """{
         "weather":[{"id":803}],
         "main":{"temp":14.9}
        }"""

        weatherspeaker.WeatherSpeaker.DEBUG_OWM_RESULT = json.loads(debug_respose)

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "temp":{
            "lt":15
           },
           "outputs":[{"serif":"寒いですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"寒いですね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_temp_not_match(self):
        """test_temp_not_match
        tempの設定にマッチしない場合、何も返さないことをテスト
        """

        speaker = weatherspeaker.create()

        debug_respose = """{
         "weather":[{"id":803}],
         "main":{"temp":29.9}
        }"""

        weatherspeaker.WeatherSpeaker.DEBUG_OWM_RESULT = json.loads(debug_respose)

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "temp":{
            "gt":30
           },
           "outputs":[{"serif":"暑いですね"}]
          },
          {
           "temp":{
            "lt":15
           },
           "outputs":[{"serif":"寒いですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),0)

    def test_weather_match(self):
        """test_weather_match
        weatherに正しくマッチすることをテスト
        """

        speaker = weatherspeaker.create()

        debug_respose = """{
         "weather":[{"id":803}],
         "main":{"temp":29.9}
        }"""

        weatherspeaker.WeatherSpeaker.DEBUG_OWM_RESULT = json.loads(debug_respose)

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "weather":[500,501,502,503,504,511,520,521,522,531],
           "outputs":[{"serif":"雨ですね"}]
          },
          {
           "weather":[800],
           "outputs":[{"serif":"晴れてますね"}]
          },
          {
           "weather":[801,802,803,804],
           "outputs":[{"serif":"曇ってますね"}]
          },
          {
           "outputs":[{"serif":"特殊ですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"曇ってますね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_complex(self):
        """test_complex
        tempとweatherの複合条件にマッチすることをテスト
        """

        speaker = weatherspeaker.create()

        debug_respose = """{
         "weather":[{"id":803}],
         "main":{"temp":30.1}
        }"""

        weatherspeaker.WeatherSpeaker.DEBUG_OWM_RESULT = json.loads(debug_respose)

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "weather":[500,501,502,503,504,511,520,521,522,531],
           "outputs":[{"serif":"雨ですね"}]
          },
          {
           "weather":[800],
           "outputs":[{"serif":"晴れてますね"}]
          },
          {
           "weather":[801,802,803,804],
           "outputs":[{"serif":"曇ってますね"}]
          },
          {
           "weather":[801,802,803,804],
           "temp":{"gt":30},
           "outputs":[{"serif":"曇ってて暑いですね"}]
          },
          {
           "outputs":[{"serif":"特殊ですね"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"曇ってて暑いですね",result[0]["serif"])

        print json.dumps(result,ensure_ascii=False)

    def test_add_url(self):
        """test_add_url
        outputにurlが指定されていない場合、OWMのURLを付加する
        """
        speaker = weatherspeaker.create()

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "outputs":[{"serif":"今日の天気です"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"今日の天気です",result[0]["serif"])
        self.assertTrue("url" in result[0])
        self.assertEqual(u"http://openweathermap.org/city/1848354",result[0]["url"])

        print json.dumps(result,ensure_ascii=False)

    def test_not_override_url(self):
        """test_not_override_url
        outputにurlが明示的に指定されていれば、それを上書きしない
        """

        speaker = weatherspeaker.create()

        setting_json="""{
         "speaker":"weather",
         "owm_app_id":"7cd63966189e7e20afd65233f5dca42f",
         "owm_location_code":"1848354",
         "conditions":[
          {
           "outputs":[{"serif":"今日の天気です","url":"http://weather.yahoo.co.jp/weather/14/4610.html"}]
          }
         ]
        }"""

        result = speaker.speak([],json.loads(setting_json,"utf-8"),[])

        self.assertEqual(len(result),1)
        self.assertTrue("serif" in result[0])
        self.assertEqual(u"今日の天気です",result[0]["serif"])
        self.assertTrue("url" in result[0])
        self.assertEqual(u"http://weather.yahoo.co.jp/weather/14/4610.html",result[0]["url"])

        print json.dumps(result,ensure_ascii=False)
