import click
import pika
from urllib.parse import urlparse
from .api import run_parser


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
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=o.hostname, port=o.port))
        channel = connection.channel()
        channel.exchange_declare(exchange='root', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='root', queue=queue_name)

        channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

        def callback(ch, method, properties, body):
            channel.basic_publish(exchange='topic_logs', routing_key=name, body=run_parser(name, body))

        # Waiting for logs
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()
    else:
        # Scheme not supported
        click.echo("Unsupported scheme for the url that is the second argument.")


cli()
