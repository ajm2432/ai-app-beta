from apps.home import blueprint
from flask import request, jsonify
import os
from apps.chat import blueprint
from openai import AsyncOpenAI
from openai import OpenAI

# Initialize the AsyncOpenAI client with the API key
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Corrected to use parentheses for getenv
)

@blueprint.route('/send-message-emoji', methods=['POST'])
async def send_message_emoji():
    message = request.get_json()['message']
    
    # Create the chat completion using the async client
    completion = await client.chat.completions.create(
        model="gpt-4-turbo",  # or "gpt-4" based on your needs
        messages=[
            {"role": "system", "content": "You are an AI IT Support Assistant.ask for their issue, provide troubleshooting steps, and if unresolved after a few attempts, inform them you'll escalate to the helpdesk for further assistance."},
            {"role": "user", "content": message}
        ],
        temperature=0.07,
        max_tokens=2560,  # Adjust based on response length needs
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # Extract the response content using the method
    bot_response = completion.choices[0].message.content
        
    return jsonify(response=bot_response)