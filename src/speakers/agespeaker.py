# -*- coding: utf-8 -*-
from .absspeaker import AbsSpeaker

class AgeSpeaker(AbsSpeaker):
    """AgeSpeaker
    """
    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        inputされたageが設定値の条件にあったoutputを返す
        @setting
        {
         "speaker":"age",
         "conditions":[
          {
           "age":{
            "gt":"${nより大きい}",
            "lt":"${nより小さい}"
           },
           "outputs":[
            ...
           ]
          },
          ...
         ]
        }
        """
        if "age" in inputs :
            if "conditions" in setting :
                rtn = None
                for cond in setting["conditions"]:
                    if "age" in cond:
                        if self._is_condition_match(cond,inputs["age"]) :
                            rtn = cond
                    else:
                        if rtn == None:
                            rtn = cond
                return rtn
            else:
                return None
        else :
            return None

    def _is_condition_match(self,cond,age):
        """_is_condition_match
        単一のconditionがageの入力値にマッチするか判定する
        @param cond 単一のcondition
        @param  入力値のage
        """
        if not isinstance(age,float) :
            age = float(age)

        rtn = True
        if "age" in cond:
            if "gt" in cond["age"]:
                if not isinstance(cond["age"]["gt"],float):
                    cond["age"]["gt"] = float(cond["age"]["gt"])
                rtn = rtn and age > cond["age"]["gt"]
            if "lt" in cond["age"]:
                if not isinstance(cond["age"]["lt"],float):
                    cond["age"]["lt"] = float(cond["age"]["lt"])
                rtn = rtn and age < cond["age"]["lt"]

        return rtn



def create():
    """create
    AgeSpeakerのインスタンスを返す
    """
    return AgeSpeaker()
