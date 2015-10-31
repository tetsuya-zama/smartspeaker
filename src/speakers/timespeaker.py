# -*- coding: utf-8 -*-
from absspeaker import AbsSpeaker
from timezone import JST
import datetime

class TimeSpeaker(AbsSpeaker):
    """TimeSpeaker
    現在時刻を元にoutputを決めるspeaker
    """
    #DEBUG用時刻 datetime.time
    DEBUG_TIME = None
    #このspeakerで扱うタイムゾーン
    TIME_ZONE = JST()

    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        現在時刻を元にoutputを選択する
        @setting
        {
         "speaker":"time",
         "conditions":[
         {
          "from":"時刻(HH:MM)",
          "to":"時刻(HH:MM)",
          "outputs":[
          ...
          ]
         },
         ...
         ]
        }
        """
        current_time = self._get_current_time()

        if "conditions" in setting:
            rtn = None
            for cond in setting["conditions"]:
                if "from" in cond and "to" in cond:
                    from_time = self._convert_time(cond["from"])
                    to_time = self._convert_time(cond["to"])

                    if from_time <= current_time and to_time > current_time :
                        rtn = cond
                else:
                    #fromとtoが設定されていないconditionをデフォルトとして扱う
                    if rtn == None:
                        rtn = cond

            return rtn
        else:
            return None

    def _get_current_time(self):
        """_get_current_time
        現在時刻を取得する
        """
        if self.DEBUG_TIME != None :
            #DEBUG_TIMEが指定されていればそれを返す
            return self.DEBUG_TIME
        else :
            return datetime.datetime.now(self.TIME_ZONE).time()

    def _convert_time(self, val):
        """_convert_time
        設定ファイルに記述された時刻をdatetime.timeに変換する
        @param val 時刻文字列(HH:MM)
        """
        hour_minutes = val.split(":")
        hour = hour_minutes[0]
        minutes = hour_minutes[1]

        return datetime.time(int(hour),int(minutes),0)

def create():
    """create
    TimeSpeakerのインスタンスを返す
    """
    return TimeSpeaker()
