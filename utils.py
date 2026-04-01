from calendar import c
import datetime
from pydantic import BaseModel
from urllib.parse import urlencode
from zoneinfo import ZoneInfo
import random
import json
import os
from config import CONFIG_LINK_GOOGLE_FORM, CONFIG_LINK_FILLOUT, AI_PROVIDER_LIST, TASKS
from ai_provider import get_ai_provider


class IdsData(BaseModel):
    id: str
    source: str | None=None
    channel_account_id: str | None=None
    caused_by_event_id: str | None=None
    platform: str
    phone_number: str | None=None
    meeting_time: str | None=None
    name: str | None=None  
    last_name: str | None=None  

class Post(BaseModel):
    # task: str
    current_post: str
    current_stage: str | None=None
    current_stage_description: str | None=None
    conversation_context: str | None=None


class Checking(BaseModel):
    phone_number: str | None=None


def generate_link(id: str, task: str, platform: str, source: str | None=None, channel_account_id: str | None=None, caused_by_event_id: str | None=None,
phone_number: str | None=None, meeting_time: str | None=None, name: str | None=None, last_name: str | None=None)     -> str:
    if platform == "google_form":
        config_data = CONFIG_LINK_GOOGLE_FORM.get(task)
    elif platform == "fillout":
        config_data = CONFIG_LINK_FILLOUT.get(task)
    else:
        return(f'nie znaleziona platrorma {platform}')
    if config_data:
        basic_link = config_data["basic_link"]
        ID = config_data["ID_param"]
        token = config_data["token_param"]
        status = config_data["status_param"]
        random_token = random.randint(100000, 999999)
        params = {
            ID: id,
            token: random_token,
            status: "Do zapisania"
        }
        if platform == "google_form":
            params["ups"] = "pp_url"
        if platform == "fillout":
            date = ""
            hour = ""
            if meeting_time:
                meeting_date_utc = datetime.datetime.strptime(meeting_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                date = meeting_date_utc.strftime("%d.%m.%Y")
                hour = meeting_date_utc.strftime("%H:%M")
            phone_number_link = ""
            if phone_number:
                row_phone_number = []
                for f in phone_number:
                    if f.isdigit():
                        row_phone_number.append(f)
                row_phone_number = "".join(row_phone_number)
                if len(row_phone_number) == 9:
                    row_phone_number = f"48{row_phone_number}"
                if len(row_phone_number) == 11:
                    a = row_phone_number[2:5]
                    b = row_phone_number[5:8]
                    c = row_phone_number[8:11]
                    d = row_phone_number[0:2]
                phone_number_link = f"%2B{d}%20{a}%20{b}%20{c}"
            params["source"] = source
            params["channel_account_id"] = channel_account_id
            params["caused_by_event_id"] = caused_by_event_id
            params["name"] = name
            params["last_name"] = last_name
            params["meeting_date"] = date
            params["meeting_hour"] = hour
        generated_link = f"{basic_link}?{urlencode(params)}&phone_number={phone_number_link}"
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


def prompt_generator(*, task: str, current_post: str, current_stage: str, 
current_stage_description: str, conversation_context: str | None=None, current_date: str | None=None) -> str:
    if task is None or isinstance(task, str) and not task.strip():
        raise ValueError ('Temat jest wymagany')
    values = {
        "current_post": current_post,
        "current_stage": current_stage,
        "current_stage_description": current_stage_description,
        "conversation_context": conversation_context,
        "current_date": current_date
    }
    if task in TASKS:
        required = TASKS[task]["required"]
        for r in required:
            val = values[r]
            if val is None or isinstance(val, str) and not val.strip():
                raise ValueError(f'brak {r} w danych do zadania {task}')
        build = TASKS[task]["build"]
        payload = {}
        for b in build:
            k = values[b]
            if k is None or isinstance(k, str) and not k.strip():
                continue           
            payload[b] = k
        prompt = load_prompt(task)
        json_prompt_str = json.dumps(payload, ensure_ascii=False, indent=2) 
        entire_prompt = (f'{prompt}\n{json_prompt_str}')
        return entire_prompt
    else:
        raise ValueError (f'nie obsługiwane zadanie: {task}')


def def_current_date(*, time_zone: str, date_format=None, hour_format=None) -> dict:
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


async def ai_answer(*, task: str, current_post: str, current_stage: str | None=None, current_stage_description: str | None=None, 
conversation_context: str | None=None, current_date: str | None=None) -> dict:
    current_day = None
    if current_date:
        if isinstance(current_date, dict):
            current_day = current_date.get("current_day")
        elif isinstance(current_date, str):
            current_day = current_date.strip()
        else:
            raise TypeError(f"Nieprawidłowy format {current_date}")
    error = []
    prompt = prompt_generator(task=task, current_post=current_post, current_stage=current_stage, 
    current_stage_description=current_stage_description, conversation_context=conversation_context, current_date=current_day)
    for provider in AI_PROVIDER_LIST:
        try:
            provider_name = provider["name"]
            provider_model = provider["model"]
            current_model = get_ai_provider(provider_name, provider_model)
            if task == "classyfi":
                current_model = get_ai_provider("OpenAI", "gpt-5.4")
            current_day = None
            ai_result = await current_model._call_api(prompt=prompt)
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


async def checking_data(phone_number: str | None=None) -> str:
    if phone_number:
        row_phone_number = []
        for i in phone_number:
            if i.isdigit():
                row_phone_number.append(i)
        row_phone_number = "".join(row_phone_number)        
        if len(row_phone_number) == 9:
            row_phone_number = f'48{row_phone_number}'
        if len(row_phone_number) == 11:
            a = row_phone_number[0:2]
            b = row_phone_number[2:5]
            c = row_phone_number[5:8]
            d = row_phone_number[8:11]
            return {"checking":"OK",
                    "phone": f'+{a} {b} {c} {d}'}
        else:
            return {"checking":"BAD_NUMBER",
                    "phone": row_phone_number}
    return {"checking": "NEED_DATA_TO_CHECK",
            "phone": ""}
                

