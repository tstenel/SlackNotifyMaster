import os
import subprocess
import traceback

import dbus
import yaml
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

config = yaml.load(open('config.yaml'), Loader=yaml.SafeLoader  )
default_notification = os.path.expanduser(config["default"]["notification"])
default_volume = config["default"].get("volume", 100)
groups = {}
members = {}

for key, section in config.items():
    if key == "default":
        continue

    path = section["notification"]

    groups[key] = {
        "notification": os.path.expanduser(path),
    }
    if "members" in section:
        for member in section["members"]:
            if member in members:
                raise ValueError(f"Member '{member}' is already defined in group {members[member]}")
            members[member] = key

def play_sound(sound_path: str, volume: int = 100):
    subprocess.Popen(["mplayer", "-volume", str(volume), sound_path]).wait()

def handle_slack_message(args):
    try:
        for name, group in members.items():
            if name in args[3]:
                play_sound(groups[group]["notification"], groups[group].get("volume", default_volume))
                break
        else:
            play_sound(default_notification, default_volume)
    except Exception:
        print(traceback.format_exc())

def msg_cb(bus, msg):
    if msg.get_interface() == 'org.freedesktop.Notifications' and msg.get_member() == 'Notify':
        args = msg.get_args_list()

        if args[0] == "Slack":
            handle_slack_message(args)


def main():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    obj_dbus = bus.get_object('org.freedesktop.DBus',
                              '/org/freedesktop/DBus')
    obj_dbus.BecomeMonitor(["interface='org.freedesktop.Notifications'"],
                           dbus.UInt32(0),
                           interface='org.freedesktop.Notifications')

    bus.add_message_filter(msg_cb)

    mainloop = GLib.MainLoop()
    mainloop.run()

if __name__ == '__main__':
    main()



