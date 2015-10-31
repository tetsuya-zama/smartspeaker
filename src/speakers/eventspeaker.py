# -*- coding: utf-8 -*-
from absspeaker import AbsSpeaker
from timezone import JST
import datetime

class EventSpeaker(AbsSpeaker):
    """EventSpeaker
    期間（日時）に基づいてoutputを選択するspeaker
    """
    #デバッグ用日時(datetime.datetime タイムゾーン付き)
    DEBUG_DATETIME = None
    #このspeakerで扱うタイムゾーン
    TIME_ZONE = JST()

    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        期間(日時)のfrom,toに基づいてoutputを選択する
        @setting
        {
         "speaker":"event",
         "conditions":[
          {
           "from":"${日時(from) YYYY/mm/dd HH:MM:SS}",
           "to":"${日時(from) YYYY/mm/dd HH:MM:SS}",
           "outputs":[
            ...
           ]
          },
          ...
         ]
        }
        """
        current_datetime = self._get_current_datetime()

        if "conditions" in setting:
            rtn = None
            for cond in setting["conditions"]:
                if "from" in cond and "to" in cond:
                    from_time = self._convert_datetime(cond["from"])
                    to_time = self._convert_datetime(cond["to"])

                    if from_time <= current_datetime and to_time > current_datetime :
                        rtn = cond
                else:
                    #fromとtoが指定されていないconditionをデフォルトとして扱う
                    if rtn == None:
                        rtn = cond

            return rtn
        else:
            return None

    def _get_current_datetime(self):
        """_get_current_datetime
        現在の時刻を取得する
        """
        if self.DEBUG_DATETIME != None:
            #DEBUG_DATETIMEが指定されていればそれを返す
            return self.DEBUG_DATETIME
        else:
            return datetime.datetime.now(self.TIME_ZONE)

    def _convert_datetime(self,val):
        """_convert_datetime
        設定値に指定された日時をdatetime.datetimeに変換する
        @param val 日時を表す文字列(YYYY/mm/dd HH:MM:SS)
        """
        dt = datetime.datetime.strptime(val,"%Y/%m/%d %H:%M:%S")
        dt = dt.replace(tzinfo=self.TIME_ZONE).astimezone(self.TIME_ZONE)
        return dt


def create():
    """create
    EventSpeakerのインスタンスを返す
    """
    return EventSpeaker()
