#!/usr/bin/env python3

import socket, time, sys, threading, signal
import world, player


ip_addr = '127.0.0.1'
port = 5001

active_clients = []
players = []

debug = True

def db(data):
    """ Prints data if debug is True
    """
    if not debug:
        return False

    print(data)

def _proc(data):
    return data.decode().strip()

def player_worker(conn, addr, player_lock, MAX_BUFF=4096):
    """ Main player worker thread
    """
    conn.sendall('Connection Accepted\n'.encode())
    print('Connection accepted from {}'.format(addr))

    pl = player.Player(conn, addr)
    with player_lock:
        players.append(pl)

    pl.send_room_desc()
    # main loop: receive / send data
    while True:
        data = conn.recv(MAX_BUFF)
        if not data:
            break
        input = _proc(data)
        moved = False

        if input in  ('quit', 'exit', 'bye'):
            break
        elif input == 'look':
            #msg = game.get_room_description(pl.location)
            #pl.send_message(pl.get_room_desc())
            pl.send_room_desc()
        elif input in ('n', 'e', 's', 'w'):
            #exits = game.get_exits(pl.location)
            exits = pl.get_exits()
            if input in exits:
                with player_lock:
                    # move character to that room
                    mv_cmd = world.exit_abbrevs.get(input)
                    pl.location = world.rooms[pl.location]['exits'][mv_cmd]
                    #msg = pl.get_room_desc()
                    moved = True

            # If we moved the player, let's send a message to those in his room as well
            if moved:
                #conn.sendall(msg.encode())
                pl.send_room_desc()
                with player_lock:
                    for p in players:
                        # don't send it if the player is the one that entered :D
                        if p is pl:
                            continue
                        if p.location == pl.location:
                            p.send_message('{} has entered the room.'.format(pl.name))


    # Broke out of main player loop - so clean up here
    conn.close()
    active_clients.remove(addr)
    print('Connection ended for {}'.format(addr))
    print('Active Clients: [{}]'.format(len(active_clients)))
    # players.remove pl...
    for client in active_clients:
        print('  {}'.format(client))

def conn_listener_worker():
    """ Network listener thread - listens for connections, essentially
    """
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('conn_listener_worker thread started...')

    try:
        soc.bind((ip_addr, port))
        print('Socket bind complete')
    except Exception as e:
        print('Bind failed. Error: {}'.format(str(e)))

    soc.listen()
    print('Socket Listening...')

    # main loop to accept connections
    while True:
        try:
            conn, addr = soc.accept()
        except:
            sys.exit(0)
        print('Accepting connection from {}'.format(addr))
        active_clients.append(addr)
        try:
            thread = threading.Thread(target=player_worker, args=(conn, addr, player_lock))
            thread.setDaemon(True)
            thread.start()
        except Exception as e:
            print('Thread Error: {}'.format(str(e)))
        print('Active Clients: [{}]'.format(len(active_clients)))
        for client in active_clients:
            print('  {}'.format(client))

    print('CLOSING SOCKET')
    soc.close()

if __name__ == '__main__':
    server_thread = threading.Thread(target=conn_listener_worker)
    server_thread.setDaemon(True)
    server_thread.start()

    player_lock = threading.Lock()

    tick_counter = 0
    # main game world loop
    while True:
        tick_counter += 1
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('Shutting down!')
            sys.exit(0)
        db('game tick [{}]'.format(tick_counter))
        db('clients: [{}]'.format(len(active_clients)))


