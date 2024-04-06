# ======================================================================
# Project Name    : Linebot 
# File Name       : main.py
# Encoding        : utf-8
# Creation Date   : 2021/02/18
# =======================================================================

from flask import Flask, request, abort
from dotenv import load_dotenv
load_dotenv()

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, ImageMessage, 
)
import os
import requests

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN =  os.getenv( "YOUR_CHANNEL_ACCESS_TOKEN")
YOUR_CHANNEL_SECRET =  os.getenv("YOUR_CHANNEL_SECRET")

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
headers = {'Authorization': 'Bearer ' + YOUR_CHANNEL_SECRET}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if "いぬ" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text + "わん"))
    elif "画像" in event.message.text:
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(original_content_url='https://example.com/original.jpg',preview_image_url='https://example.com/preview.jpg'))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    