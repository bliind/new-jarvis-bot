import os
import json
import requests

token = os.environ.get('BOT_TOKEN')

# make a call to the API
def call(endpoint, method='GET', options={}):
    if 'headers' not in options: options['headers'] = {}
    options['headers']['Authorization'] = f'Bot {token}'

    url = f'https://discord.com/api/v10{endpoint}'
    res = requests.request(method, url, **options)

    return json.loads(res.text)

# get a list of automod rules
def get_automod_rules(guild: int, ):
    return call(f'/guilds/{guild}/auto-moderation/rules')

# get a specific automod rule
def get_automod_rule(guild: int, id: int):
    return call(f'/guilds/{guild}/auto-moderation/rules/{id}')

# update an automod rule
def update_automod_rule(guild: int, id: int, params={}):
    return call(
        f'/guilds/{guild}/auto-moderation/rules/{id}',
        'PATCH',
        options={
            "headers": {"Content-Type": "application/json"},
            "data": json.dumps(params)
        }
    )
