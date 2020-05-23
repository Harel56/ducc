import click
import logging
from urllib.parse import urlparse
from .api import run_parser, parsers
from ..utils import queue, net


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
    with net.SafetyNet():
        click.echo(run_parser(name, data.read()))


@cli.command('run-parser')
@click.option('--log/--no-log', default=True)
@click.argument('name', type=click.Choice(tuple(parsers.keys())))
@click.argument('url')
def cli_run_parser(name, url, log):
    """
    Accepts a parser name and url for the message queue.
    Runs the parser as a service, working with the message queue indefinitely.
    """
    with net.SafetyNet():
        o = urlparse(url, scheme="rabbitmq")
        if o.scheme == 'rabbitmq':
            def callback(ch, method, properties, body):
                if log:
                    logging.info("Received message from queue")
                queue.publish(o.hostname, o.port, 'topic_logs', run_parser(name, body), 'topic', name)
                if log:
                    logging.info("Sent message to queue")
            queue.consume(o.hostname, o.port, 'root', callback, 'fanout')
        else:
            # Scheme not supported
            raise click.UsageError("Unsupported scheme for the message queue url")


if __name__ == "__main__":
    cli(prog_name="python -m ducc.parsers.cli")
