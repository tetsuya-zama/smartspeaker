# -*- coding: utf-8 -*-
from speakers import loader
import json
import os
import sys

class SmartSpeaker:
    """SmartSpeaker
    settingの内容に基づいてspeakers/xxxspeakerを実行し、
    結果を合算して返すメインクラス
    """

    def __init__(self,setting):
        """コンストラクタ
        @param 設定ファイル(json)をロードしたdict
        """
        self._setting = setting

    def speak(self,inputs):
        """speak
        設定に基づいてspeakers/xxxspeakerを実行する
        @param args 話しかける言葉 もしくは [話しかける言葉]
        #XXX argsの定義は現在仮決め
        """

        if not isinstance(self._setting,list):
            speakers = [self._setting]
        else:
            speakers = self._setting

        results = []

        #設定値が配列であれば、その中のspeakerを順次実行して結果を返す
        for current in speakers:
            speaker = loader.load(current["speaker"])
            results = speaker.speak(inputs,current,results)

        return results

def create(setting_file_path = None):
    """create
    SmartSpeakerのインスタンスを返す
    @param setting_file_path 設定ファイルのパス
    """

    if setting_file_path == None:
        if __name__ == '__main__':
            setting_file_path = "setting.json"
        else:
            setting_file_path = os.path.dirname(__file__) + "/setting.json"

    with open(setting_file_path) as f:
        setting = json.load(f,"utf-8")

    return SmartSpeaker(setting)

if __name__ == '__main__':
    args = sys.argv[1:]

    inputs = {}

    for i in range(0,len(args) - 1) :
        if args[i].startswith("-") :
            if args[i+1]:
                inputs[args[i].lstrip("-")] = args[i+1]

    print inputs;

    speaker = create()
    result = speaker.speak(inputs)

    print json.dumps(result,ensure_ascii=False)
