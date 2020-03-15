import datetime as dt
import flask
import pymongo
from bson.objectid import ObjectId
from urllib.parse import urlparse


app = flask.Flask(__name__)
client = None


@app.route('/users')
def users():
    found = client.db.users.find({}, {'_id': 0, 'id': 1, 'name': 1})
    return flask.render_template('users.html', users=found)


@app.route('/users/<int:userID>')
def user(userID: int):
    found = client.db.users.find_one({'id': userID})
    return flask.render_template('user.html', user=found, birth=dt.date.fromtimestamp(found['birthday']))


@app.route('/users/<int:userID>/snapshots')
def snapshots(userID: int):
    user = client.db.users.find_one({'id': userID})
    found = client.db.snapshots.find({'user_id': userID}, {'time': 1})
    return flask.render_template('snapshots.html', user=user, snapshots=found)


@app.route('/users/<int:userID>/snapshots/<snapshotID>')
def snapshot(userID: int, snapshotID):
    found = client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})
    return flask.render_template('snapshot.html', snapshot=found)


@app.route('/users/<int:userID>/snapshots/<snapshotID>/color')
def color(userID: int, snapshotID):
    return flask.send_file(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})['color'])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/depth')
def depth(userID: int, snapshotID):
    return flask.send_file(client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})['depth'])


@app.route('/users/<int:userID>/snapshots/<snapshotID>/next')
def next(userID: int, snapshotID):
    og = client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})
    found = min((i for i in client.db.snapshots.find({'user_id': userID}) if og['time'] < i['time']), default=og)
    return flask.redirect(flask.url_for('snapshot', userID=found['user_id'], snapshotID=found['_id']))


@app.route('/users/<int:userID>/snapshots/<snapshotID>/prev')
def prev(userID: int, snapshotID):
    og = client.db.snapshots.find_one({'_id': ObjectId(snapshotID), 'user_id': userID})
    found = max((i for i in client.db.snapshots.find({'user_id': userID}) if og['time'] > i['time']), default=og)
    return flask.redirect(flask.url_for('snapshot', userID=found['user_id'], snapshotID=found['_id']))


def run_server(host, port, database_url):
    global client
    o = urlparse(database_url, scheme='mongodb')
    if o.scheme == 'mongodb':
        client = pymongo.MongoClient(o.hostname, o.port)
    else:
        return  # Unsupported scheme / database
    app.run(host, port)
