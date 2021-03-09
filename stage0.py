import requests

from env import config

s = requests.Session()
s.headers.update({
    'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"
})

def get_room_id():
    WEBEX_BASE_URL = config['WEBEX_BASE_URL']
    url = f"{WEBEX_BASE_URL}/v1/rooms"
    resp = s.get(url)

    if resp.status_code == 200:
        for room in resp.json()["items"]:
            if room["title"] == config["PRODUCTION_ROOM_TITLE"]:
                config["PRODUCTION_ROOM"] = room["id"]
                return config["PRODUCTION_ROOM"]
    return 0

if __name__ == "__main__":
    get_room_id()
    print(f'Found production room ID: {config["PRODUCTION_ROOM"]}')