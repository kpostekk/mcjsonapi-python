import cmd, json
from mcjson_api import *

config = json.load(open('config.json'))
worker = MinecraftApiWorker(config['host'], config['port'])


class MinecraftApiShell(cmd.Cmd):
    intro = 'Welcome in minecraft webapi shell! Type help or ? for list of all commands'

    def do_broadcast(self, arg):
        """
        Broadcasts messeage to the server
        example: broadcast yoyo im not giey
        """
        print(f'Broadcasting {arg}')
        worker.run_task(
            MinecraftApiTask(
                config['username'], config['password'],
                'chat.broadcast', [arg]
            )
        )

    def do_playersonline(self, arg):
        """
        Lists all players
        example: playersonline
        """
        players = worker.run_task(
            MinecraftApiTask(
                config['username'], config['password'],
                'players.online.names'
            )
        )['success']

        for player in players:
            print(player)

    def do_kick(self, arg):
        reason = input('The reason is... ')
        if reason.__len__() == 0:
            print('Using default message')
            reason = 'You were kicked by admin, thru his cmd'
        r = worker.run_task(
            MinecraftApiTask(
                config['username'], config['password'],
                'players.name.kick', [arg, reason]
            )
        )
        if r['is_success']:
            print(f'Kicked {arg} with reason {reason}')
        else:
            print(f'There were a problem with kicking {arg}')
            print(json.dumps(r, indent=2))


if __name__ == '__main__':
    MinecraftApiShell().cmdloop()
