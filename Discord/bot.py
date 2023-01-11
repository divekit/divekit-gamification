import asyncio,os, requests, discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.environ["TOKEN"]
GUILD_ID = int(os.environ["GUILD_ID"])
API_BASE_URL = os.environ["API_BASE_URL"]
BOT_USERNAME = os.environ["BOT_USERNAME"]
BOT_PASSWORD = os.environ["BOT_PASSWORD"]

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def get_api_token(refresh_token):
    response = requests.post(API_BASE_URL+'/api/v1/token/refresh/',json={"refresh":refresh_token})

    access_token = response.json()["access"]
    refresh_token = response.json()["refresh"]

    return access_token,refresh_token

async def send_message(access_token,refresh_token):

    while True:
        access_token,refresh_token = get_api_token(refresh_token)
        headers = {"Authorization": "Bearer "+access_token}
        try:
            response = requests.get(API_BASE_URL+'/api/v1/bot/notifications/',headers=headers)
            
            print(response.json())
            responseJson = response.json()

            for member in client.get_guild(GUILD_ID).members:
                for notification in responseJson:
                    if str(member) == notification["owner"]:
                        await member.send(notification["message"])

        except Exception as e:
            print("ERROR",e.with_traceback())
        await asyncio.sleep(900)

@client.event
async def on_ready():
    try:
        response = requests.post(API_BASE_URL+'/api/v1/token/obtain/',json={"username":BOT_USERNAME,"password":BOT_PASSWORD})
        access_token = response.json()["access"]
        refresh_token = response.json()["refresh"]
        print('We have logged in as {0.user}'.format(client))
        client.loop.create_task(send_message(access_token,refresh_token))
    except Exception as e:
        print("ERROR",e)

client.run(TOKEN)