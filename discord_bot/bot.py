from cmath import nan
import discord
import os
import sqlite3
import random
import asyncio
import aiomysql
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get


load_dotenv()
# client=discord.Client()

# connecting to sql database
conn=sqlite3.connect('gamedb.sqlite')
cur = conn.cursor()

# dictionary with numbers being mapped to the three options
game = {
    "stone" : 0,
    "paper" : 1,
    "scissor" : 2
}




cur.executescript('''              
    CREATE TABLE IF NOT EXISTS Player (
        player_id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        player_name         TEXT UNIQUE     
    );
    
    CREATE TABLE IF NOT EXISTS Round (
        game_id             INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        player_id           INTEGER,
        player_input	    INTEGER,
        computer_input	    INTEGER,
        winner	            TEXT,
        FOREIGN KEY (player_id) REFERENCES Player(player_id)
    );
''')

#setting prefix for bot
PREFIX=str(os.getenv('PREFIX'))
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name='start', pass_context=True)
async def startGame(ctx):
    # print(dir(bot))
    
    # getting player name
    player_name=str(ctx.author)
    player_name=player_name.strip()
    await bot.channel.send(player_name)
#     # # inputting player name in Player table
#     # cur.execute('''INSERT OR IGNORE INTO Player (player_name) VALUES (?)''',(player_name,))
#     # cur.execute('SELECT player_id FROM Player WHERE player_name= ?', (player_name,))

#     # # fetching player_id from player_name
#     # player_id=cur.fetchone()[0]

#     # # creating list of all options
#     # game_list=list(game.items())

#     # # selecting random option from game_list and taking player_input
#     # rand_choice=random.choice(game_list)
#     # player_choice=input("What do you want to choose ? ")
#     # player_choice=player_choice.lower();




#     # if player_choice in game.keys():
        
#     #     # on draw
#     #     if player_choice==rand_choice[0]:
#     #         print("Computer choose", rand_choice[0],". Its A Draw")
#     #         winner=nan
#     #         cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
#     #                         VALUES (?,?,?,? )''',
#     #                         (player_id, player_choice, rand_choice[0], winner,))
#     #     # on player winning 
#     #     elif (player_choice=='stone' and rand_choice[0]=='scissor') or (player_choice=='scissor' and rand_choice[0]=='paper') or (player_choice=='paper' and rand_choice[0]=='stone'):
#     #         print("Computer choose",rand_choice[0],". You Won")
#     #         winner=player_name
#     #         cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
#     #                         VALUES (?,?,?,? )''',
#     #                         (player_id, player_choice, rand_choice[0], winner,))
#     #     # on computer winning 
#     #     else:
#     #         print("Computer choose",rand_choice[0],". You Lost")
#     #         winner="Computer"
#     #         cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
#     #                         VALUES (?,?,?,? )''',
#     #                         (player_id, player_choice, rand_choice[0], winner,))

#     # else:
#     #     print("Invalid Input")

# conn.commit()
# conn.close()


D_TOKEN=os.getenv('TOKEN')
bot.run(D_TOKEN)

