"""
I define the map of my game in a text file outline called a YAML file. YAML is just a specific way to write an outline that can easily be read
and converted to python dictionaries and lists. There is a library called yaml that lets me read the YAML file and convert it to a dictionary.
That way I can have 1000 maps but only one program.

sys is another python library. I use it to read the YAML file
"""
import yaml, sys

world = {} # game map of rooms as a dictionary
current_location = {} # the current room a player is in
bag = [] # the stuff a player is carrying

# these next did_xxx variables are flags used to check that the player solved the different problems in the game
did_spin = False # did they run the colorwheel spinner
did_piano = False # did they play the piano
did_build = False # did they build the box
did_break = False # did they use the sledgehammer
did_note = False #did they read the note
did_die = False # did they die?
did_riddle = False # did they read the riddle

def set_location(room):
    """ set the players current location to room """
    
    global current_location

    # we check to make sure I don't accidentally set the current location to a room not in the map!
    if room in world['ROOMS']:
        current_location = world['ROOMS'][room]
    else:
        print("LOSER - this room %s doesn't exist!" % room) # the %s thingy is a way in python to put a string inside another string

def get_location(loc):
    """ search through the world map for the location and return it if found """
    
    place = { "name": "The Void" }
    if loc in world['ROOMS']:
        place = world['ROOMS'][loc]
    
    return place

def print_location():
    """ print out all the information about which room the player is in """
    
    print('') # this prints a blank line
    print(current_location['name'])
    print('=' * len(current_location['name'])) # trick to print N equal signs where N is the length of the name of the room
    print(current_location['description'])
    print('')
    
    # print out all the moves and the destination if you try and go in that direction
    if 'moves' in current_location:
        moves = current_location['moves']
        for direction in moves:
            location = get_location(moves[direction])
            print("%s: %s" % (direction, location["name"]))
    print('')
    
    # print out all the items in the room
    if 'items' in current_location:
        if len(current_location['items']) > 0:
            print("you can see the following: " + ", ".join(current_location['items']))

def do_help():
    # create a formatted multi line string using triple quotes
    message = """
    Here is the list of available movement commands: 
         - north, south, east, west, northeast, southeast, northwest, southwest, jump

    In addition, you can TAKE an object, DROP an object, PLAY PIANO, 
    LOOK at an object (or just say look and it will show you where you are),
    SPIN the wheel, BUILD a box, and INVENTORY to get a list of items in your bag. 
    
    Oh, and QUIT. Quits the game."""
    print(message)

def do_hint():
    print("\nSeriously?! You want a hint in a lame ass game like this?\n")
    
def do_take(obj):
    """ take an object from the room and put into your bag """
    
    # check to make sure the object is really in the room
    if obj in current_location['items']:
        bag.append (obj) # lists use append() to add to them
        current_location['items'].remove (obj) # lists use remove() to remove objects from themselves
        inventory()
    else:
        print("\nHey! That item is not here.\n") #the item typed in is not used in the game

def inventory():
    """ print out the list of stuff in your bag """
    if len(bag) > 0: #if there is more than 0 items in a player's inventory, then the following message will read
        print("\nYou have the following in your bag:")
        for item in bag: # for every item in your bag
            print("\t" + item)
    else:
        print("\nYour bag is empty. Go to Whole Foods.\n") #if there is nothing in a players bag this message will read
      
def do_drop(obj):
    """ take an object out of the bag and drop it onto the ground """
    
    # in the YAML for some rooms there is no items list
    # so you have to check for the items list first and if it isn't
    # there create it so you can remove the item from your bag and put
    # it in the room
    if not 'items' in current_location:
        current_location['items'] = []

    if obj in bag: 
        bag.remove (obj) #remove item from bag
        current_location['items'].append (obj)
    else:
        print("\nWhat'chu talking bout Willis? I don't have that.\n") #if an item that is not in the players bag is entered, this message will be read
        
def do_spin():
    """ spin the colorwheel in the colorwheel room """
    global did_spin
    if current_location['name'] == "Colorwheel Room": #function only works in colorwheel room
        print("\nYou spin the wheel and it lands on blue! You have unlocked the door.\n")
        did_spin = True #variable is set to true
    else:
        print("\nYoooo...there's nothing to spin here.\n") #if not in colorwheel room, this message will be read
        
def do_piano():
    """ play the piano in the fugue room and in big bedroom """
    global did_piano
    if current_location['name'] == "Fugue Room" or current_location['name'] == "Big Bedroom": #function only works in fugue room and big bedroom
        print("\nBach plays his fugue and you're finally smart enough to actually solve the math problem! You unlocked the door.\n")
        did_piano = True #variable is set to true
    else:
        print("\nYou're still wayyyyy too stupid to solve the simple one-step equation.\n") #if not in fugue room or big bedroom, this message will be read

def do_build():
    """ build a box to unlock door in bob the builders room """
    global did_build
    if "hammer" and "nails" and "wood" in bag: #function will only work if these items are in inventory
        print("\nThe door is 10 feet above the ground. Using items in your inventory you built a box that allowed you and Bach to finally reach the door!\n")

        # now that the box is built we can drop the tools and wood used
        do_drop("hammer")
        do_drop("nails")
        do_drop("wood")

        did_build = True #variable set to true
    else:
        print("\nHmmm... to build something you need wood, a small hammer, and nails. You don't have all that.")

def check_Bach1_door():
    """ check if door opens in bachs bedroom """
    if "key" in bag:
        print("\nThe door is locked. But you have a key! In an remarkable example of GCC brillance, you use the key to unlock the door!\n") #shows when player has key in inventory
        # we keep the key in the bag so we can use it again if we come back
        return True  
    else:
        return False

def check_colorwheel():
    """ check if door opens in colorwheel room """
    if did_spin: #check did_spin variable
        return True
    else:
        return False

def check_fugue():
    """ check if door opens in fugue room """
    if did_piano: #check did_piano variable
        return True
    else:
        print("You don't feel smart enough to figure this out. Studies shows that playing fugue music on the piano makes you super smart. It's a thing. Seriously.") #print this if door does not unlock
        return False

def check_box():
    """ check if door is unlocked in bob the builders room """
    if did_build:
        print("Whew! Bet you're glad you built that box. You can climb the box, unlock the door, and get the heck out...")        
        return True
    else:
        return False

def check_break():
    """ check if door is unlocked in lion tamers tool room """
    global did_break
    
    if "sledge hammer" in bag: #if sledge hammer is in inventory
        print("\nThere is no knob on the door! You find a 12 pound sledgehammer in your bag and break down the door with ease.\n")
        do_drop("sledge hammer") #remove sledge hammer from inventory after used
        did_break = True
        return True
    else:
        return False

def check_riddle():
    """ check if note can be read to use in game """
    if 'note' in bag:
        did_note = True #check did_note variable
        print("You remember that you have a note with a code on it! You take the note out of your bag, read it, and punch 8173 on the keypad. WOOSH... the door opens. You crumple up the note and toss it out. Litterer!") #print when door is unlocked
        do_drop('note') #now that the noet's been read you discard it and litter
        return True
    else:
        return False

def check_math2():
    """ check if riddle can be read and used in game """
    if did_riddle:
        print("The riddle! You remember that the answer to the riddle is 'umbrella' (ella, ella, ella) so you enter that into the keypad and life is good. The door is open but the fly is not dead yet") #print when door is unlocked
        return True
    else:
        return False

def check_lions_den():
    """ check if player has lion taming tool """
    global did_die
    
    if 'lion taming tool' in bag: #if the player has the lion taming tool
        # you can make a multiple line string using tripe quotes
        message = """
        Those lion's are hungry! And mean! And pretty... they really 
        are pretty. And vicious. And hungry. Did I say that already? Luckily 
        you have the lion taming tickler tool in your bag. You tickle the 
        lion and he LOVES you. So you live... for now."""
        
        print(message)

        return True
    else:
        # use triple quotes in python to make a multi line string
        message = """
        Those lion's are hungry! And mean! And pretty... they 
        really are pretty. And vicious. And hungry. Did I say that 
        already? Ummm... bad news. IF you have the *lion taming tool* 
        you could soothe the savage beasts and leave. But you don't so 
        you can't. How do I put this delicatly? They rip you to shreds. 
        With the last remnants of your remaining eye and a few strands 
        of neurons left you see a speck of water on the ground... 
        
        Somehow what's left of your tongue touches the water drop... and
        everything fades to black. Wait. Ouch! Ouch! Ouch!"""

        print(message)

        did_die = True #set did_die flag
        return False

def check_puddle1():
    """ make sure player has goggles and flippers """
    global did_die
    
    if 'goggles' in bag and 'flippers' in bag: #if player has goggles and flippers in bag
        return True
    else:
        print("Houston, we have a problem. You need goggles and flippers to swim through a deep dark dank dreary dumb puddle. You might not make it...") #print when player does not have goggles and flippers
        did_die = True
        return False

def check_puddle3():
    """ check if player has only goggles and flippers in bag, nothing else """
    global did_die
    
    # check if the player ONLY has googles and flippers in the bag
    if 'goggles' in bag and 'flippers' in bag and len(bag) == 2:
        print("\nYou put on your goggles and flippers and make like Michael Phelps and jump into the puddle...\n") #printed when player has only goggles and flippers
        return True
    else:
        print("Houston, we have a problem. You need goggles and flippers to swim through a deep dark dank dreary dumb puddle. And nothing else. You might not make it...")
        did_die = True #set did_die flag
        return False
  
    
def do_look(obj):
    """ describe an object or location """
    global did_note, did_riddle
    
    if obj: #if player types look OBJ, make sure  they have it first in bag
        if obj in bag:
            if obj == 'note':
                print("You read the note and it says '8173'. Hmmmmmm...")
                did_note = True #set did_note flag
            elif obj == 'riddle':
                print("You look at the riddle and it says 'What goes up when rain goes down?' and you KNOW the answer is 'umbrella'! You are supremely confident this will be information that you'll need later")
                did_riddle = True #set did_riddle flag
            else:
                print("You look at the %s and see nothing special" % obj)
        else:
            print("Umm... you can't look at something you don't have")
    else:
        print_location() #tell player where they are 
        
def move(direction):
    """ move to next room, doing whatever checks are required in map """
    global did_die
    
    ok_to_move = True
    whereto = direction.upper()

    if whereto in current_location['moves']: #make sure player can go that way from current room
        """every room in the map says which directions are available. some directions have preconditions. I call these 'checks'.
            this block of code tests for whether there are any checks needed. If there is, some python magic is used to take a string and
            convert it into an actual function that can be called. """
        if 'checks' in current_location and whereto in current_location['checks']:
            fn = current_location['checks'][whereto]
            ok_to_move = globals()[fn]() # all checks return true or false
        if ok_to_move: #checks are checked, move to that location 
            new_location = current_location['moves'][whereto]
            set_location(new_location)
            print_location()
        else: #some failed checks cause the player to die, so we test for that
            if did_die == False:
                print("Hmm... you legs feel heavy and you can't move. You have this sudden feeling this is something you need to do first...")
            else:
                did_die = False
                set_location("ROOM_DEAD")
                
    else:
        print("Hey! You can't go that way")

def get_command():
    """ reads input from screen and returns command and object. if there is no object it returns an empty string for the object."""
    PROMPT = ">> "
    s = input(PROMPT) #read input from the screen 
    words = s.lower().strip().split(' ') #converts input to lowercase, strips leading and trailing white spaces, and makes a list of words

    cmd = words[0].lower().strip() #command is the first word 
    obj = ' '.join(words[1:]).lower().strip() #take all the other words and put them back together with a space between them to display the OBJ

    return cmd, obj

def play():
    """ loop to play the game """
    done = False

    DIRECTIONS = [ # list of moves player can make
        'north',
        'south',
        'east',
        'west',
        'northeast',
        'southeast',
        'northwest',
        'southwest',
        'up',
        'down',
        'jump',
        'restart'
    
    ]

    print_location() #prints location to start game 
    while not done:
        cmd, obj = get_command()
        
        if cmd in DIRECTIONS: #check to see if command is movement command
            move(cmd)
            
        #test for the common commands used throughout the game
        #each command has its own function
        elif cmd == 'quit':
            raise SystemExit
        elif cmd == '?' or cmd == 'help':
            do_help()
        elif cmd == 'hint':
            do_hint()
        elif cmd == 'look':
            do_look(obj)
        elif cmd == "take":
            do_take(obj)
        elif cmd == "drop":
            do_drop(obj)
            inventory() # after we drop something show what's left in the bag
        elif cmd == "inventory":
            inventory()
        elif cmd == "spin":
            do_spin()
        elif cmd == "play" and obj == "piano":
            do_piano()
        elif cmd == "build":
            do_build()
        else:
            print("\nNo comprende hombre...")
            

# ---- MAIN PROGRAM

def restart():
    """ restart the game """
    #this is only run whenplayer gets to ROOM_END or ROOM_DEAD
    initialize_game()
    return True

def initialize_game():
    """real the map file into the world dictionary """
    global world
    
    YAML_FILE = "meredith.yaml"
    with open(YAML_FILE, "r") as f:
        world = yaml.load(f)
    f.close()

    bag = [] #set bag to be empty at start of game 


initialize_game()
set_location('ROOM_START')   #set location to ROOM_START  
play()