# -*- coding: utf-8 -*-
from .absspeaker import AbsSpeaker

class ConversationSpeaker(AbsSpeaker):
    """ConversationSpeaker
    inputされたwordからoutputを選ぶspeaker
    """
    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):
        """@override _think
        inputされた言葉とwordに設定した言葉が一致すればoutputを返す
        @setting
        {
         "speaker":"conversation",
         "conditions":[
          {
           "word":"${条件となる言葉}",
           "outputs":[
            ...
           ]
          },
          ...
         ]
        }
        """
        if "conditions" in setting:
            rtn = None
            for cond in setting["conditions"]:
                if "word" in cond:
                    if not isinstance(inputs[0],unicode):
                        inputs[0] = inputs[0].decode("utf-8")
                    if cond["word"] == inputs[0]:
                        rtn = cond
                else :
                    #wordが選択されていないconditionをデフォルトとして扱う
                    if rtn == None:
                        rtn = cond

            return rtn
        else:
            return None

def create():
    """create
    ConversationSpeakerのインスタンスを返す
    """
    return ConversationSpeaker()
