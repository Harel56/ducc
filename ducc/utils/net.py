import click


class SafetyNet:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and not issubclass(exc_type, (EOFError, KeyboardInterrupt, click.ClickException)):
            raise click.ClickException(str(exc_val))
