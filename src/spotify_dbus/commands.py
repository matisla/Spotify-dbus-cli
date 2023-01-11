import click

from typing import Optional


from .spotify import Spotify

@click.command()
def play():
    """
    start playing the current song
    """
    sp = Spotify()
    sp.play()

@click.command()
def pause():
    """
    stop playing the current song
    """
    sp = Spotify()
    sp.pause()

@click.command()
def toggle():
    """
    if the song is playing, pause it, otherwise play it
    """
    sp = Spotify()
    sp.playpause()

@click.command()
def next():
    """
    play the next song
    """
    sp = Spotify()
    sp.next()

@click.command()
def previous():
    """
    play the previous song
    """
    sp = Spotify()
    sp.previous()

@click.command()
@click.argument('amount', type=str, required=False)
def volume(amount) -> Optional[int]:
    """
    If `amount` is specified, set the volume accordingly to `amount`.
    The `amount` can be absolut or relative by speficying a `+` or `-` before the amount.
    Otherwise the current volume level of spotify is returned.

    amount: volume level in % [0;100]

    Examples:

        volume 50  # set the volume to 50%  

        volume +10  # increase the volume by 10% 

        volume -10  # decrease the volume by 10% 

        volume  # get the current volume level 
    """
    sp = Spotify()

    if amount is None:
        click.echo(f"Volume: {sp.get_volume()}%")
        return
    
    if amount.startswith("+") or amount.startswith("-"):
        level = sp.get_volume() + int(amount)
    else:
        level = int(amount)

    percent = max(min(level, 100), 0) / 100
    sp.set_volume(percent)


