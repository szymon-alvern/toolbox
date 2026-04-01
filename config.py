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
        "phone_number_param": "phone_number",
        "meeting_date_param": "meeting_date",
        "meeting_hour_param": "meeting_hour",
        "source_param": "source",
        "channel_account_id_param": "channel_account_id",
        "caused_by_event_id_param": "caused_by_event_id",
        "status_param": "status",
        "name_param": "name",
        "last_name_param": "last_name"
        }
    }




AI_PROVIDER_LIST = [
    {"name": "OpenAI", "model": "gpt-4o"},
    {"name": "Google Generative AI", "model": "gemini-2.5-flash"},
    {"name": "Anthropic", "model": "claude-3-5-sonnet-20240620"}
]


TASKS = {
    "classyfi" : {"required": ["current_post", "current_stage", "current_stage_description"],
            "build": ["current_post", "conversation_context", "current_stage", "current_stage_description"]},
    "date_extract": {"required": ["current_post", "current_date"],
            "build": ["current_post", "current_date", "conversation_context"]},
    "date_hour_extract": {"required": ["current_post", "current_date"],
            "build": ["current_post", "current_date", "conversation_context"]},
    "phone_extract": {"required": ["current_post"],
            "build": ["current_post", "conversation_context"]}
    }
