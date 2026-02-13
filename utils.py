from calendar import c
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


def current_date(*, time_zone: str, date_format=None, hour_format=None) -> dict:
    try:
        now = datetime.datetime.now(ZoneInfo(time_zone))
    except:
        raise ValueError (f"Nieprawidłowa strefa czasowa {time_zone}. Wymagana prawidłowa strefa czasowa")
    if date_format:
        cur_day = now.strftime(date_format) 
    else:
        cur_day = None
    if hour_format:
        cur_hour = now.strftime(hour_format)
    else:
        cur_hour = None
    return {"current_day": cur_day, "current_hour": cur_hour}


def clear_date_str(date=None) -> str:      
    bad_result = {"", "0", "null", "nil", "none"}
    if date is None:
        date_str = "0"
    elif isinstance (date, str):
        date_str = date.strip()
    else:
        date_str = str(date).strip()  
    if date_str.lower() in bad_result:
        date_str = "0"
    return date_str


def clear_date_list(dates: list[str]) ->list[str]:
    if not dates:
        return []
    clear_list = []
    for d in dates:
        clear_d = clear_date_str(d)
        if clear_d != "0":
            clear_list.append(clear_d)
    if len(clear_list) == 0:
        return []
    return clear_list


async def ai_answer(text: str, task: str, current_date=None) -> dict:
    error = []
    prompt = load_prompt(task)
    for provider in AI_PROVIDER_LIST:
        try:
            provider_name = provider["name"]
            provider_model = provider["model"]
            current_model = get_ai_provider(provider_name, provider_model)
            current_day = None
            if current_date:
                if isinstance(current_date, dict):
                    current_day = current_date.get("current_day")
                elif isinstance(current_date, str):
                    current_day = current_date.strip()
                else:
                    raise TypeError(f"Nieprawidłowy format {current_date}")
            ai_result = await current_model._call_api(prompt=prompt, text=text, current_date=current_day)
            dates = None
            if ai_result is None:
                error.append(f"Model {provider_model} nie zwrócił odpowiedzi")
                continue
            if not isinstance(ai_result, dict):
                error.append(f"Model {provider_model} nie zwrócił odpowiedzi w formie słownika")
                continue
            result = ai_result.get('result')
            if result is None:
                error.append(f"Model {provider_model} nie zwrócił rezultatu")
                continue   
            if not isinstance(result, dict):
                error.append(f"Model {provider_model} nie zwrócił rezultatu w formie słownika")
                continue
            dates = result.get('dates')
            if dates is None:
                date_list = []
            elif isinstance(dates, str):
                date = clear_date_str(dates)
                if date == "0":
                    date_list = []
                else:
                    date_list = [date]
            elif isinstance(dates, list):  
                date_list = clear_date_list(dates)
            else:
                date_list = []
            result["dates"] = date_list
            return result
        except Exception as e:
            error.append(f"Error calling API for {provider_name} {provider_model}: {e}")
    raise RuntimeError(f"Wszystkie modele zwróciły błąd: {error}")
