# -*- coding: utf-8 -*-
from absspeaker import AbsSpeaker

class EmotionSpeaker(AbsSpeaker):
    """EmotionSpeaker
    Pepperの感情値（0.0~1.0）を元にoutputを決めるSpeaker
    """
    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        感情値を元にoutputsを選択する
        @setting
        {
         "speaker":"emotion",
         "conditions":[
          {
           "emotion":{
            "gt":${nより高い},
            "lt":${nより低い}
           },
           "outputs":[
            ...,
           ]
          }
         ]
        }
        """
        if "emotion" in inputs :
            if "conditions" in setting :
                rtn = None
                for cond in setting["conditions"]:
                    if "emotion" in cond:
                        if self._is_condition_match(cond,inputs["emotion"]) :
                            rtn = cond
                    else:
                        if rtn == None:
                            rtn = cond
                return rtn
            else:
                return None
        else :
            return None

    def _is_condition_match(self,cond,emotion):
        """_is_condition_match
        単一のconditionがemotionの入力値にマッチするか判定する
        @param cond 単一のcondition
        @param emotion 入力値のemotion
        """
        if not isinstance(emotion,float) :
            emotion = float(emotion)

        rtn = True
        if "emotion" in cond:
            if "gt" in cond["emotion"]:
                if not isinstance(cond["emotion"]["gt"],float):
                    cond["emotion"]["gt"] = float(cond["emotion"]["gt"])
                rtn = rtn and emotion > cond["emotion"]["gt"]
            if "lt" in cond["emotion"]:
                if not isinstance(cond["emotion"]["lt"],float):
                    cond["emotion"]["lt"] = float(cond["emotion"]["lt"])
                rtn = rtn and emotion < cond["emotion"]["lt"]

        return rtn


def create():
    """create
    EmotionSpeakerのインスタンスを返す
    """
    return EmotionSpeaker()
