from collections import OrderedDict
import json
import mimetypes
import os
from pathlib import Path
import random
from typing import Union, Dict

import magic as magic_base 
import requests

RAWG_BASE_URL = "https://api.rawg.io/api"
ENDPOINTS = {"games": "games"}

PAGE_SIZE = 100
GAMES_ORDERING = "-added"
DATA_DIR_NAME = "D:\Anton\IgnoredDocuments\projects\game-genre\images"
CSV_LOCATION = "image-labels.csv"

magic = magic_base.Magic(magic_file="magic.mgc")

DATA_STRUCTURE = OrderedDict(**{
    "id": "id",
    "name": "name",
    "released": "released",
    "rating": "rating",
    "genres": "genres",
    "image_web": "background_image",
    "image_location": "file_location",
})


def get_games(page_number: int = 1, genre: Union[int, str] = None) -> bool:
    ensure_label_csv()
    return _get_games(page_number, genre)

def _get_games(page_number: int = 1, genre: Union[int, str] = None) -> bool:
    """
    Gets the next X games and analyses them.

    Arguments:
        page_number: Which page to take. Defaults to 1
        genre: The genre which to search for. Either the genre id or name
            No genre is no filtering. Defaults to None

    Return:
        Whether there is a next page
    """
    queryparams = {
        "page_size": PAGE_SIZE,
        "ordering": GAMES_ORDERING,
        "genre": genre,
        "page": page_number,
    }
    url = f"{RAWG_BASE_URL}/{ENDPOINTS['games']}"
    response = requests.get(url, params=queryparams)
    if response.status_code != 200:
        raise ValueError(
            "Something went wrong, the response status code was not 200 \n"
            + f"Request URL: {url}, parameters: {queryparams} \n"
            + f"Response text: {response.text} \n"
        )

    # with open("json.json", "w+") as f:
    #     f.write(json.dumps(response.json(), indent=4))

    if "results" not in response.json():
        raise ValueError(
            "There are no results in the response"
            + f"Request URL: {url}, parameters: {queryparams} \n"
            + f"Response text: {response.json()} \n"
        )

    response_json = response.json()
    games = response_json["results"]
    csv_text = ""
    for game in games:
        csv_text += post_process_game(game) + "\n"
    write_csv(csv_text)

    return bool(response_json.get("next", None))


def post_process_game(game_info: Dict):
    try:
        image_location = create_image(game_info)
    except magic_base.MagicException:
        return ""
    return append_to_csv(game_info, image_location)


def create_image(game_info):
    genres = game_info.get("genres", [])
    image = game_info.get("background_image", None)

    if not genres or not image:
        return

    image_response = requests.get(image)
    image_bytes = image_response.content
    mime_type = magic.from_buffer(image_bytes)
    extension = mimetypes.guess_extension(mime_type)

    file_location = generate_file_location(game_info, extension)
    write_file(image_bytes, file_location)

    return file_location


def generate_file_location(game_info: Dict, extension: str) -> Path:
    if extension is None:
        extension = ".jpg"  # Because why not

    ensure_image_dir()

    game_id = game_info["id"]
    genres_str = "_".join(map(lambda x: x["name"], game_info["genres"]))
    file_name = "-".join(map(str, [game_id, genres_str])) + extension

    file_location = Path(".") / DATA_DIR_NAME / file_name
    return file_location


def write_file(image, location):
    if os.path.exists(location):
        return
    with open(location, "wb+") as image_file:
        image_file.write(image)

def ensure_image_dir():
    os.makedirs(DATA_DIR_NAME, exist_ok=True)


def ensure_label_csv():
    if not os.path.exists(CSV_LOCATION):
        header_line = ",".join(DATA_STRUCTURE.keys()) + "\n"
        write_csv(header_line, create=True)


def append_to_csv(game_info, file_location):
    csv_items = []
    
    for key, value in DATA_STRUCTURE.items():
        if value == "file_location":
            csv_items.append(file_location)
        elif key == "genres":
            csv_items.append("-".join(map(lambda x: str(x["name"]), game_info[value])))
        else:   
            csv_items.append(game_info[value])
    csv_items = map(lambda x: str(x).replace(",", "."), csv_items)
    return ",".join(csv_items)

def write_csv(text, create=False):
    mode = "a+" if create else "a"
    with open(CSV_LOCATION, mode, encoding="utf-16") as csv_file:
        csv_file.write(text)
