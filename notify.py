from os import getenv
from dotenv import load_dotenv
import requests

def notify_dates(title, message_list):
    """send pushover notification
    title: (string) title of push notification
    message: (list) list of dates for message body
    """

    load_dotenv()
    user_key = getenv('USER_KEY')
    app_token = getenv('APP_TOKEN')

    url = 'https://api.pushover.net/1/messages.json'

    body = '\n'.join(message_list)

    pushover_request = {'token': app_token, 'user': user_key,
                'title': title, 'message': body}
    
    requests.post(url, data=pushover_request)
