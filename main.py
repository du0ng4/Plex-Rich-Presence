
import os
import flask
import pypresence
import configparser
import json, pprint, threading

pp = pprint.PrettyPrinter(indent=2)

# Config
parser = configparser.ConfigParser()
parser.read("config.ini")
PLEX_USERNAME = parser.get("listener", "plex_username")
IP = parser.get("listener", "host_ip")
PORT = parser.getint("listener", "port")
DISPLAY_WEBHOOKS = parser.getboolean("listener", "display_webhooks")
CLIENT_ID = parser.get("presence", "client_id")

PAYLOAD = {"event": None, "Metadata": {"type": None} }

"""
    LISTENER

    Listens for webhooks from Plex Media Server
    Stores received payload in Python dictionary form in global variable PAYLOAD
"""

app = flask.Flask(__name__)

@app.route("/", methods=["POST"])
def listen():
    global PAYLOAD
    temp = json.loads(flask.request.form["payload"])
    if temp["Account"]["title"] == PLEX_USERNAME:
        PAYLOAD = json.loads(flask.request.form["payload"])
        if DISPLAY_WEBHOOKS is True:
            pp.pprint(PAYLOAD)
    return "OK"

"""
    PRESENCE SETTER

    Takes updated information from global variable PAYLOAD to determine user's current
    state and determines whether to set presence to Discord
"""

RPC = pypresence.Presence(CLIENT_ID)
RPC.connect()

valid_types = [ # supported media types
    "movie",
    "episode"
]

valid_events = [ # events that are considered "currently watching"
    "media.play",
    "media.resume"
]


def get_state():
    global PAYLOAD   
    event = PAYLOAD["event"]
    type = PAYLOAD["Metadata"]["type"]
    watching = event in valid_events and type in valid_types
    return watching, type


def extract_movie_info(): # used for movies
    global PAYLOAD
    title = PAYLOAD["Metadata"]['title']
    year = str(PAYLOAD["Metadata"]['year'])
    return title, year


def extract_episode_info(): # used for tv shows
    global PAYLOAD
    title = PAYLOAD["Metadata"]["grandparentTitle"]
    season = str(PAYLOAD["Metadata"]["parentIndex"])
    episode = str(PAYLOAD["Metadata"]["index"])
    return title, season, episode


# thread function to set presence
def set_presence():
    while True:
        watching, type = get_state()
        if watching is True:
            if type == "movie":
                title, year = extract_movie_info()
                text1 = "Watching " + title
                text2 = year  
            elif type == "episode":
                title, season, episode = extract_episode_info()
                text1 = "Watching " + title
                text2 = "On Season " + season + " Episode " + episode
            RPC.update(state=text2, details=text1, large_image="icon")
        else:
            RPC.clear(pid=os.getpid())


if __name__ == "__main__":
    print("PID: ", os.getpid())
    thread = threading.Thread(target=set_presence)
    thread.start()
    app.run(host=IP, port=PORT)
