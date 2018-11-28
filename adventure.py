import yaml, sys

current_location = {}

def set_location(room):
    global current_location

    if room in world['ROOMS']:
        current_location = world['ROOMS'][room]
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
        print("around you are " + ",".join(current_location['items']))

def do_help():
    print("\nHELP!!!!!! -- to be defined later\n")

def do_hint():
    print("\nSeriously?! You want a hint in a lame ass game like this?\n")

def move(direction):
    whereto = direction.upper()
    if whereto in current_location['moves']:
        new_location = current_location['moves'][whereto]
        set_location(new_location)
        print_location()
    else:
        print("Hey! You can't go that way")

def play():
    done = False
    PROMPT = ">> "

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
        cmd = input(PROMPT)
        cmd = cmd.lower().strip()
        
        if cmd in DIRECTIONS:
            move(cmd)

        elif cmd == 'quit':
            raise SystemExit
        elif cmd == '?' or cmd == 'help':
            do_help()
        elif cmd == 'hint':
            do_hint()
        else:
            print("\nNo comprende hombre...")

        
        # execute_command(cmd)


# ---- MAIN PROGRAM

YAML_FILE = "meredith.yaml"
with open(YAML_FILE, "r") as f:
    world = yaml.load(f)
f.close()


set_location('ROOM_START')
play()
