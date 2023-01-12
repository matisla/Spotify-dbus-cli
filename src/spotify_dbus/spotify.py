import re

from typing import Dict, List

import dbus


class SpotifyNotRunningError(Exception):
    pass


def connected(func):
    def wrapper(self, *args, **kwargs):
        if not self.is_connected:
            raise SpotifyNotRunningError("Spotify is not running")
        return func(self, *args, **kwargs)

    return wrapper


class Spotify:
    interface_name: str = "org.mpris.MediaPlayer2.Player"
    property_interface_name: str = "org.freedesktop.DBus.Properties"
    bus_name = "org.mpris.MediaPlayer2.{}"
    object_path = "/org/mpris/MediaPlayer2"
    _connected = False

    def __init__(self):
        self.dbus = dbus.SessionBus()

    def connect(self, mediaplayer="spotify") -> None:
        try:
            self.player = self.dbus.get_object(self.bus_name.format(mediaplayer), self.object_path)
            self.interface = dbus.Interface(self.player, self.interface_name)
            self.property_interface = dbus.Interface(self.player, self.property_interface_name)
        except dbus.exceptions.DBusException:
            raise SpotifyNotRunningError()

        self._connected = True

    @connected
    def play(self) -> None:
        self.interface.Play()

    @connected
    def pause(self) -> None:
        self.interface.Pause()

    @connected
    def playpause(self) -> None:
        self.interface.PlayPause()

    @connected
    def next(self) -> None:
        self.interface.Next()

    @connected
    def previous(self) -> None:
        self.interface.Previous()

    @property
    def services(self) -> List[str]:
        """List of mediaplayer that are currently running"""

        services = []
        pattern = re.compile(r"org.mpris.MediaPlayer2.(?P<name>\w+)")

        for service in self.dbus.list_names() or []:

            match = pattern.match(str(service))

            if match:
                services.append(match.group("name"))

        return services

    @property
    def is_connected(self) -> bool:
        """
        check if the spotify is connected to the dbus

        :return: True if running, False otherwise
        """

        return self._connected

    @connected
    def set_volume(self, level: float) -> None:
        """
        set the volume to a specific level

        :param level: the volume level in % [0;1]
        """
        self.property_interface.Set(self.interface_name, "Volume", level)

    @connected
    def get_volume(self) -> int:
        """
        get the current volume level in % [0;100]
        """

        volume = self.property_interface.Get(self.interface_name, "Volume")
        return round(volume * 100)

    @connected
    def properties(self) -> str:
        return self.property_interface.GetAll(self.interface_name)

    @connected
    def metadata(self) -> Dict[str, str]:
        """
        Get the metadata of the current song.
        """
        metadata = {}

        if not self.is_connected:
            raise SpotifyNotRunningError()

        for key, value in (
            self.player.Get(
                self.interface_name, "Metadata", dbus_interface=self.property_interface_name
            )
            or {}
        ).items():

            key = key.replace("xesam:", "").replace("mpris:", "")

            if type(value) == dbus.Array:
                metadata[key] = ",".join([str(v) for v in value])
            else:
                metadata[key] = str(value)

        return metadata

    @connected
    def song(self, format="{artist} - {title}") -> str:
        """Return the current song in a specific format"""

        metadata = self.metadata()

        return format.format(**metadata)
