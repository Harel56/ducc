import click
from urllib.parse import urlparse
from .api import run_parser, parsers
from ..utils import queue


@click.group()
def cli():
    pass


@cli.command()
@click.argument('name', type=click.Choice(tuple(parsers.keys())))
@click.argument('data', type=click.File())
def parse(name, data):
    """
    Accepts a parser name and a path to some raw data, as consumed from the message queue,
    and prints the results as published to the message queue
    """
    click.echo(run_parser(name, data.read()))


@cli.command('run-parser')
@click.argument('name', type=click.Choice(tuple(parsers.keys())))
@click.argument('url')
def cli_run_parser(name, url):
    """
    Accepts a parser name and url for the message queue.
    Runs the parser as a service, working with the message queue indefinitely.
    """
    o = urlparse(url, scheme="rabbitmq")
    if o.scheme == 'rabbitmq':
        def callback(ch, method, properties, body):
            return queue.publish(o.hostname, o.port, 'topic_logs', run_parser(name, body), 'topic', name)
        queue.consume(o.hostname, o.port, 'root', callback, 'fanout')
    else:
        # Scheme not supported
        raise click.UsageError("Unsupported scheme for the message queue url")


cli()