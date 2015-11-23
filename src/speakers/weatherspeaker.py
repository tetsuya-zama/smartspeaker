# -*- coding: utf-8 -*-
from absspeaker import AbsSpeaker
from timezone import JST
from urllib2 import Request, urlopen, URLError, HTTPError
import json

class WeatherSpeaker(AbsSpeaker):
    """WeatherSpeaker
    OpenWeatherMapの情報を元にoutputを決めるspeaker
    @see http://openweathermap.org/
    """

    #DEBUG用のOWMの結果
    DEBUG_OWM_RESULT = None

    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        OpenWeatherMapの現在の天気情報を元にoutputを返す
        @setting
        {
         "speaker":"weather",
         "owm_app_id":"${OWMのAPPID}",
         "owm_location_code":"${OWMのロケーションコード}",
         "conditions":[{
          "temp":{
           gt:${摂氏n度より高い},
           lt:${摂氏n度より低い}
          },
          "weather":[
            ${OWGの天気コード @see http://openweathermap.org/weather-conditions},
            ...
          ],
          "outputs":[
          ...
          ]
         }]
        }
        """

        if "owm_app_id" in setting and "owm_location_code" in setting:
            owm_result = self._get_owm(setting["owm_app_id"],setting["owm_location_code"])
            self._owm_location_code = setting["owm_location_code"]
        else:
            return None

        if "conditions" in setting and owm_result != None:
            rtn = None
            for cond in setting["conditions"]:
                if "temp" in cond or "weather" in cond :
                    if(self._is_condition_match(cond,owm_result)):
                        rtn = cond
                else:
                    if rtn == None:
                        rtn = cond

            return rtn
        else:
            return None

    def _get_owm(self,app_id,location_code):
        """_get_owm
        OpenWeatherMapから現在の天気情報を取得する
        @param app_id OWMのAPPID
        @prama location_code OWMの位置情報
        @tips locationコードの位置情報はOWMのトップページから地名を検索してWeather in your cityを表示し、
        http://openweathermap.org/city/xxxxxxx
        のxxxxxxxを設定する
        """

        if self.DEBUG_OWM_RESULT != None:
            return self.DEBUG_OWM_RESULT

        url = "http://api.openweathermap.org/data/2.5/weather?id=" + location_code + "&units=metric&APPID=" + app_id
        try:
            response = urlopen(url)
            return json.loads(response.read())
        except URLError as e:
            return None
        except HTTPError as e:
            return None

    def _is_condition_match(self,cond,owm_result):
        """_is_condition_match
        単一のconditionがOWMの結果にマッチするか判定する
        @param cond 単一のcondition
        @param owm_result OWMの結果
        """

        rtn = True

        if "temp" in cond:
            temp = cond["temp"]
            if "gt" in temp:
                rtn = rtn and temp["gt"] < owm_result["main"]["temp"]
            if "lt" in temp:
                rtn = rtn and temp["lt"] > owm_result["main"]["temp"]

        if "weather" in cond:
            rtn = rtn and owm_result["weather"][0]["id"] in cond["weather"]

        return rtn

    def _choose_output(self,outputs):
        """@override _choose_output
        AbsSpeakerで選択されたoutputにurlがなかった場合、
        OWMのWeather in your cityページのurlを付与する
        """
        result = AbsSpeaker._choose_output(self,outputs)

        if result != None:
            if not "url" in result:
                result["url"] = "http://openweathermap.org/city/" + self._owm_location_code

            return result
        else:
            return None


def create():
    """create
    WeatherSpeakerのインスタンスを返す
    """
    return WeatherSpeaker()
