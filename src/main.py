import click

from cli.commands import *

class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(
    AliasedGroup,
    options_metavar='[<options>]',
    subcommand_metavar='<command> [<args>]',
)


@click.version_option(message=f"Spotify-cli %(version)s")

def cli():
    pass


# commands:

cli.add_command(play)
