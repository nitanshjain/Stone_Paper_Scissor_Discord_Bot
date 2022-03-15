import random
import sqlite3

conn=sqlite3.connect('gamedb.sqlite')
curr=conn.cursor()

curr.executescript('''
    CREATE TABLE IF NOT EXISTS Game ( 
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        game_name TEXT
    );
    
    
    CREATE TABLE IF NOT EXISTS Player (
        id                INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        player_name       TEXT
    );
    
    CREATE TABLE IF NOT EXISTS Round (
        game_id             INTEGER,
        player_id           INTEGER,
        player_input	    INTEGER,
        computer_input	    INTEGER,
        winner	            TEXT,
        PRIMARY KEY (game_id, player_id)
    );
''')

game = {
    "stone" : 0,
    "paper" : 1,
    "scissor" : 2
}

score = {
    "Computer" : 0,   
}

player_name = input("Enter your name ")
score[player_name]=0;

curr.execute('''INSERT OR IGNORE INTO Player (player_name) VALUES (?)''',(player_name,))
curr.execute('SELECT id FROM Player WHERE player_name= ?', (player_name,))
player_id=curr.fetchone()[0]

num_rounds = int(input("Enter the number of rounds you want to play : "))

game_list=list(game.items())
for i in range(num_rounds):
    
    rand_choice=random.choice(game_list)
    player_choice=input("What do you want to choose ? ")
    player_choice=player_choice.lower();
    
    game_name=player_name+str(i)
    curr.execute('''INSERT OR IGNORE INTO Game (game_name) VALUES (?)''', (game_name,))
    curr.execute('SELECT id FROM Game WHERE game_name = ? ', (game_name, ))
    game_id = curr.fetchone()[0]
    
    if player_choice in game.keys():
        
        if player_choice==rand_choice[0]:
            print("Computer choose", rand_choice[0],". Its A Draw")
            winner="Draw"
            curr.execute('''INSERT OR IGNORE INTO Round (game_id, player_id, player_input, computer_input, winner) 
                            VALUES ( ?,?,?,?,? )''',
                            (game_id, player_id, player_choice, rand_choice[0], winner))
            
        elif (player_choice=='stone' and rand_choice[0]=='scissor') or (player_choice=='scissor' and rand_choice[0]=='paper') or (player_choice=='paper' and rand_choice[0]=='stone'):
            print("Computer choose",rand_choice[0],". You Won")
            score[player_name]=score[player_name]+1
            winner=player_name
            curr.execute('''INSERT OR IGNORE INTO Round (game_id, player_id, player_input, computer_input, winner) 
                            VALUES ( ?,?,?,?,? )''',
                            (game_id, player_id, player_choice, rand_choice[0], winner))
            
        else:
            print("Computer choose",rand_choice[0],". You Lost")
            score["Computer"]=score["Computer"]+1 
            winner="Computer"
            curr.execute('''INSERT OR IGNORE INTO Round (game_id, player_id, player_input, computer_input, winner) 
                            VALUES ( ?,?,?,?,? )''',
                            (game_id, player_id, player_choice, rand_choice[0], winner))
    
    else:
        print("Invalid Input")
        continue
        
    # print(game[player_choice])
    
    
print(score)
conn.commit()
conn.close()
    