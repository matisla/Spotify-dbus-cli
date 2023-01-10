import click


from spotify import Spotify


@click.command(options_metavar='[<options>]')
def play():
    sp = Spotify()
    sp.play()

@click.command(options_metavar='[<options>]')
def stop():
    sp = Spotify()
    sp.stop()
