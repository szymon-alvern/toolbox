import datetime
from pydantic import BaseModel
from urllib.parse import urlencode
from zoneinfo import ZoneInfo
import random
import os
from config import CONFIG_LINK, AI_PROVIDER_LIST, TASKS
from ai_provider import get_ai_provider




class IdsData(BaseModel):
    task: str
    id: str


class Post(BaseModel):
    task: str
    post: str

def generate_link(id: str, task: str) -> str:
    config_data = CONFIG_LINK.get(task)
    if config_data:
        basic_link = config_data["basic_link"]
        ID_entry = config_data["ID_entry"]
        token_entry = config_data["token_entry"]
        status_entry = config_data["status_entry"]
        random_token = random.randint(100000, 999999)
        params = {
            "usp": "pp_url",
            ID_entry: id,
            token_entry: random_token,
            status_entry: "Do zapisania"
        }
        generated_link = f"{basic_link}?{urlencode(params)}"
        return generated_link
    else:
        return f"Brak generowania linków dla zadania {task}"


def load_prompt(task: str) -> str:
    if task in TASKS:
        prompt_name = f"{task}.txt"
        if not os.path.exists(f'prompts/{prompt_name}'):
            raise ValueError (f"plik {prompt_name} nie istnieje")
        with open(f'prompts/{prompt_name}', "r", encoding="utf-8") as file:
            return file.read()
    else:
        raise ValueError (f'nie obsługiwane zadanie: {task}')


def current_date():
    date = datetime.datetime.now(ZoneInfo("Europe/Warsaw"))
    today = date.strftime("%d-%m-%Y") 
    return today


async def ai_answer(text: str, task: str, current_date=None) -> dict:
    error = []
    prompt = load_prompt(task)
    for provider in AI_PROVIDER_LIST:
        try:
            provider_name = provider["name"]
            provider_model = provider["model"]
            current_model = get_ai_provider(provider_name, provider_model)
            result = await current_model._call_api(prompt=prompt, text=text, current_date=current_date)
            date = result.get('date')
            bad_result = {"", "0", "null"}
            if date is None:
                date_str = "0"
            elif isinstance (date, str):
                date_str = date.strip()
            else:
                date_str = str(date).strip()  
            if date_str.lower() in bad_result:
                error.append(f'{current_model} nie odczytał daty')
                continue
            result["date"] = date_str
            return result
        except Exception as e:
            error.append(f"Error calling API for {provider_name} {provider_model}: {e}")
    raise RuntimeError(f"Wszystkie modele zwróciły błąd: {error}")
