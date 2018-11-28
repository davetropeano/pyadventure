import sys, yaml, cmd

YAML_NAME = "meredith.yaml"
PROMPT = "> "

db = {}
location = {}

def set_location(tag):
    global location
    for x in db['locations']:
        if x[0] == tag:
            location = x[1]
            location["tag"] = tag

def print_location(long=True):
    d = location['description']['long'] if long == True else location['description']['short']
    print(d)
    # print_verbs()

def goto(location):
    set_location(location)

def do_action(action):
    cmd = action[0]
    param = action[1]

    if cmd.lower() == 'goto':
        goto(param)
        print_location()
    else:
        print("sorry, mi no comprende")

def move(cmd):
    # gross simplification because dead ends don't have explicit back actions
    if cmd.lower() == 'back':
        do_action(location['travel'][0]['action'])
        return

    for t in location['travel']:
        for v in t['verbs']:
            if cmd.lower() == v.lower():
                do_action(t['action'])
                break


def print_verbs():
    s = []
    for t in location['travel']:
        s.extend(t['verbs'])

    print(",".join(s))

def print_info():
    print(location)

def play():
    print_location()

    done = False
    while done == False:
        raw = input(PROMPT)
        if raw == 'quit':
            done = True
        elif raw == '?':
            print_info()
        elif raw == 'look':
            print_location(long=False)
        elif raw == 'words':
            print_verbs()
        else:
            move(raw.strip())

if __name__ == "__main__":
    with open(YAML_NAME, "r") as f:
        db = yaml.load(f)
    f.close()

    set_location('LOC_START')
    play()
# end
