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

    for k in request.args :
        inputs[k] = request.args.get(k)

    result = speaker.speak(inputs)

    return Response(response = json.dumps(result,ensure_ascii=False), status=200, mimetype = "application/json;charset=utf-8")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "debug":
            app.debug = True
    app.run()
