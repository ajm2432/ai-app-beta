
from apps.home import blueprint
from flask import render_template, request, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
import os
from apps.chat import blueprint
from apps.chat.forms import ChatForm
import openai
import json

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
    
@blueprint.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    chat_form = ChatForm(request.form)
    if 'chat' in request.form:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Austin A.I is a chat bot that responds sarcastically to questions. Here is a question for Austin A.I"+request.form["chat"],
        temperature=0.07,
        max_tokens=2560,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        if response:
            response = response['choices'][0]['text']
            print(response)
            return render_template('chat/chat.html',
                            msg=response,
                            success=True,
                            form=chat_form)
                            
    return render_template('chat/chat.html', form=chat_form)
@blueprint.route('/emoji-chat', methods=['GET', 'POST'])
@login_required
def chatemoji():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    chat_form = ChatForm(request.form)
    if 'chat' in request.form:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Austin A.I is a bot that will respond to any request with a mix of emojis and words. Here is a request for Austin A.I ,"+request.form["chat"],
        temperature=0.07,
        max_tokens=2560,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
        if response:
            response = response['choices'][0]['text']
            print(response)
            return render_template('chat/chat.html',
                            msg=response,
                            success=True,
                            form=chat_form)
                            
    return render_template('chat/chat.html', form=chat_form)