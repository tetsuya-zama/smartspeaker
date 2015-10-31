#Smart Speaker

##ファイル構成
- smartspeaker.py
 * main処理
		 * setting.jsonの内容に従ってspeakersをロードして結果を出力する
- setting.json
 * 設定ファイル
	  * speakersの構成や対応するセリフを設定する

- speakers/
 * absspeaker.py
	 * speakerの抽象クラス
 * conversationspeaker.py
	 * 入力されたセリフによって出力を変化させる
 * timespeaker.py
	 * 時刻によって出力を変化させる
 * wheatherspeaker.py
	 * 天気によって出力を変化させる
 * trainspeaker.py
	 * 鉄道の運行状況によって出力を変化させる
 * eventspeaker.py
	 * 設定された期間によって出力を変化させる

##実行
実行時には相手（ユーザー）からのセリフを引き渡す

###コマンドラインから実行
```shell
 $ python smartspeaker.py "おはよう"
```

###他のPythonスクリプトから実行
```python
# -*- coding: utf-8 -*-

import smartspeaker

speaker = smartspeaker.create()
result = speaker.speak("おはよう")
```

###設定
setting.jsonには各speakerごとの出力を入れ子構造で設定する。

```javascript
 {
    "speaker":"conversation",
    "conditions":[
		{
			"word":"おはよう",
			"outputs":[
				{
					"serif":"おはようございます。",
					"motion":"001"
				}
			]
			"append":{
				"speaker":"time"
				"conditions":[
					{
						"from":"03:00",
						"to":"06:00",
						"outputs":[
							{
								"serif":"ずいぶん早いご出社ですね。"
							}
						]
					},
					{
						"from":"12:00",
						"to":"24:00",
						"outputs":[
							{
								"serif":"なんだか業界人みたいですね。"
							}
						]
					}
				]			
			}
		}
		{
			"word":"バイバイ",
			"outputs":[
				{
					"serif":"お疲れさまでした。",
					"motion":"002"
				}
			]
		}
	]
 }
```

###出力
以下の3要素をjson(pythonから呼び出した場合はdict)で返す
1. serif
 * 必須
 * speakerから応答されたセリフ
2. motion
 * 任意（key自体が存在しないケースあり）
 * 動作させるモーションを表す連番または記号（詳細検討中）
3. url
 * 任意（key自体が存在しないケースあり）
 * 参照して欲しいURL

出力が複数ある場合は、出力順に返す。

出力例
```javascript
 [
	{"serif":"おはようございます。", "motion":"001"},
	{"seirf":"ずいぶん早いご出社ですね。"},
	{
	 "serif":"今日は1日晴れるみたいです。気分がいいですね。",
	 "motion":"002",
	 "url":"http://weather.yahoo.co.jp/weather/14/4610.html"
	}
 ]
```
