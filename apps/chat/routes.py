
from apps.home import blueprint
from flask import render_template, request, Response, jsonify,session
from flask_login import login_required
from jinja2 import TemplateNotFound
import os
from apps.chat import blueprint
from apps.authentication.forms import LoginForm
import requests
import openai
import boto3

def get_fine_tune_data():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.File.create(
    file=open("mydata.jsonl", "rb"),
    purpose='fine-tune'
)
    return response['id']
def fine_tune():
    file = get_fine_tune_data()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    fine_tuned_model = openai.FineTune.create(training_file=file)
    return fine_tuned_model['id']

@blueprint.route('/send-message-emoji', methods=['POST'])
@login_required
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
@blueprint.route('/send-message', methods=['POST'])
@login_required
def send_message():
    # Get the user's message from the request body
    message = request.get_json()['message']
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Austin A.I is a chat bot that responds sarcastically to questions. Here is a question for Austin A.I"+message,
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

@blueprint.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    username = session.get('username')
    return render_template('chat/chat.html', username=username)
                            
@blueprint.route('/emoji-chat', methods=['GET', 'POST'])
@login_required
def chatemoji():
    username = session.get('username')
    return render_template('chat/chat.html', username=username)

@blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    username = session.get('username')
    client = boto3.client('cognito-idp',region_name='us-east-1', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    response = client.list_users_in_group(
        UserPoolId=os.getenv('COGNITO_USER_POOL_ID'),
        GroupName="Admin"
    )
    users = response['Users']
    for user in users:
        if user['Username'] == username:
            print("User Authorized")
            return render_template('admin-dash/dashboard.html', username=username)
        else:
            return render_template('home/page-403.html'), 403
@login_required
def profile():
    username = session.get('username')
    return render_template('home/profile.html', username=username)