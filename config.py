CONFIG_LINK = {
    "analiza_dokumentu": {
        "basic_link": "https://docs.google.com/forms/d/e/1FAIpQLSdwHyGVEjQGya9OXc7-BstTQ3WJoMJx9iFlkpuZmJpVGPIptA/viewform",
        "ID_entry": "entry.1721827309",
        "token_entry": "entry.1814604231",
        "status_entry": "entry.838922726"
        }
    }


AI_PROVIDER_LIST = [
    {"name": "OpenAI", "model": "gpt-4o"},
    {"name": "Google Generative AI", "model": "gemini-2.5-flash"},
    {"name": "Anthropic", "model": "claude-3-5-sonnet-20240620"}
]


TASKS = {
    "classyfi" : {"required": ["prompt","text"],
            "build": ["prompt","text"]},
    "date_extract": {"required": ["prompt","text", "Current_date"],
            "build": ["prompt","text", "Current_date"],
    }}