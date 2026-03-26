CONFIG_LINK_GOOGLE_FORM = {
    "analiza_dokumentu": {
        "basic_link": "https://docs.google.com/forms/d/e/1FAIpQLSdwHyGVEjQGya9OXc7-BstTQ3WJoMJx9iFlkpuZmJpVGPIptA/viewform",
        "ID_param": "entry.1721827309",
        "token_param": "entry.1814604231",
        "status_param": "entry.838922726"
        },
    "book_appointments": {
        "basic_link": "https://docs.google.com/forms/d/e/1FAIpQLSfz3gpJqff-s0gwRAYcdaUiaE2WZTjbQoiZ7RPI5hNWqBed5w/viewform",
        "ID_param": "entry.322681086",
        "token_param": "entry.82943063",
        "status_param": "entry.836695870"
        }
    }


CONFIG_LINK_FILLOUT = {

    "book_appointments": {
        "basic_link": "https://forms.fillout.com/t/w39gRpc5Dzus",
        "ID_param": "case_id",
        "token_param": "token",
        # "source_param": "source",
        # "channel_account_id_param": "channel_account_id",
        "status_param": "status"
        }
    }




AI_PROVIDER_LIST = [
    {"name": "OpenAI", "model": "gpt-4o"},
    {"name": "Google Generative AI", "model": "gemini-2.5-flash"},
    {"name": "Anthropic", "model": "claude-3-5-sonnet-20240620"}
]


TASKS = {
    "classyfi" : {"required": ["current_post", "last_topic", "last_stage"],
            "build": ["current_post", "conversation_context", "last_topic", "last_stage"]},
    "date_extract": {"required": ["current_post", "current_date"],
            "build": ["current_post", "current_date", "conversation_context"]},
    "date_hour_extract": {"required": ["current_post", "current_date"],
            "build": ["current_post", "current_date", "conversation_context"]}
    }