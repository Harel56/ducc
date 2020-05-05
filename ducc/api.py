import click
import flask
import pymongo
from bson.objectid import ObjectId
from urllib.parse import urlparse


app = flask.Flask(__name__)
client = None


@app.route('/users')
def users():
    return str(list(client.db.users.find({}, {'id': 1, 'name': 1})))


@app.route('/')
def home():
    return flask.redirect(flask.url_for('users'))


@app.route('/users/<int:userID>')
def user_details(userID: int):
    return str(client.db.users.find_one({'id': userID}))


@app.route('/users/<int:userID>/snapshots')
def snapshots(userID: int):
    return str(list(client.db.snapshots.find({'user_id': userID}, {'time': 1})))


@app.route('/users/<int:userID>/snapshots/<snapshotID>')
def snapshot_details(userID: int, snapshotID):
    return str(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID}, {'user_id': 1, 'time': 1, 'topics': 1}))


@app.route('/users/<int:userID>/snapshots/<snapshotID>/pose')
def pose(userID: int, snapshotID):
    return str(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID}, {'pose': 1})['pose'])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/color-image')
def color(userID: int, snapshotID):
    return str(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID}, {'color': 1})['color'])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/depth-image')
def depth(userID: int, snapshotID):
    return client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID}, {'depth': 1})['depth']


@app.route('/users/<int:userID>/snapshots/<snapshotID>/feelings')
def feelings(userID: int, snapshotID):
    return str(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID}, {'feelings': 1})['feelings'])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/color-image/data')
def color_data(userID: int, snapshotID):
    return flask.send_file(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})['color'][2])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/depth-image/data')
def depth_data(userID: int, snapshotID):
    return flask.send_file(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})['depth'][2])


def run_api_server(host, port, database_url):
    global client
    o = urlparse(database_url, scheme='mongodb')
    if o.scheme == 'mongodb':
        client = pymongo.MongoClient(o.hostname, o.port)
    else:
        return
    app.run(host, port)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=5000)
@click.option('-d', '--database', default='mongodb://localhost:27017/')
def run_server(host, port, database):
    run_api_server(host, port, database)


if __name__ == "__main__":
    cli()
