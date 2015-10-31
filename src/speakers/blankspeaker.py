# -*- coding: utf-8 -*-
from .absspeaker import AbsSpeaker

class BlankSpeaker(AbsSpeaker):
    """BlankSpeaker
    特にconditionを選択せず、確実にconditions[0]を返すSpeaker
    必ず出力したいoutputのプレースホルダーとしてや、
    append_randomのプーレスホルダーとして使用する
    """
    def __init__(self):
        """コンストラクタ
        """
        AbsSpeaker.__init__(self)

    def _think(self,inputs,setting):

        #conditionsの中から単に最初のものを返す
        if "conditions" in setting:
            return setting["conditions"][0]
        else:
            return None

def create():
    """create
    BlankSpeakerのインスタンスを返す
    """
    return BlankSpeaker()
