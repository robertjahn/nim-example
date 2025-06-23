import re

from models.nim import Nim
from langchain_core.tools import tool

regex = re.compile('[^a-zA-Z]')

@tool
def valid_city(city: str)->bool:
    """ Returns if the input is a valid city"""
    prompt = f"Is {city} a city? respond only with yes or no."
    response = Nim().chat(prompt)
    response = regex.sub('', response).lower()
    print(f"Tool answer: -->{response}<--")
    return response == "yes"
