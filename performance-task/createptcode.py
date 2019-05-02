"""
I define the map of my game in a text file outline called a YAML file. YAML is just a specific way to write an outline that can easily be read
and converted to python dictionaries and lists. There is a library called yaml that lets me read the YAML file and convert it to a dictionary.
That way I can have 1000 maps but only one program.

sys is another python library. I use it to read the YAML file
"""
import yaml, sys

world = {} 
current_location = {} 
bag = []

did_sign = False #did they look at the signs at the intersection
did_die = False #did they die and the game restarted
did_calendar = False #did they take the calendar from the town hall
did_key = False #did they use the key to unlock the door
did_note = False #did they have the note to unlock the safe
did_document = False #did they have the documents to give to the boss
did_camera = False #did they have the camera in the sad ending

def set_location(room):
    
    global current_location
    
    if room in world['ROOMS']:
        current_location = world['ROOMS'][room]
    else:
        print("LOSER - this room %s doesn't exist!" %room)
        
def get_location(loc):
    
    place = { "name": "The Void" }
    if loc in world['ROOMS']:
        place = world['ROOMS'][loc]
    
    return place

def print_location():
       
    print('') 
    print(current_location['name'])
    print('=' * len(current_location['name'])) 
    print(current_location['description'])
    print('')
    
    if 'moves' in current_location:
        moves = current_location['moves']
        for direction in moves:
            location = get_location(moves[direction])
            print("%s: %s" % (direction, location["name"]))
    print('')
    
    if 'items' in current_location:
        if len(current_location['items']) > 0:
            print("you can see the following: " + ", ".join(current_location['items']))

def do_help():
        print("\nHere is the list of available movement commands: north, south, east, west")
        print("In addition, you can TAKE an object, DROP an object, LOOK at an object (or just say look and it will show you where you are),")
        print("INVENTORY to get a list of items in your bag. Oh, and QUIT. Quits the game.")

def do_hint():
      print("\nSeriously?! You want a hint in a lame game like this?\n")
      
def do_take(obj):
    if obj in current_location['items']:
        bag.append (obj)
        current_location['items'].remove (obj)
        inventory()
    else:
        print("\nHey! That item is not here.\n")
        
def inventory():
    if len(bag) > 0: 
        print("\nYou have the following in your bag:")
        for item in bag:
            print("\t" + item)
    else:
        print("\nYour bag is empty. Go to Whole Foods.\n") 
      
def do_drop(obj):
    if obj in bag: 
        bag.remove (obj)
        current_location['items'].append (obj)
        inventory() 
    else:
        print("\nWhat'chu talking bout Willis? I don't have that.\n") 
    
def check_fog_sign():
     if "goggles" in bag:
        print("\nThe signs are hard to see. But you have night goggles! You use them to look at the signs at the intersection and pick which way to go.\n")
        bag.remove("goggles")
        return True          
     else:
        return False

def check_calendar():
    if "calendar" in bag:
        print("\nWhoops. You stole and the police saw you. You got an unfair jury and were locked up for life, and died in prison. The end.\n")
        
        return True
    else:
        print("\nYou move on to see a wall of TVs going on about the news.\n")
        return False
              
def check_key():
    if "key" in bag:
        print("\nThe door is locked. But you have a key! In a remarkable example of engineering brillance, you use the key to unlock the door.\n")
        bag.remove("key")
        return True
    else:
        return False

def check_document():
    if "document" in bag:
        print("\nYou hand over the documents to your boss and hope he will read them in time.\n")
        return True
    else:
        return False

def check_camera():
    if "camera" in bag:
        print("\nYou grab your camera and get ready to set up.\n")
        return True
    else:
        return False

def do_look(obj):
    global did_note, did_document, did_calendar
    
    if obj:
        if obj in bag:
            if obj == 'note':
                print("You read the note and it says '3927'. Hmmmmmm...")
                did_note = True 
            elif obj == 'document':
                print("You look at the document and see it shows the the O-rings will break once they reach cold temperatures. It's very cold out today. This makes you nervous. Hmmmmm...")
                did_riddle = True 
            else:
                print("You look at the %s and see nothing special" % obj)
        else:
            print("Umm... you can't look at something you don't have")
    else:
        print_location()  
        
def move(direction):
   
    global did_die
    
    ok_to_move = True
    whereto = direction.upper()

    if whereto in current_location['moves']:
        if 'checks' in current_location and whereto in current_location['checks']:
            fn = current_location['checks'][whereto]
            ok_to_move = globals()[fn]() 
        if ok_to_move: 
            new_location = current_location['moves'][whereto]
            set_location(new_location)
            print_location()
        else:
            if did_die == False:
                print("Hmm... you legs feel heavy and you can't move. You have this sudden feeling this is something you need to do first...")
            else:
                did_die = False
                set_location("ROOM_DEAD1")
                
    else:
        print("Hey! You can't go that way")

def get_command():
    PROMPT = ">> "
    s = input(PROMPT) 
    words = s.lower().strip().split(' ') 

    cmd = words[0].lower().strip() 
    obj = ' '.join(words[1:]).lower().strip()
    return cmd, obj

def play():
    done = False

    DIRECTIONS = [ 
        'north',
        'south',
        'east',
        'west',
        'yes',
        'no',
        'restart'
    
    ]

    print_location() 
    while not done:
        cmd, obj = get_command()
        
        if cmd in DIRECTIONS:
            move(cmd)
            
        
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
        else:
            print("\nNo comprende hombre...")
            

# ---- MAIN PROGRAM

def restart():
    initialize_game()
    return True

def initialize_game():
    global world, bag
    
    YAML_FILE = "createperformancetaskyaml.yaml"
    with open(YAML_FILE, "r") as f:
        world = yaml.load(f)
    f.close()

    bag = [] 

initialize_game()
set_location('ROOM_START')
play()  
