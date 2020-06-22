cmds = {
    'look': 'Look Around',
    'north': 'Go North',
    'south': 'Go South',
    'east': 'Go East',
    'west': 'Go West',
    }

exit_abbrevs = {
    'n': 'north',
    's': 'south',
    'e': 'east',
    'w': 'west',
    }


rooms = {
    'town_square_1': {
        'title': 'Town Square',
        'description': """
You are standing in the center of the town.
""",
        'exits': {
            'east': 'dirt_road_1',
            'west': 'town_narrow_1'
            }
        },
    'dirt_road_1': {
        'title': 'A Dirt Road',
        'description': """
You are standing on a dirt road off of town square.""",
        'exits': {
            'west': 'town_square_1'
            }
        },
    'town_narrow_1': {
        'title': 'A Narrow Alley',
        'description': """
You are in a narrow alley.  It is very dark.""",
        'exits': {
            'east': 'town_square_1'
            }
        },
    }

