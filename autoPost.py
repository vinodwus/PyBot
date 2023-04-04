import telegram
from telegram.ext import Updater, CommandHandler,ApplicationBuilder

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import openai
import os
import queue
from telegram import Bot, Update

# Set up credentials for the Blogger API
SCOPES = ['https://www.googleapis.com/auth/blogger']
SERVICE_ACCOUNT_FILE = 'path/to/service_account.json'

#creds = None
#creds = service_account.Credentials.from_service_account_file(
   #     "AIzaSyCak363LawHNfgQphqaQ3YCKrSbNJZCpjw", scopes=SCOPES)

# Set up credentials for the Blogger API
api_key = 'AIzaSyCak363LawHNfgQphqaQ3YCKrSbNJZCpjw'
service = build('blogger', 'v3', developerKey=api_key)

# Set up the Google Blogger API client
#service = build('blogger', 'v3', credentials=creds)

# Set up the Telegram bot
bot_token = '6295391205:AAFUPKaed4Joiott4P0UKUaZeve3IG6lcxM'
#bot = telegram.Bot(token=bot_token)
# create an update queue instance
#update_queue = queue.Queue()

# create an updater instance
# create a dispatcher instance
#dispatcher = Dispatcher(bot, update_queue)

# create an updater instance and pass the dispatcher
app = ApplicationBuilder().token(bot_token).build()
# = Bot(token=bot_token)

# Set up OpenAI API credentials
openai.api_key = "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"

# Define the command handler for the /post command
def post(update, context):
    # Get the user's input
    user_input = update.message.text
     # If user input is "/post", ask for the title
    
    


    # Generate the title, content, and labels for the blog post using Chat GPT
    prompt = f"Generate a blog post with the following prompt: {user_input}"
    response = openai.Completion.create(
    engine="davinci",
    prompt=prompt,
    temperature=0.7,
    max_tokens=2000,
    n=1,
    stop=None,
    timeout=60,
    )
    generated_text = response.choices[0].text
    generated_text_lines = generated_text.split('\n')
    title = generated_text_lines[0].strip()
    content = '\n'.join(generated_text_lines[1:]).strip()
    labels = generated_text_lines[-1].strip().split(',')

    # Create the blog post
    try:
        new_post = service.posts().insert(
            blogId='trendingfactsnews', body={
                'title': title,
                'content': content,
                'labels': labels
            }).execute()
        post_url = new_post['url']
    except HttpError as error:
        print('An error occurred: {}'.format(error))
        post_url = 'Error'

    # Send a message to the user with the link to the blog post
    update.message.reply_text('Your blog post has been created. You can view it at {}'.format(post_url))

# Start the bot
#updater = Updater(token=bot_token, use_context=True)

# create an updater instance
app.add_handler(CommandHandler('post', post))

app.run_polling()