from langchain_core.tools import tool

from models.nim import Nim

@tool
def travel_advice(city: str)->str:
    """ Provide travel advice for the given city"""
    prompt = f"Give travel advise in a paragraph of max 50 words about {city}"
    response = Nim().chat(prompt)
    print(f"Tool answer: -->{response}<--")
    return response
