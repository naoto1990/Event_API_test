import os
import json
import urllib

from flask import Flask, request, Response, jsonify

OAuth_access_token = os.environ['OAuth_access_token']

def create_app(test_config=None):
    """
    appの生成と設定を行う
    """
    app = Flask(__name__, instance_relative_config=True)


    @app.route('/', methods=['POST'])
    def handle_slack_event():
        """
        Slack上でリッスンしているEventを受け取り、任意の処理を行う
        """
        if 'challenge' in request.json:
            verification_req = request.json

            return verification_req['challenge']

        event_info = request.json
        print(event_info)

        post_response(event_info['event']['item']['channel'])

        # TODO: returnがないとFlaskのTypeErrorが発生するが、returnする値がない場合どうすべきか確認
        return 'ok'


    def post_response(target_channel: str):
        """
        Reacjiのイベントが発火した際に、#generalチャネルにメッセージをポストする
        """
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": "Bearer {0}".format(OAuth_access_token)
        }

        method = 'POST'

        data = {
            "channel": target_channel,
            "text": 'Thanks!',
            "username": 'Bot-Sample'
        }

        json_data = json.dumps(data).encode("utf-8")

        req = urllib.request.Request(url=url, data=json_data, headers=headers, method=method)
        res = urllib.request.urlopen(req, timeout=5)

        print("Http status: {0} {1}".format(res.status, res.reason))
        print(res.read().decode("utf-8"))


    return app
