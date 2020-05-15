import pika


def _ack_when_done(f):
    def wrapper(ch, method, properties, body):
        f(ch, method, properties, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    return wrapper


def publish(host, port, exchange, body, exchange_type='direct', routing_key=''):
    with pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port)) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        channel.basic_publish(exchange=exchange, routing_key=routing_key, body=body)


def consume(host, port, exchange, callback, exchange_type='direct', routing_key=None):
    with pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port)) as connection:
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)
        # Waiting for logs
        channel.basic_consume(queue=queue_name, on_message_callback=_ack_when_done(callback))
        channel.start_consuming()
