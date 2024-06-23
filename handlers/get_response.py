import requests
import json
import logging


def top10(text: str):
    res = requests.get(f"http://mutagen.space/api/v1/search/find", params={"query": text})
    if res.status_code == 200:
        data = res.content.decode()
        return json.loads(data)
    else:
        logging.error(f"Some error occured: {res.status_code}:{res.text}")

