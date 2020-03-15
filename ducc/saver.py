import click
import datetime as dt
import json
import pika
import pymongo
from urllib.parse import urlparse


class Saver:
    def __init__(self, database_url):
        self.database_url = database_url
        o = urlparse(database_url, scheme='mongodb')
        self.scheme = o.scheme
        if self.scheme == 'mongodb':
            client = pymongo.MongoClient(o.hostname, o.port)
            self.db = client.db
            self.users = self.db.users
            self.snapshots = self.db.snapshots
        else:
            pass

    def __repr__(self):
        return "Saver(%s)" % self.database_url

    def basic_save_mongo(self, topic: str, data):
        d = json.loads(data)
        self.users.replace_one(d["user"], d["user"], upsert=True)
        self.snapshots.update_one({"user_id": d["user"]["id"], "time": dt.datetime.fromtimestamp(d["timestamp"]/1000)},
                                  {'$set': {topic: d[topic]}, '$push': {"topics": topic}}, upsert=True)

    def save(self, topic, data):
        if self.scheme == 'mongodb':
            if topic in ('pose', 'color', 'depth', 'feelings'):
                self.basic_save_mongo(topic, data)
            else:
                pass  # Possible custom implementation for saving result from other parsers
        else:
            pass  # Unsupported scheme / database


@click.group()
def cli():
    pass


@cli.command()
@click.option('-d', '--database', help="url for the database")
@click.argument('topic')
@click.argument('data', type=click.File())
def save(database, topic, data):
    Saver(database).save(topic, data.read())


@cli.command()
@click.argument('database', help="url for the database")
@click.argument('queue')
def run_saver(database, queue):
    o = urlparse(queue, scheme="rabbitmq")
    if o.scheme == 'rabbitmq':
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=o.hostname, port=o.port))
        channel = connection.channel()
        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key='#')

        saver = Saver(database)

        def callback(ch, method, properties, body):
            saver.save(method.routing_key, body)

        # Waiting for logs
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()
    else:
        # Scheme not supported
        click.echo("USAGE")


if __name__ == "__main__":
    cli()
