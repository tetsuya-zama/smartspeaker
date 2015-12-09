# -*- coding: utf-8 -*-
from .absspeaker import AbsSpeaker

class GenderSpeaker(AbsSpeaker):
    """GenderSpeaker
    """
    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        inputのgender(0->女性、1->男性)によってoutputを決定する
        @setting
        {
         "speaker":"gender",
         "conditions":[
          {
           "gender":${0->女性,1->男性},
           "outputs":[
            ...
           ]
          },
          ...
         ]
        }
        """
        if "gender" in inputs :
            if "conditions" in setting :
                rtn = None
                for cond in setting["conditions"]:
                    if "gender" in cond:
                        if int(cond["gender"]) == int(inputs["gender"]) :
                            rtn = cond
                    else:
                        if rtn == None:
                            rtn = cond
                return rtn
            else:
                return None
        else :
            return None


def create():
    """create
    GenderSpeakerのインスタンスを返す
    """
    return GenderSpeaker()
