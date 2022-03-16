import discord
import os
import sqlite3
import random
from dotenv import load_dotenv

load_dotenv()
client=discord.Client()

# connecting to sql database
conn=sqlite3.connect('gamedb.sqlite')
curr=conn.cursor()

# creating table player and round
curr.executescript('''              
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

# dictionary with numbers being mapped to the three options
game = {
    "stone" : 0,
    "paper" : 1,
    "scissor" : 2
}

# entering player name
player_name = input("Enter your name ")
player_name=player_name.strip()

# inputting player name in Player table
curr.execute('''INSERT OR IGNORE INTO Player (player_name) VALUES (?)''',(player_name,))
curr.execute('SELECT player_id FROM Player WHERE player_name= ?', (player_name,))

# fetching player_id from player_name
player_id=curr.fetchone()[0]

# creating list of all options
game_list=list(game.items())

# selecting random option from game_list and taking player_input
rand_choice=random.choice(game_list)
player_choice=input("What do you want to choose ? ")
player_choice=player_choice.lower();




if player_choice in game.keys():
    
    # on draw
    if player_choice==rand_choice[0]:
        print("Computer choose", rand_choice[0],". Its A Draw")
        winner=nan
        curr.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                        VALUES (?,?,?,? )''',
                        (player_id, player_choice, rand_choice[0], winner,))
    # on player winning 
    elif (player_choice=='stone' and rand_choice[0]=='scissor') or (player_choice=='scissor' and rand_choice[0]=='paper') or (player_choice=='paper' and rand_choice[0]=='stone'):
        print("Computer choose",rand_choice[0],". You Won")
        winner=player_name
        curr.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                        VALUES (?,?,?,? )''',
                        (player_id, player_choice, rand_choice[0], winner,))
    # on computer winning 
    else:
        print("Computer choose",rand_choice[0],". You Lost")
        winner="Computer"
        curr.execute('''INSERT OR IGNORE INTO Round (player_id, player_input, computer_input, winner) 
                        VALUES (?,?,?,? )''',
                        (player_id, player_choice, rand_choice[0], winner,))

else:
    print("Invalid Input")

conn.commit()
conn.close()




