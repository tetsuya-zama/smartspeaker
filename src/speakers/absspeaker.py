# -*- coding: utf-8 -*-
from . import loader
import random

class AbsSpeaker:
    """AbsSpeaker
    speakerの抽象クラス
    speakers/xxxspeakerはこのクラスを継承すること
    """

    def __init__(self):
        """コンストラクタ
        #XXX 何か引数を渡せるようにするか検討中
        """
        pass

    def _next(self,inputs,condition,results):
        """_next
        appendもしくはappend_randomに定義された次のspeakerを実行する
        @param inputs SmartSpeakerからのinput
        @param condition 自身（の継承クラス）の設定値
        @results これまでの結果が格納された配列
        """
        if "append" in condition:
            #appendが配列の場合は先頭から順次実行する
            if isinstance(condition["append"],list):
                for append in condition["append"] :
                    results = self._append(inputs,append,results)

                return results
            else:
                return self._append(inputs,condition["append"],results)
        elif "append_random" in condition:
            #append_randomは配列の中からランダムでspeakerを実行する
            return self._append_random(inputs,condition["append_random"],results)
        else :
            return results

    def _append(self,inputs,setting,results):
        """_append
        appendされた次のspeakerを実行する
        @param inputs SmartSpeakerからのinput
        @param setting 次に実行するspeakerの設定値
        @param results これまでの結果が格納された配列
        """
        speaker = loader.load(setting["speaker"])
        if speaker != None:
            return speaker.speak(inputs,setting,results)
        else:
            return results

    def _append_random(self,inputs,settings,results):
        """_append_random
        append_randomに設定されたspeakerからランダムで選択して実行する
        @param inputs SmartSpeakerからのinput
        @param settings append_randomに設定されたspeakerの配列
        @param results これまでの結果が格納された配列
        """
        if len(settings) == 0:
            return results
        else:
            num = random.randint(0,len(settings) - 1)
            return self._append(inputs,settings[num],results)

    def speak(self,inputs,setting,results):
        """speak
        設定に基づいて結果をresultsに格納する
        @inputs SmartSpeakerからのinput
        @setting 自身（の継承クラス）の設定値
        @results これまでの結果が格納された配列
        """

        #_thinkでconditionsに設定されたconditionのうちどれか一つを選択する
        condition = self._think(inputs,setting)

        if condition != None:
            #選択したconditionにoutputsがあればその中からresultsに格納する
            if "outputs" in condition:
                output = self._choose_output(condition["outputs"])
                if output != None:
                    results.append(output)
            #次のspeakerを実行する
            return self._next(inputs,condition,results)
        else :
            #conditionが選択できなければここで終了
            return results

    def _think(self,inputs,setting):
        """_think
        設定値のconditionsの中からconditionを1つ選択する
        #継承クラスは基本的にこのメソッドをoverrideして実装する
        @param inputs SmartSpeakerからのinput
        @param setting 自身（の継承クラス）の設定ファイル
        """

        #下記の実装はあくまでサンプルであり、overrideされることを前提としている

        #conditionsの中から単に最初のものを返す
        if "conditions" in setting:
            return setting["conditions"][0]
        else:
            return None

    def _choose_output(self,outputs):
        """_choose_output
        outputsに設定されたoutputからランダムでoutputを返す
        @param outputs outputが格納された配列
        """
        if len(outputs) == 0:
            return None
        else:
            num = random.randint(0,len(outputs)-1)
            return outputs[num]
