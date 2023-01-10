import subprocess

from typing import Union 

import dbus


class Spotify:
    interface_name: str = "org.mpris.MediaPlayer2.Player"
    property_interface_name: str = "org.freedesktop.DBus.Properties"
    bus_name = "org.mpris.MediaPlayer2.spotify"
    object_path = "/org/mpris/MediaPlayer2"

    def __init__(self) -> None:
        self.dbus = dbus.SessionBus()
        self.player = self.dbus.get_object(self.bus_name, self.object_path)
        self.interface = dbus.Interface(self.player, self.interface_name)
        self.property_interface = dbus.Interface(self.player, self.property_interface_name)

        for action in ["Play", "Pause", "PlayPause", "Next", "Previous"]:
            setattr(self, action.lower(), getattr(self.interface, action))

    @property
    def is_running(self) -> bool:
        """
        check if the spotify process is running

        :return: True if running, False otherwise
        """

        proc = subprocess.run(["pidof", "-s", "spotify"], capture_output=True)

        if proc.returncode == 0:
            return True

        return False

    def set_volume(self, level: Union[str, int]) -> None:
        """
        set the volume to a specific level

        :param level: the volume level in % [0;100]
        """

        if type(level) == int:
            pass

        elif level.startswith("+") or level.startswith("-"):
            level = self.get_volume() + int(level)

        percent = max(min(level, 100), 0) / 100
        self.property_interface.Set(self.interface_name, "Volume", percent)

    def get_volume(self) -> int:
        volume = self.property_interface.Get(self.interface_name, "Volume")
        return round(volume * 100)

    def properties(self) -> str:
        return self.property_interface.GetAll(self.interface_name)

    def metadata(self):
        return {
            k: v
            for k, v in self.player.Get(
                self.interface_name, "Metadata", dbus_interface=self.property_interface_name
            )
            or []
        }