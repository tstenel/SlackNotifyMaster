# Slack Notify Master

I have wanted to be able to set custom notification sounds per channel / users for a really long time, 
so I ended up making this python service :)

It plugs into dbus to get slack notification informations

## !!! you will need to disable the notification sound in your slack-desktop app to not have double notification sounds !!!

# Dependencies : 

On Debian, to install the dependencies : 

```
sudo apt install mplayer libcairo2-dev libglib2.0-dev build-essentials libdbus-1-dev libgirepository-2.0-dev 
```
# Configuration :

there is a yaml config file to fill up with your configuration

### Default section
 ```yaml
 default:
  notification: ~/Music/notifications/knock_brush.mp3  # path to the default notification
  volume: 150  # volume argument passed to mplayer, default 100 if not filled
 ```

### Adding groups

this is an example of a group `bots` that will have the same notification sound for all its member

group members can be channel names or usernames

members can only be in one group at a time

```yaml
bots:
  notification: ~/Music/notifications/flitterbug.mp3
  volume: 110
  members:
    - Slackbot
    - Commbot
    - Outlook Calendar
    - Deskare App
```