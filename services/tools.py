from langchain_core.tools import tool
from datastore.qdrant_datastore import QdrantDatastore
from services.openai_utils import OpenAI
import requests, os

from dotenv import load_dotenv

load_dotenv()

oai = OpenAI()
qd = QdrantDatastore(embedder=oai.get_embedding)

@tool
def get_rag_response(user_query: str):
    """
    This tool will be used by to retrieve specific information from the uploaded documents.
    """
    text = ""
    response = qd.search(user_query)
    for hit in response:
        text += hit.payload['text'] + '\n\n\n'
    return text


@tool
def get_weather(city_name: str):
    """
    This tool will be used if the user asks for weather.
    """
    response = requests.post('http://api.openweathermap.org/geo/1.0/direct', data={'q':city_name, 'appid':os.environ.get('OPEN_WEATHER_MAP_API_KEY'),'limit':1}).json()
    if response.status_code != 200 or not response:
        return f'It looks like I cannot check the weather in {city_name}. Please try again.'
    lat = response[0]['lat']
    lon = response[0]['lon']

    response = requests.post('https://api.openweathermap.org/data/2.5/weather', {'lat': lat, 'lon': lon, 'appid':os.environ.get('OPEN_WEATHER_MAP_API_KEY'), 'units': 'metric'}).json()
    if response.status_code != 200 or not response:
        return f'It looks like I cannot check the weather in {city_name}. Please try again.'
    
    weather = f'Weather in {city_name}:{response}'

    return weather