import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

from env import config

s = requests.Session()
s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})

def get_nb_meetings():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/meetings"

    resp = s.get(url)

    if resp.status_code == 200:
        return len(resp.json()["items"])
    return 0

def create_meeting():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/meetings"

    data = {
        "title": "Stien Vanderhallen appreciation moment",
        "start": "2021-03-10 14:00:00",
        "end": "2021-03-10 15:00:00",
        "enabledAutoRecordMeeting": False,
        "invitees": [
            {
                "email": "paholse@cisco.com",
                "displayName": "Patrick Holse",
                "coHost": True
            }
        ],
        "hostEmail": "stienvan@cisco.com",
    }

    resp = s.post(url, json=data)

def get_rooms():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/rooms?max=1000"
    resp = s.get(url)

    if resp.status_code == 200:
        return resp.json()["items"]
    return 0

def get_nb_messages(room_id):
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/messages?roomId={room_id}&max=20000"
    resp = s.get(url)

    if resp.status_code == 200:
        return len(resp.json()["items"])
    return 0

def get_nb_spaces():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/memberships?max=1000"
    resp = s.get(url)

    if resp.status_code == 200:
        return len(resp.json()["items"])
    return 0

def post_markdown_message(room_id, nb_meetings, mess_spaces, nb_spaces):
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/messages"

    data = {
        "roomId": room_id,
        "markdown": \
            " ## If you like it, put a number on it" +
            " \n \n **Number of meetings I scheduled:** " + str(nb_meetings) +
            " \n \n **Number of spaces I am in:** " + str(nb_spaces),
    }

    resp = s.post(url, json=data)

    m = MultipartEncoder({'roomId': room_id,
                      'text': "Please don't judge me",
                      'files': ('messages.json', open('messages.json', 'rb'),
                      'application/json')})

    m_headers = {
        'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}",
        "Content-Type": m.content_type
    }
    
    resp = s.post(url, data=m, headers=m_headers)

if __name__ == "__main__":
    # create_meeting()
    NB_MEETINGS = get_nb_meetings()
    NB_SPACES = get_nb_spaces()

    MESS_PER_ROOM = {}
    # ROOMS = get_rooms()
    # for room in ROOMS:
    #     MESS_PER_ROOM[room["title"]] = get_nb_messages(room["id"])
    with open('messages.json') as json_file:
        MESS_PER_ROOM = json.load(json_file)

    post_markdown_message(config["TESTING_ROOM"], NB_MEETINGS, MESS_PER_ROOM, NB_SPACES)

    # with open("messages.json", "w") as f:
    #     f.write(json.dumps(MESS_PER_ROOM, indent=2))
    #     f.close()