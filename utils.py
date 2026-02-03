from pydantic import BaseModel
from config import CONFIG_LINK
import random
from urllib.parse import urlencode

class IdsData(BaseModel):
    task: str
    id: str

def generate_link(id: str, task: str) -> str:
    config_data = CONFIG_LINK.get(task)
    if config_data:
        basic_link = config_data["basic_link"]
        ID_entry = config_data["ID_entry"]
        token_entry = config_data["token_entry"]
        random_token = random.randint(100000, 999999)
        params = {
            "usp": "pp_url",
            ID_entry: id,
            token_entry: random_token
        }
        generated_link = f"{basic_link}?{urlencode(params)}"
        return generated_link
    else:
        return f"Brak generowania linków dla zadania {task}"
