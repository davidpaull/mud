import world

# Terminal Colors
red = '\u001b[31m'
green = '\u001b[32m'
reset = '\u001b[0m'


class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = None
        self.location = 'town_square_1'

        self.max_hp = 100
        self.max_mp = 100
        self.hp = 100
        self.mp = 100

    def send_message(self, msg):
        msg = msg + '\n> '
        self.conn.sendall(msg.encode())

    def get_exits(self):
        if self.location in world.rooms:
            return [i[0] for i in world.rooms[self.location]['exits'].keys()]
        return []

    def send_room_desc(self):
        abb_exits = []
        player_bar = '{}hp {}mp'.format(self.hp, self.mp)
        room_title = world.rooms[self.location]['title'].upper()
        room_desc = world.rooms[self.location]['description']
        exits = self.get_exits()
        for exit in exits:
            abb_exits.append(exit[0])
        exits = ','.join(abb_exits)

        msg = f"""
{green}{player_bar}{reset}
{room_title}
{room_desc.strip()}
[Exits: {exits}] 
"""

        self.send_message(msg)
        """
        title = '-= {} =-'.format(world.rooms[self.location]['title'].upper())
        desc = world.rooms[self.location]['description']
        exits = self.get_exits()
        abb_exits = []
        for exit in exits:
            abb_exits.append(exit[0])
        exits = ','.join(abb_exits)

        ret = '\n{}\n{}\nExits: {}\n> '.format(title, desc, exits)
        return ret
        """





