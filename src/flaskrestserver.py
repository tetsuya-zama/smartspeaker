# -*- coding: utf-8 -*-
import json
from flask import Flask, jsonify, request ,Response
import smartspeaker
from smartspeaker import SmartSpeaker
import sys

app = Flask(__name__)

@app.route('/speak', methods=['GET'])
def speak():
    speaker = smartspeaker.create()
    inputs = {}

    if request.args.get('word'):
        inputs['word'] = request.args.get('word')
    if request.args.get('emotion'):
        inputs['emotion'] = request.args.get('emotion')

    result = speaker.speak(inputs)

    return Response(response = json.dumps(result,ensure_ascii=False), status=200, mimetype = "application/json;charset=utf-8")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            app.debug = True
    app.run()
