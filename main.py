import subprocess
import click
import os
import platform

@click.command()
def architecture():
    click.echo(platform.architecture())


if __name__ == "__main__":
    architecture()