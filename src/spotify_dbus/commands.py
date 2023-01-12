import click

from typing import Optional

from .spotify import Spotify, SpotifyNotRunningError


def get_spotify():

    sp = Spotify()

    if not sp.is_connected:
        try:
            sp.connect()
        except SpotifyNotRunningError:
            raise click.ClickException("Spotify is not running")

    return sp


@click.command()
def play() -> None:
    """
    start playing the current song
    """
    sp = get_spotify()
    sp.play()


@click.command()
def pause() -> None:
    """
    stop playing the current song
    """
    sp = get_spotify()
    sp.pause()


@click.command()
def toggle() -> None:
    """
    if the song is playing, pause it, otherwise play it
    """
    sp = get_spotify()
    sp.playpause()


@click.command()
def next() -> None:
    """
    play the next song
    """
    sp = get_spotify()
    sp.next()


@click.command()
def previous() -> None:
    """
    play the previous song
    """
    sp = get_spotify()
    sp.previous()


@click.command()
@click.option(
    "--format",
    default="{artist} - {title}",
    type=str,
    help=(
        "format of the song name, filled with value get from `metadata`. "
        "default: '{artist} - {title}'"
    ),
)
def song(format) -> None:
    """
    print the current song name
    """
    sp = get_spotify()
    text = sp.song(format)
    click.echo(text)


@click.command()
@click.argument("amount", type=str, required=False)
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
    sp = get_spotify()

    if amount is None:
        click.echo(f"Volume: {sp.get_volume()}%")
        return

    elif amount.startswith("+") or amount.startswith("-"):
        level = sp.get_volume() + int(amount)

    else:
        level = int(amount)

    percent = max(min(level, 100), 0) / 100
    sp.set_volume(percent)


@click.command()
def metadata():
    """
    get Metadata from Spotify
    """
    sp = get_spotify()
    for key, value in sp.metadata().items():
        click.echo(f"{key}: {value}")


@click.command()
def services():
    """
    get all available MediaPlayers
    """
    sp = Spotify()
    for service in sp.services:
        click.echo(service)
