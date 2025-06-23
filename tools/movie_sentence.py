from langchain_core.tools import tool

from models.nim import Nim


@tool
def movie_quote(city: str)->str:
    """ Returns a quote from a movie """
    prompt = f"Provide a quote from the movie {city}"
    response = Nim().chat(prompt)
    return response
