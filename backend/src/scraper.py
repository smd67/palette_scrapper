import requests
from bs4 import BeautifulSoup, Tag, NavigableString

import pprint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, List
import pandas as pd

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PaletteGroup(BaseModel):
    text: str
    value: str

class Palette(BaseModel):
    palette_name: str
    color_list: List[str]

class PaletteQuery(BaseModel):
    """
    Pydantic representation of a query.
    """
    url: str

@app.get("/get-palette-groups/")
def get_palette_groups() -> List[PaletteGroup]:
    data = []
    base_url = 'https://www.color-hex.com'
    url = f"{base_url}/color-palettes/"
    response = requests.get(url)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    elements_with_class = soup.find('div', class_="taglistDiv")
    for element in elements_with_class.contents:
        if isinstance(element, Tag):
            group_name = element['title']
            href = element['href']
            group_url = f"{base_url}{href}"
            data.append({"text": group_name, "value": group_url})
    data.append({"text": "popular", "value": "https://www.color-hex.com/color-palettes/popular.php"})
    data.append({"text": "random", "value": "https://www.color-hex.com/random-color-palette"})
    return [PaletteGroup(**group_dict) for group_dict in data]

@app.post("/get-palettes/")
def get_palettes(query: PaletteQuery) -> List[Palette]:
    data = []
    response = requests.get(query.url)
    response.raise_for_status()
    
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    elements_with_class = soup.find_all('div', class_="palettecontainerlist")
    for element in elements_with_class:
        palette_name = element.text.strip()
        color_list = []
        for subelem in element.contents:
            if isinstance(subelem, Tag):
                colors = subelem.find_all('div', 'palettecolordiv')
                for color in colors:
                    color_list.append(color['style'].split(':')[1])
        data.append({"palette_name": palette_name, "color_list": color_list})
    
    return [Palette(**group_dict) for group_dict in data]
