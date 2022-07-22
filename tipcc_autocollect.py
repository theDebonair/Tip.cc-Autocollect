import asyncio
import json
import random
import aiohttp
import art
import discord
import os
from discord.ext import tasks
from time import sleep

channel = None

proxies = ["syd","tor","par","fra","lin","nrt","ams","waw","lis","sin","mad","sto","lon","iad","atl","chi","dal","den","lax","mia","nyc","sea","phx"]

air_count = 0

phase_count = 0

env_count = 0

os.system('cls' if os.name == 'nt' else 'clear')

print("\033[0;35m")
art.tprint("theDebonair", font="smslant")

with open("config.json", 'r') as f:
    config = json.load(f)

client = discord.Client()

if config["TOKEN"] == "":
    config["TOKEN"] = input("\nEnter your discord token\n-> ")
    with open("config.json", 'w') as f:
        json.dump(config, f)

if config["FIRST"] == "True":
    config["CPM"] = int(input("\nEnter your CPM (Characters Per Minute).\nThis is to make the Phrase Drop Collector more legit.\nA decent CPM would be 310. (Remember, the higher the faster)\n-> "))
    config["FIRST"] = "False"
    with open("config.json", 'w') as f:
        json.dump(config, f)
        
if config["id"] == 0:
    config["id"] = int(input("\nEnter your Main Account's ID.\n\nIf you are sniping from your Main Account, put your Main Account's ID.\n-> "))
    with open("config.json", 'w') as f:
        json.dump(config, f)
        
if config["channel_id"] == 0:
    config["channel_id"] = int(input("\nEnter the Channel ID where you want your Alt Account to tip your Main Account.\n(Remember, the tip.cc bot has to be in the server with this channel.)\nIf None, send \"1\".\n-> "))
    with open("config.json", 'w') as f:
        json.dump(config, f)

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(config["channel_id"])
    print(f"Logged in as {client.user.name}#{client.user.discriminator} ({client.user.id})")
    tipping.start()

@tasks.loop(minutes = 10.0)
async def tipping():
    await channel.send("$bals top")
    answer = await client.wait_for('message', check=lambda message: message.author.id == 617037497574359050 and message.embeds)
    pages = int(answer.embeds[0].author.name.split('/')[1].replace(')',''))
    page = 1

    for page in range(pages):
        button = answer.components[0].children[1]

        for crypto in answer.embeds[0].fields:
            if "Estimated total" in crypto.name:
                pass

            else:
                content = f"$tip <@{config['id']}> {crypto.value.split('**')[1].replace(',','')}"
                async with channel.typing():
                    await asyncio.sleep(len(content) / config["CPM"] * 60)
                await channel.send(content)

        if button.disabled:
            await answer.components[0].children[2].click()
            return

        await button.click()
        await asyncio.sleep(1)
        answer = await channel.fetch_message(answer.id)

@tipping.before_loop
async def before_tipping():
    print("\nWaiting for bot to be ready before tipping starts...\n\n")
    await client.wait_until_ready()

@client.event
async def on_message(message):
    global air_count, phase_count, env_count

    if message.author.id == 617037497574359050:
        if message.embeds:
            embed = message.embeds[0]

            try:
                if "ended" in embed.footer.text.lower() and "Trivia time - " not in embed.title:
                    return

                elif "An airdrop appears" in embed.title:
                    comp = message.components
                    comp = comp[0].children
                    button = comp[0]

                    if "Enter airdrop" in button.label:
                        sleep(random.uniform(1.0, 2.25))
                        await button.click()
                        air_count += 1
                        print(f"\nEntered Airdrop for {embed.description.split('**')[1]} {embed.description.split('**')[2].split(')')[0].replace(' (','')}.\nTotal Airdrop(s) entered: {air_count}\nSleeping...\n\n")
                        sleep(random.uniform(1.0, 60.0))
                
                elif "Phrase drop!" in embed.title:
                    content = embed.description.replace("\n", "").replace("**", "")
                    content = content.split("*")
                    
                    try:
                        content = content[1].replace("​", "").replace("\u200b", "")
                    
                    except IndexError:
                        pass
                    
                    else:
                        length = len(content) / config["CPM"] * 60
                        async with message.channel.typing():
                            await asyncio.sleep(length)
                        await message.channel.send(content)
                        phase_count += 1
                        print(f"\nEntered Phrasedrop for {embed.description.split('**')[1]} {embed.description.split('**')[2].split(')')[0].replace(' (','')}.\nTotal Phasedrop(s) entered: {phase_count}\nSleeping...\n\n")
                        sleep(random.uniform(1.0, 60.0))
                
                elif "appeared" in embed.title:
                    comp = message.components
                    comp = comp[0].children
                    button = comp[0]

                    if "envelope" in button.label:
                        sleep(random.uniform(0.25, 1.0))
                        await button.click()
                        env_count += 1
                        print(f"\nClaimed Envelope for {embed.description.split('**')[1]} {embed.description.split('**')[2].split(')')[0].replace(' (','')}.\nTotal Envelope(s) entered: {env_count}\nSleeping...\n\n")
                        sleep(random.uniform(1.0, 60.0))
            
            except AttributeError:
                pass
            
            except discord.HTTPException:
                return
            
            except discord.NotFound:
                return

try:
    client.run(config["TOKEN"])

except discord.LoginFailure:
    print("\nInvalid token, restarting the program...\n\n")
    config["TOKEN"] = ""
    with open("config.json", 'w') as f:
        json.dump(config, f)
