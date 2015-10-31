# -*- coding: utf-8 -*-
import datetime

# 日本時間
class JST(datetime.tzinfo):
  """JST
  日本標準時(JST)を示すtzinfo
  """
  # UTCからの時間のずれ
  def utcoffset(self, dt):
    return datetime.timedelta(hours=9)
  # サマータイム
  def dst(self, dt):
    return datetime.timedelta(0)
  # タイムゾーンの名前
  def tzname(self, dt):
    return 'JST'
