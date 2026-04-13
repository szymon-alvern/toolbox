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
            "build": ["current_post", "conversation_context"]},
    "time_extract": {"required": ["current_post", "current_date"],
            "build": ["current_post", "current_date"]},
    "data_from_call": {"required": ["current_post"],
            "build": ["current_post"]}      
    }


RESPONSE_BUILDERS = {
    "phone_call":{
        "fields":["case_id", "meeting_time", "phone", "name", "last_name", "email", "event_type", "event_date", "start_event_time",
                  "guest_count", "customer_notes", "owner_notes", "needs_follow_up"],
        "messages":
            {"case_id":"- Numer sprawy: {value}",
            "name": "- Zapisano imię klienta: {value}",
            "last_name": "- Zapisano nazwisko klienta: {value}",
            "phone": "- Zapisano numer telefonu klienta: {value}",
            "email": "- Zapisano email do klienta: {value}",
            "meeting_time": {
                True: "- Zapisano datę spotkania z klientem w kalendarzu.\n - Data i godzina spotkania {value}",
                False: "- UWAGA!!! Podana data {value} jest zajęta, sprawdź jeszcze raz i ewentualnie poinformuj klienta o zmianie"},
            "event_date": "- Planowana data imprezy {value}",
            "event_type": "- Typ imprezy {value}",
            "start_event_time": "- Planowana godzina rozpoczecia imprezy {value}",
            "guest_count": "- Orientacyjna liczba gości {value}",
            "customer_notes": "- Informacja od klienta: {value}", 
            "owner_notes": "- Moja notatka: {value}", 
            "needs_follow_up": {True: "- Konieczna informacja zwrotna do klienta",
                                False: "- Klient ma wszystkie informacje"}
            }   
    }
}

