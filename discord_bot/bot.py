from cmath import nan
import discord
import os
import sqlite3
import random
import asyncio
import aiomysql
# import pandas
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord.utils import get
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

load_dotenv()

# dictionary with numbers being mapped to the three options
game = {
    "stone" : 0,
    "paper" : 1,
    "scissor" : 2
}

#setting prefix for bot
PREFIX=str(os.getenv('PREFIX'))
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    
    # connecting to sql database
    conn=sqlite3.connect('gamedb.sqlite')
    cur = conn.cursor()
    
    
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
    
    conn.commit()
    conn.close()
    print('We have logged in as {0.user}'.format(bot))
    DiscordComponents(bot, change_discord_methods=True)

@bot.command(name='start', pass_context=True)
async def startGame(ctx):
    conn=sqlite3.connect('gamedb.sqlite')
    cur = conn.cursor()
    
    # getting player name
    player_name=str(ctx.author)
    player_name=player_name.strip()
    await ctx.send('You will now play {}'.format(player_name))
    
    # inputting player name in Player table
    cur.execute('''INSERT OR IGNORE INTO Player (player_name) VALUES (?)''',(player_name,))
    cur.execute('SELECT player_id FROM Player WHERE player_name= ?', (player_name,))
    
    # fetching player_id from player_name
    player_id=cur.fetchone()[0]

    # creating list of all options
    game_list=list(game.items())

    # selecting random option from game_list and taking player_input
    rand_choice=random.choice(game_list)
    await ctx.send('What do you want to choose ? ')
    
    # taking user input and storing it in variable
    try:
        msg = await bot.wait_for("message", timeout=30) # 30 seconds to reply
    except asyncio.TimeoutError:
        await ctx.send('Sorry, bot took your delay as a sign of cowardice')
    await ctx.send('Your option was {}'.format(msg.content))
    player_choice=str(msg.content)
    player_choice=player_choice.lower();




    if player_choice in game.keys():
        
        # on draw
        if player_choice==rand_choice[0]:
            await ctx.send('Bot choose {} . Its A Draw'.format(rand_choice[0]))
            winner=nan
            cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                            VALUES (?,?,?,? )''',
                            (player_id, player_choice, rand_choice[0], winner,))
        # on player winning 
        elif (player_choice=='stone' and rand_choice[0]=='scissor') or (player_choice=='scissor' and rand_choice[0]=='paper') or (player_choice=='paper' and rand_choice[0]=='stone'):
            await ctx.send('Bot choose {} . {} Won '.format(rand_choice[0],player_name))
            winner=player_name
            cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                            VALUES (?,?,?,? )''',
                            (player_id, player_choice, rand_choice[0], winner,))
        # on computer winning 
        else:
            await ctx.send('Bot choose {} . {} Won '.format(rand_choice[0],player_name))
            winner="Computer"
            cur.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                            VALUES (?,?,?,? )''',
                            (player_id, player_choice, rand_choice[0], winner,))

    else:
        await ctx.send('We are playing stone, paper and scissor. What are you playing ?')
    conn.commit()
    conn.close()

# gets total count of all wins
@bot.command(name='mywins', pass_context=True)
async def listWinners(ctx):
    conn=sqlite3.connect('gamedb.sqlite')
    cur = conn.cursor()
    
    # getting player name
    player_name=str(ctx.author)
    player_name=player_name.strip()
    
    cur.execute('SELECT COUNT(winner) FROM Round WHERE winner= ?', (player_name,))
    win_count=cur.fetchall()
    
    cur.execute('SELECT game_id, winner, player_input, computer_input FROM Round WHERE winner= ?', (player_name,))
    winner_detail=cur.fetchall()
    
    num_wins=win_count[0][0]
    await ctx.send('{} has won {} games'.format(player_name, num_wins))
    # await ctx.send(winner_detail)
    
    conn.commit()
    conn.close()



D_TOKEN=os.getenv('TOKEN')
bot.run(D_TOKEN)

