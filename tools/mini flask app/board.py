from flask import Flask, Response, json, render_template, redirect, url_for
from mcjson_api import *
from ruamel import yaml

board = Flask(__name__)
api_conf = json.load(open('config.json'))
worker = MinecraftApiWorker(api_conf['host'], api_conf['port'])


@board.route('/')
def board_index():
    players_names = worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.online.names')
    )['success']
    return render_template('index.html', players=players_names)


@board.route('/yaml')
def board_yaml():
    players = worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.online')
    )
    return Response(yaml.dump(players['success']), mimetype='text/yaml')


@board.route('/json')
def board_json():
    players = worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.online')
    )['success']
    return Response(json.dumps(players), mimetype='text/json')


@board.route('/get/<name>')
def board_player(name):
    player = worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.name', [name])
    )['success']
    return render_template('player.html', player_name=name,
                           player_xp=player['experience'],
                           player_hp=player['health'],
                           player_food=player['foodLevel'],
                           player_op=player['op'],
                           player_uuid=player['uuid'],
                           player_coords=json.dumps(player['location'])
                           )


@board.route('/kick/<name>')
def board_kick(name):
    worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.name.kick', [name, 'You were kicked'])
    )
    return redirect(url_for('board_index'))


@board.route('/plain/coords/<name>')
def board_plain_coords(name):
    coords = worker.run_task(
        MinecraftApiTask(api_conf['username'], api_conf['password'], 'players.name', [name])
    )['success']['location']
    return Response(json.dumps(coords), mimetype='text/json')


if __name__ == '__main__':
    board.run(debug=True)
