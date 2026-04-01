from fastapi import FastAPI
import uvicorn
from utils import IdsData, generate_link, Post, ai_answer, def_current_date, Checking, checking_data

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Cześć nazywam się ToolBox",
    "version": "1.0.0",
    "author": "Szymon Suchodolski"}


@app.post("/client_opinion/link_generator")
def client_opinion_link_generator(request: IdsData):
    generated_link = generate_link(task="book_appointments", id=request.id, platform=request.platform, source=request.source, 
    channel_account_id=request.channel_account_id, caused_by_event_id=request.caused_by_event_id, phone_number=request.phone_number, 
    meeting_time=request.meeting_time, name=request.name, last_name=request.last_name)
    return {"link": generated_link}


@app.post("/classyfi")
async def classyfi(request: Post):
    respons = await ai_answer(task="classyfi", current_post=request.current_post, current_stage=request.current_stage, 
    current_stage_description=request.current_stage_description, conversation_context=request.conversation_context)
    return respons


@app.post("/date_extract")
async def date_extract(request: Post):
    today = def_current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y")
    respons = await ai_answer(task="date_extract", current_post=request.current_post,  current_date=today, conversation_context=request.conversation_context)
    return respons


@app.post("/phone_extract")
async def phone_extract(request: Post):
    respons = await ai_answer(task="phone_extract", current_post=request.current_post, conversation_context=request.conversation_context)
    return respons


@app.post("/date_hour_extract")
async def date_hour_extract(request: Post):
    today = def_current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y", hour_format="%H:%M")
    respons = await ai_answer(task="date_hour_extract", current_post=request.current_post, current_date=today, conversation_context=request.conversation_context)
    return respons


@app.post("/today")
async def today():
    now = def_current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y", hour_format="%H:%M:%")
    return now


@app.post("/check")
async def check(request: Checking):
    result = await checking_data(phone_number=request.phone_number)
    return result





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)