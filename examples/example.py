import json

from mcjson_api import *

# Reading config
cnf_file = json.load(open('config.json'))
login = cnf_file['username']
passwd = cnf_file['password']
host = cnf_file['host']
port = cnf_file['port']

if __name__ == '__main__':
    # Creating commands, which will be send to server
    calls = (
        ('players.online.names', []),
        ('players.offline.names', []),
        ('chat.broadcast', ['Admin bawi się API, wszystko jest ok']),
    )
    # Creating api client
    api = MinecraftApiWorker(host, port)

    # Preparing tasks
    for call in calls:
        api.add_task(
            MinecraftApiTask(login, passwd, call[0], call[1])
        )

    # Executing tasks
    print(
        json.dumps(
            api.do_tasks(),
            indent=2)
    )
