import discord
import requests
# from decouple import config
import os

# API_KEY = config('API_KEY')
# TOKEN = config('TOKEN')

TOKEN = os.environ.get('TOKEN')
API_KEY = os.environ.get('API_KEY')

client = discord.Client()

def get_aqi(city):
    
    url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"
    querystring = {"city":city}
    headers = {
        'x-rapidapi-host': "air-quality-by-api-ninjas.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()
    if "error" in data.keys():
        return "Couldn't find the place :("
    else:
        aqi = data['overall_aqi']
        return f"AQI in {city.upper()} is {aqi}"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$aqi'):
        aqi = get_aqi(message.content[5:])
        await message.channel.send("> "+aqi)

client.run(TOKEN)