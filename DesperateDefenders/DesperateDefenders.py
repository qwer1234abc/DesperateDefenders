#Kelvin Beh S10244263E IT02 7 August 2022

import random
import pickle

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }

defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']
attack_list = ['ARCHR']
defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },

             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }

monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]

#field2 for hp

field2 = [[None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    print("    1     2     3")
    print(" +-----+-----+-----+-----+-----+-----+-----+")
    for row in range(len(field)):
        print(chr(ord("A") + row), end="")
        for column in range(len(field[row])):
            if field[row][column] == None:
                print('|{:5}'.format(''), end="")
            else:
                print('|{:5}'.format(field[row][column]), end="")
        print("|")
        print(" ", end="")
        for hp in range(len(field2[row])):
            if field2[row][hp] == None:
                print('|{:5}'.format(''), end="")
            else:
                if field[row][hp] in defender_list:
                    if field2[row][hp] <10:
                        if defenders[field[row][hp]]['maxHP'] < 10:
                            print('|{:>2}/{:<} '.format(field2[row][hp], defenders[field[row][hp]]['maxHP']), end="")
                        else:
                            print('|{:>}/{:<2} '.format(field2[row][hp], defenders[field[row][hp]]['maxHP']), end="")
                    else:
                        print('|{:>}/{:<2}'.format(field2[row][hp], defenders[field[row][hp]]['maxHP']), end="")
                elif field[row][hp] in monster_list:
                    if field2[row][hp] >= 10:
                        print('|{:>}/{:<2}'.format(field2[row][hp], monsters[field[row][hp]]['maxHP']), end="")
                    else:
                        print('|{:>}/{:<2} '.format(field2[row][hp], monsters[field[row][hp]]['maxHP']), end="")

        print("|")
        print(" +-----+-----+-----+-----+-----+-----+-----+")
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print("Turn {}    Threat = [{}]   Danger Level {} ".format(game_vars['turn'], game_vars['threat'] * '-' + (game_vars['max_threat'] - game_vars['threat']) * " ", game_vars['danger_level']))
    print("Gold = {}   Monsters killed = {}/{}".format(game_vars['gold'], \
         game_vars['monsters_killed'], game_vars['monster_kill_target']))
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):

    if int(position[1]) >3:
        return False
    unit_hp = defenders[unit_name]['maxHP']

    #Let variable 'a' be the new place_choice
    if position[0] == 'a':
        a = position.replace(position[0], "0")
    elif position[0] == 'b':
        a = position.replace(position[0], "1")
    elif position[0] == 'c':
        a = position.replace(position[0], "2")
    elif position[0] == 'd':
        a = position.replace(position[0], "3")
    elif position[0] == 'e':
        a = position.replace(position[0],"4")

    if  field[int(a[0])][int(a[1])-1] == None:

        field[int(a[0])][int(a[1])-1] = unit_name
        field2[int(a[0])][int(a[1])-1] = unit_hp
        game_vars['gold'] -= defenders[unit_name]['price']

    else:
        print("\nA unit is on the position you are placing!")
        draw_field()
        return False


    draw_field()
    return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit():
    print("What unit do you wish to buy?")
    for index in range(len(defender_list)):
        print('{}. {} ({} gold)'.format(index+1, defenders[defender_list[index]]['name'],defenders[defender_list[index]]['price']))
    print("3. Don't buy")
    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):
    total_dmg = 0
    lanes = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    for amount in range(field[row].count(defender_name)):
        damage = int(random.randint(defenders["ARCHR"]['min_damage'], defenders["ARCHR"]['max_damage']))
        total_dmg += damage
    field2[row][column] -= total_dmg
    print('Archer(s) in lane {} shoots {} for {} damage!'.format(lanes[row + 1], monsters[monster]['name'],total_dmg))

    if field2[row][column] <= 0:
        print('{} dies!'.format(monsters[monster]['name']))
        print('You gain {} gold as a reward'.format(monsters[field[row][column]]['reward']))
        game_vars['monsters_killed'] += 1
        game_vars['gold'] += monsters[field[row][column]]['reward']
        game_vars['threat'] += monsters[field[row][column]]['reward']
        game_vars['num_monsters'] -= 1
        field2[row][column] = None
        field[row][column] = None

    return


#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, column):
    lanes = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    print('{} in lane {} advances!'.format(monsters[monster_name]['name'], lanes[row + 1]))
    if monster_name == "ZOMBI":
        if field[row][column-1] == "ARCHR" or field[row][column-1] == "WALL":
            dmgMonst = random.randint(monsters["ZOMBI"]['min_damage'], monsters["ZOMBI"]['max_damage'])
            field2[row][column - 1] -= dmgMonst
            if field2[row][column - 1] <= 0:
                field2[row][column - 1] = None
                field[row][column - 1] = None
        elif field[row][column - 1] == monster_name:
            pass

        else:
            if field[row][0] == 'ZOMBI':
                print('A {} has reached the city! All is lost!'.format(monsters["ZOMBI"]['name']))
                print('You have lost the game. :(')
                exit()
            else:
                field[row][column] = None
                field[row][column - 1] = monster_name
                a = field2[row][column]
                field2[row][column - 1] = a
                field2[row][column] = None
    elif mons == "WWOLF":
        if field[row][column-1] == "ARCHR" or field[row][column-1] == "WALL":
            dmgMonst = random.randint(monsters["WWOLF"]['min_damage'], monsters["WWOLF"]['max_damage'])
            field2[row][column - 1] -= dmgMonst
            if field2[row][column - 1] <= 0:
                field2[row][column - 1] = None
                field[row][column - 1] = None
        elif field[row][column-2] == "ARCHR" or field[row][column-2] == "WALL":
            if field[row][column-1] != "WWOLF" or field[row][column-1] != "ZOMBI":
                dmgMonst = random.randint(monsters["WWOLF"]['min_damage'], monsters["WWOLF"]['max_damage'])
                field2[row][column - 2] -= dmgMonst
                if field2[row][column - 2] <= 0:
                    field2[row][column - 2] = None
                    field[row][column - 2] = None
                field[row][column] = None
                field[row][column - 1] = monster_name
                a = field2[row][column]
                field2[row][column - 1] = a
                field2[row][column] = None
            else:
                pass
        elif field[row][column-1] == "ZOMBI" or field[row][column-1] == "WWOLF":
            pass
        elif field[row][column-2] == "ZOMBI" or field[row][column-2] == "WWOLF":
            field[row][column] = None
            field[row][column - 1] = monster_name
            a = field2[row][column]
            field2[row][column - 1] = a
            field2[row][column] = None
        else:
            if field[row][0] == 'WWOLF' or (field[row][1] == 'WWOLF' and field[row][0] == None):
                print('A {} has reached the city! All is lost!'.format(monsters['WWOLF']['name']))
                print('You have lost the game. :( ')
                exit()
            field[row][column] = None
            field[row][column - 2] = monster_name
            a = field2[row][column]
            field2[row][column - 2] = a
            field2[row][column] = None

    return



#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    game_vars['num_monsters'] += 1
    random_place = random.randint(0, len(field)-1)
    random_monster = random.randint(0, len(monster_list)-1)
    unit_name = monster_list[random_monster]
    unit_hp = monsters[monster_list[random_monster]]['maxHP']

    for i in field:
        if i[-1] == None:
            field[random_place][-1] = unit_name
            field2[random_place][-1] = unit_hp

    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    file = open("save.txt","wb") #write binary file into save.txt
    # store the datas below into the file by using dump()
    pickle.dump(game_vars,file)
    pickle.dump(field,file)
    pickle.dump(field2,file)
    file.close
    print("Game saved!")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game():
    # Modify the variables below to that of the ones loaded with global and make it accessible outside this function
    global field
    global field2
    global game_vars
    file = open("save.txt","rb") #read binary file from save.txt
    # load the pickled or saved data from the file and use it
    game_vars = pickle.load(file)
    field = pickle.load(file)
    field2 = pickle.load(file)

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    game_vars['threat'] = 0
    game_vars['danger_level'] = 1


#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
while True:
    show_main_menu()
    break
saved_game = False
end_after_place = False
while True:
    choices = input('Your choice? ')
    if choices == "1":

        spawn_monster(field,monster_list)
        draw_field()
        game_vars['turn'] += 1
        break
    elif choices == "2":
        try:
            load_game()
            draw_field()
            saved_game = True
            break
        except (EOFError, pickle.UnpicklingError, FileNotFoundError) as error :
            print("\nNo saved game")
            show_main_menu()
    elif choices == "3":
        print('Come by soon!')
        exit()
    else:
        print('\nPlease select another option')
        show_main_menu()


while True:
    if choices == "1" or saved_game == True:
        show_combat_menu(game_vars)
        choice = input('Your choice? ')
        if choice == "1":
            buy_unit()
            while True:
                unit_choice = input("Your choice? ")
                if unit_choice == "1" or unit_choice ==  "2":
                    try:
                        position = input("Place where? ")
                        if unit_choice == "1" or unit_choice == "2":
                            if unit_choice == "1":
                                if game_vars['gold'] >= defenders["ARCHR"]['price']:
                                    place_unit(field,position, 'ARCHR')
                                else:
                                    print("\nNot Enough Gold")
                                    draw_field()
                            elif unit_choice == "2":
                                if game_vars['gold'] >= defenders["WALL"]['price']:
                                    place_unit(field, position, 'WALL')
                                else:
                                    print("\nNot Enough Gold")
                                    draw_field()
                            break
                        else:
                            print("\nPosition selected is not in field of play please try again.")
                            buy_unit()
                            continue
                    except (IndexError, ValueError, UnboundLocalError) as error:
                        print("\nPosition selected is not in field of play please try again.")
                        buy_unit()
                        continue

                elif unit_choice == "3":
                    draw_field()
                    break
                else:
                    print("\nSelect another option from 1-3.")
                    buy_unit()
                    continue

        elif choice == "2" or end_after_place == True:
            for row in range(len(field)):
                for defender in attack_list:
                    for monster in monster_list:
                        if monster in field[row] and defender in field[row]:
                            column = field[row].index(monster)
                            monster = field[row][column]
                            defender_attack(defender, field, row, column)
                for column in range(len(field[row])):
                    for mons in monster_list:
                        if field[row][column] == mons:
                            monster_advance(mons, field, row, column)
            game_vars['turn'] += 1
            game_vars['gold'] += 1
            game_vars['threat'] += random.randint(1, game_vars['danger_level'])
            if game_vars['turn'] % 12 == 0:
                game_vars['danger_level'] += 1
                for m in monsters:
                    monsters[m]['maxHP'] += 1
                    monsters[m]['max_damage'] += 1
                    monsters[m]['min_damage'] += 1
                    monsters[m]['reward'] += 1
            if game_vars['num_monsters'] < 1:
                spawn_monster(field, monster_list)
                game_vars['gold'] += 1
            if game_vars['threat'] > 10:
                game_vars['threat'] = 0
                spawn_monster(field, monster_list)
            if game_vars['monsters_killed'] >= game_vars['monster_kill_target']:
                print('You have protected the city! You win!')
                break
            draw_field()
        elif choice == "3":
            save_game()
            break
        elif choice == "4":
            print('See you next time!')
            break
        else:
            print('\nPlease enter a valid choice')
            draw_field()




