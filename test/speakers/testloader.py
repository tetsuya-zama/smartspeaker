# -*- coding: utf-8 -*-
import unittest
import speakers
from speakers import loader

class TestLoaderModule(unittest.TestCase):
    """TestLoaderModule
    speakerのloaderのunittest
    """
    def test_conversation(self):
        """test_conversation
        ConversationSpeakerをロードするテスト
        """
        speaker = loader.load("conversation")
        self.assertIsInstance(speaker,speakers.conversationspeaker.ConversationSpeaker)

    def test_time(self):
        """test_time
        TimeSpeakerをロードするテスト
        """
        speaker = loader.load("time")
        self.assertIsInstance(speaker,speakers.timespeaker.TimeSpeaker)

    def test_event(self):
        """test_event
        EventSpeakerをロードするテスト
        """
        speaker = loader.load("event")
        self.assertIsInstance(speaker,speakers.eventspeaker.EventSpeaker)
