from discord.ext import commands
from replit import db
import discord
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta
import threading
from keep_alive import keep_alive

intents = discord.Intents( guilds=True,members=True,presences=True,messages=True)
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)
start = datetime.now() # Initializing start variable
vector1 = [] # Initializing "vector"
day_count = 0 # Initializing day_count reset timer (that doesn't work (actually don't know if it works or not))
i = 0 #Initializing trivial count variable
client = discord.Client()
load_dotenv('TOKEN.env') #Loading bot password




class Person: #Creates the person object
  def __init__(help, name, starttime, endtime, totaltime):
    help.name = name #Name of individual
    help.starttime = starttime #Time started Overwatch
    help.endtime = endtime #Time stopped Overwatch
    help.totaltime = totaltime #Total time on Overwatch stored in deltatime



@bot.event
async def on_ready():
    print("bot ready") #Lets me know that indeed the bot is trying to do something
    now = datetime.now() #Takes the current time of start
    current_time = now.strftime("%H:%M:%S") #Formats the time into a string
    print("Current Time =", current_time) #Tells me the time it started working
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='The Clock')) #Changes bot status to "Watching The Clock"
    to_leave = bot.get_guild(891700203101519962)
    print(to_leave)
    await to_leave.leave()
    

my_token = os.getenv('TOKEN')

keep_alive()
bot.run(my_token)
client.run(my_token)
