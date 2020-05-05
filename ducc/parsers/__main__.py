import click
import pika
from urllib.parse import urlparse
from .api import run_parser


def publish(name, body, conn_params):
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
    channel.basic_publish(exchange='topic_logs', routing_key=name, body=run_parser(name, body))
    connection.close()


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name')
@click.argument('data', type=click.File())
def parse(name, data):
    click.echo(run_parser(name, data.read()))


@cli.command('run-parser')
@click.argument('name')
@click.argument('url')
def cli_run_parser(name, url):
    o = urlparse(url, scheme="rabbitmq")
    if o.scheme == 'rabbitmq':
        connection_params = pika.ConnectionParameters(host=o.hostname, port=o.port)
        connection = pika.BlockingConnection()
        channel = connection.channel()
        channel.exchange_declare(exchange='root', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='root', queue=queue_name)

        #channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        def callback(ch, method, properties, body):
            publish(name, body, connection_params)
            #channel.basic_publish(exchange='topic_logs', routing_key=name, body=run_parser(name, body))

        # Waiting for logs
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()
    else:
        # Scheme not supported
        raise click.BadParameter("Unsupported scheme for the message queue url", param='url')


cli()
