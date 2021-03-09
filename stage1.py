import requests

from env import config

s = requests.Session()
s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})

def get_room_id():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/rooms"

    data = {
        "title" : config["TESTING_ROOM_TITLE"]
    }

    resp = s.post(url, json=data)

    if resp.status_code == 200:
        config["TESTING_ROOM"] = resp.json()["id"]
    return config["TESTING_ROOM"]

def add_member(room_id, email):
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/memberships"

    data = {
        "roomId": room_id,
        "personEmail": email,
    }

    resp = s.post(url, json=data)

    if resp.status_code == 200:
        config["TESTING_ROOM"] = resp.json()["id"]
    return config["TESTING_ROOM"]

def post_message(room_id):
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/messages"

    data = {
        "roomId": room_id,
        "text": "Welcome! This is a safe space to share your best stories about our favourite viking",
    }

    resp = s.post(url, json=data)

if __name__ == "__main__":
    # ROOM_ID = get_room_id()
    ROOM_ID = config["TESTING_ROOM"]

    members = ["mneiding@cisco.com", "frewagne@cisco.com"]
    for member in members:
        add_member(ROOM_ID, member)
    post_message(ROOM_ID)