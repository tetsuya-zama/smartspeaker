# -*- coding: utf-8 -*-

def load(speaker_name):
    """load
    speakrs/xxxspeakerを動的にロードする
    @param speaker_name speaker名（xxxspeaker.pyのxxxにあたる部分）
    """
    module = __import__("speakers." + speaker_name + "speaker")
    module = getattr(module,speaker_name + "speaker")
    create = getattr(module,"create")

    return create()
