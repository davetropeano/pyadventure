import yaml, sys

current_location = {}
previous_locations = []
total_moves = 0
bag = []

def do_back():
    global total_moves, current_location

    # the first previous location will be an empty dictionary {}
    # because when set_location() is called it pushes the current location
    # and initially the current location is empty... 
    # so to test for previous locations you know the len > 1
    if len(previous_locations) > 1:
        current_location = previous_locations.pop()
        total_moves = total_moves+1
        print_location()
    else:
        print("There is nowhere to go back to!")

def set_location(room):
    global current_location, total_moves

    if room in world['ROOMS']:
        previous_locations.append(current_location)
        current_location = world['ROOMS'][room]
        total_moves = total_moves+1
    else:
        print("LOSER - this room %s doesn't exist!" % room)

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
        items = current_location['items']
        if len(items):
            print("This is what you see around you: " + ",".join(current_location['items']))

def do_help():
    print("\nHELP!!!!!! -- to be defined later\n")

def do_hint():
    print("\nSeriously?! You want a hint in a lame ass game like this?\n")

def check_door():
    print("\nThrough some SERIOUS python voodoo I am running a function that was listed by name in a YAML text file... this is well above my mortal abilities but hey it works!")
    return True

def move(direction):
    ok_to_move = True
    whereto = direction.upper()

    if whereto in current_location['moves']:
        if 'checks' in current_location and whereto in current_location['checks']:
            fn = current_location['checks'][whereto]
            ok_to_move = globals()[fn]() # DANGER - SERIOUS VOODOO REFLECTION
        if ok_to_move:
            new_location = current_location['moves'][whereto]
            set_location(new_location)
            print_location()
        else:
            print("Hmm... you legs feel heavy and you can't move. You have this sudden feeling this is something you need to do first...")
    else:
        print("Hey! You can't go that way")

def get_command():
    PROMPT = ">> "
    s = input(PROMPT)
    words = s.strip().split(' ')

    cmd = words[0].lower().strip()
    obj = ' '.join(words[1:]).lower().strip()

    return words[0], ' '.join(words[1:])

def do_drop(obj):
    global current_location, bag
    if obj in bag:
        current_location['items'].append(obj)
        bag.remove(obj)
        total_moves = total_moves+1
    else:
        print('ARGH! There is no %s in your bag!' % obj)

def do_take(obj):
    global current_location, bag, total_moves
    if obj in current_location['items']:
        bag.append(obj)
        current_location['items'].remove(obj)
        total_moves = total_moves+1
    else:
        print('ARGH! There is no %s to take around here!' % obj)

def do_inventory():
    print("\nLet's see... in your bag you have:")
    if len(bag) == 0:
        print("Nothing. Zip. Nada. Zilch. You don't have a single thing.")
    else:
        for item in bag:
            print("\t" + item)

def do_look(obj):
    if obj:
        if obj in bag:
            print("I am looking at the %s" % obj)
        else:
            print("Ummmm... you don't have %s in your bag..." % obj)
    else:
        print_location()

def play():
    done = False

    DIRECTIONS = [
        'north',
        'south',
        'east',
        'west',
        'northeast',
        'southeast',
        'northwest',
        'southwest',
        'up',
        'down'
    ]

    print_location()
    while not done:
        cmd, obj = get_command()
        
        if cmd in DIRECTIONS:
            move(cmd)

        elif cmd == 'back':
            do_back()
        elif cmd == 'take':
            do_take(obj)
        elif cmd == 'drop':
            do_drop(obj)
        elif cmd == 'inventory':
            do_inventory()
        elif cmd == 'look':
            do_look(obj)
        elif cmd == 'quit':
            raise SystemExit
        elif cmd == '?' or cmd == 'help':
            do_help()
        elif cmd == 'hint':
            do_hint()
        else:
            print("\nNo comprende hombre...")


# ---- MAIN PROGRAM

YAML_FILE = "meredith.yaml"
with open(YAML_FILE, "r") as f:
    world = yaml.load(f)
f.close()


set_location('ROOM_START')
play()
