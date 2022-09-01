# Plex-Rich-Presence

[![pypresence](https://img.shields.io/badge/using-pypresence-00bb88.svg?style=for-the-badge&logo=discord&logoWidth=20)](https://github.com/qwertyquerty/pypresence)

Python script for Plex integration with Discord

Plex Rich Presence allows you to display your current streaming activity on Plex to Discord.  It uses Discord's Rich Presence feature set a status message, similar to when playing a game. Utilizes Plex Webhooks (requires Plex Pass).

## Instructions to Run:
1. Navigate to project directory and edit file "config.ini"
   - Specify your Plex username
   - Specify local ip and an available port for your machine (the script does not need to run on the same machine as Plex or Plex Media Server but does need an open instance of discord)
4. Open Plex and navigate to account settings > Webhooks
   - Add a webhook to the machine that is running the script (should look something like http://IP:PORT)
6. Ensure that an instance of Discord is open and run the script
7. Your streaming activity should now be displayed on Discord
