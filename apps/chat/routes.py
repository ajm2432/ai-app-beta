
from apps.home import blueprint
from flask import  request, jsonify,session
import os
from apps.chat import blueprint
import openai

@blueprint.route('/send-message-emoji', methods=['POST'])
def send_message_emoji():
        message = request.get_json()['message']
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Austin A.I is a bot that will respond to any request with a mix of emojis and words. Here is a request for Austin A.I ,"+message,
        temperature=0.07,
        max_tokens=2560,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        if response:
            bot_response = response['choices'][0]['text']
            print(response)
            # Return the bot's response as a JSON object
        return jsonify(response=bot_response)

