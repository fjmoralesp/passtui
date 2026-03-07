import click
from passtui.app import PassTUI


@click.command()
def cli():
    app = PassTUI()
    app.run()
