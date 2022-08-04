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
target_channel_id = 963582662684069928 #TannerBot Channel address
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
    channelTime = bot.get_channel(963582662684069928)
    id = channelTime.guild.id
    print(id)

@bot.event
async def on_member_update(before, after):
        global vector1
        global start 
        global i
        if (after.activity is not None and before.activity is not None): #Case 1: was doing something before and is doing something after (have to do these paths because NoneType breaks everything).
            print("Overwatch1") # Dumb name to know this path was taken.
            i = 0 # Count reset
            if(str(after.activity.name) == 'Overwatch' and str(before.activity.name != 'Overwatch')): #Case 1a: If Overwatch is being played after but not before, take this path.
                print(before.name + " is playing " + after.activity.name) # Tells me what the user is playing after.
                print(after.activity.name) # Tells me the after activity... again...
                start = datetime.now() # Takes the current time
                starting_time = start.strftime("%H:%M:%S") #Formats the time into string
                if (vector1): #If vector is not empty
                    while (i < len(vector1)): # While the count is staying within the vector (so it doesn't go past the size of the vector)
                        if (vector1[i].name == before.mention): # If the name of the object (person) in the vector is the same as the member who changed their status.
                            vector1[i].starttime = start #The starttime stored in their object is now the current time.
                            if before.mention in db:
                                vector1[i].totaltime = convert_string_to_timedelta(db.get(before.mention))
                            i = len(vector1) + 1 # Ends the while loop
                        else: # If there is not a match, end the while loop.
                            i = i + 1
                    if (i == len(vector1)): #If count is equal to the size of the vector (there was not a match)
                        player = Person(before.mention, start, start, start - start) # Store a new Person object into a variable.
                        vector1.append(player) # Add person object to the vector with default values and name of member.
                        i = 0 # Reset the count
                else: # If the vector is empty
                    if before.mention in db:
                        resetTotal = convert_string_to_timedelta(db.get(before.mention))
                        player = Person(before.mention, start, start, resetTotal)
                        vector1.append(player)
                        i = 0
                    else:
                        player = Person(before.mention, start, start, start - start) #Store a new Person object into a variable
                        vector1.append(player)
                        i = 0
            elif(str(before.activity.name) == 'Overwatch' and str(after.activity.name) != 'Overwatch'):
                    print(before.name + " is no longer playing " + before.activity.name)
                    print(str(before.activity.name))
                    end = datetime.now()
                    ending_time = end.strftime("%H:%M:%S")
                    vector1.append(player)
                    i = 0
                    print("Overwatch2")
                    i = 0
                    while i < len(vector1) and vector1[i].name != before.mention:
                        i = i + 1
                    if (i == len(vector1)):
                        return
                    vector1[i].endtime = end
                    if (vector1[i].starttime >= vector1[i].endtime):
                        h1 = timedelta(hours=12)
                        Total = vector1[i].endtime - vector1[i].starttime + h1
                        vector1[i].totaltime = vector1[i].totaltime + Total
                        db[before.mention] = convert_timedelta_to_string(vector1[i].totaltime)
                        total_time = str(Total).split(".")[0]
                        print(total_time)
                        channelTime = bot.get_channel(963582662684069928)
                        i = 0
                    else:
                        Total = vector1[i].endtime - vector1[i].starttime
                        vector1[i].totaltime = vector1[i].totaltime + Total
                        db[before.mention] = convert_timedelta_to_string(vector1[i].totaltime)
                        total_time = str(Total).split(".")[0]
                        print(total_time)
                        channelTime = bot.get_channel(963582662684069928)
                        i = 0
        elif(before.activity is None and after.activity is not None):
            if(after.activity is not None):
              if(str(after.activity.name) == 'Overwatch'):
                  print(after.activity.name)
                  print("Overwatch3")
                  i = 0
                  print(before.name + " is playing " + after.activity.name)
                  print(after.activity.name)
                  start = datetime.now()
                  starting_time = start.strftime("%H:%M:%S")
                  if (vector1):
                      while (i < len(vector1)):
                          if (vector1[i].name == before.mention):
                              vector1[i].starttime = start
                              if before.mention in db:
                                  vector1[i].totaltime = convert_string_to_timedelta(db.get(before.mention))
                              i = len(vector1) + 1
                          else:
                              i = i + 1
                      if (i == len(vector1)):
                          player = Person(before.mention, start, start, start - start)
                          vector1.append(player)
                          i = 0
                  else:
                      if before.mention in db:
                          resetTotal = convert_string_to_timedelta(db.get(before.mention))
                          player = Person(before.mention, start, start, resetTotal)
                          vector1.append(player)
                          i = 0
                      else:
                          player = Person(before.mention, start, start, start - start) #Store a new Person object into a variable
                          vector1.append(player)
                          i = 0
        
        elif (after.activity is None and before.activity is not None):
              if(str(before.activity.name) == 'Overwatch'):
                  print(before.activity.name)
                  print("Overwatch4")
                  print(before.name + " is no longer playing " + before.activity.name)
                  print(str(before.activity.name))
                  end = datetime.now()
                  ending_time = end.strftime("%H:%M:%S")
                  i = 0
                  while i < len(vector1) and vector1[i].name != before.mention:
                      i = i + 1
                  if( i == len(vector1)):
                      return
                  vector1[i].endtime = end
                  if (vector1[i].starttime >= vector1[i].endtime):
                      h1 = timedelta(hours=12)
                      Total = vector1[i].endtime - vector1[i].starttime + h1
                      vector1[i].totaltime = vector1[i].totaltime + Total
                      db[before.mention] = convert_timedelta_to_string(vector1[i].totaltime)
                      total_time = str(Total).split(".")[0]
                      print(total_time)
                      channelTime = bot.get_channel(963582662684069928)
                      i = 0
                  else:
                      Total = vector1[i].endtime - vector1[i].starttime
                      vector1[i].totaltime = vector1[i].totaltime + Total
                      db[before.mention] = convert_timedelta_to_string(vector1[i].totaltime)
                      print(db.get(before.mention))
                      total_time = str(Total).split(".")[0]
                      print(total_time)
                      channelTime = bot.get_channel(963582662684069928)
                      i = 0
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    i = 0
    if message.content.startswith('?time'):
        print(message.author.mention)
        print(db.get(message.author.mention))
        if message.author.name == "Soy Clown, Tu Clown":
          await message.channel.send("Soy Clown, Tu Clown's time is invalid")
        await message.channel.send(message.author.name + "'s total time is " + str(convert_string_to_timedelta(db.get(message.author.mention))).split(".")[0])
    elif message.content.startswith('?last') and vector1:
        while (i < len(vector1) and vector1[i].name != message.author.mention):
            i = i + 1
        if (i == len(vector1)):
            return
        if (vector1[i].starttime >= vector1[i].endtime):
            h1 = timedelta(hours=24)
            await message.channel.send(message.author.name + "'s last session time was " + str(vector1[i].endtime - vector1[i].starttime + h1).split(".")[0])
        else:
            await message.channel.send(message.author.name + "'s last session time was " + str(vector1[i].endtime - vector1[i].starttime).split(".")[0])
    elif message.content.startswith('?alltime'):
        keys = list(db.keys())
        j = 0
        for key in db:
            userID = keys[j]
            print(userID)
            userID = userID.replace('{', "")
            userID = userID.replace('}', "")
            usermention = userID
            userID = userID.replace('<', "")
            userID = userID.replace('>', "")
            userID = userID.replace('!', "")
            print(usermention)
            userID = userID.replace('@', "")
            print(userID)
            user = await bot.fetch_user(userID)
            await message.channel.send(user.name + "'s total time is " + str(convert_string_to_timedelta(db.get(usermention))).split(".")[0])
            j = j + 1
        await message.channel.send("Soy Clown, Tu Clown's total time is invalid since custom statuses haven't been implemented yet and I'm lazy")
    elif message.content.startswith('?hello'):
            await message.channel.send(message.author.name + " is epic")
    i = 0
  
def convert_timedelta_to_string(td):
    # type: (datetime.timedelta) -> str
    """Convert a time delta to string
    :param datetime.timedelta td: time delta to convert
    :rtype: str
    :return: string representation
    """
    days = td.days
    hours = td.seconds // 3600
    minutes = (td.seconds - (hours * 3600)) // 60
    seconds = (td.seconds - (hours * 3600) - (minutes * 60))
    return '{0}.{1:02d}:{2:02d}:{3:02d}'.format(days, hours, minutes, seconds) 

def convert_string_to_timedelta(string):
    # type: (str) -> datetime.timedelta
    """Convert string to time delta. strptime() does not support time deltas
    greater than 24 hours.
    :param str string: string representation of time delta
    :rtype: datetime.timedelta
    :return: time delta
    """
    # get days
    tmp = string.split('.')
    if len(tmp) == 2:
        days = int(tmp[0])
        tmp = tmp[1]
    elif len(tmp) == 1:
        days = 0
        tmp = tmp[0]
    else:
        raise ValueError('{} is not a valid timedelta string'.format(string))
    # get total seconds
    tmp = tmp.split(':')
    if len(tmp) != 3:
        raise ValueError('{} is not a valid timedelta string'.format(string))
    totsec = int(tmp[2]) + int(tmp[1]) * 60 + int(tmp[0]) * 3600
    return timedelta(days, totsec) 

my_token = os.getenv('TOKEN')

keep_alive()
bot.run(my_token)
client.run(my_token)
