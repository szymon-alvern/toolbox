from fastapi import FastAPI
import uvicorn
from utils import IdsData, generate_link, Post, ai_answer, def_current_date

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Cześć nazywam się ToolBox",
    "version": "1.0.0",
    "author": "Szymon Suchodolski"}


@app.post("/client_opinion/link_generator")
def client_opinion_link_generator(request: IdsData):
    generated_link = generate_link(task=request.task, id=request.id, platform=request.platform, source=request.source, 
    channel_account_id=request.channel_account_id, caused_by_event_id=request.caused_by_event_id)
    return {"link": generated_link}


@app.post("/classyfi")
async def classyfi(request: Post):
    respons = await ai_answer(task="classyfi", current_post=request.current_post, last_topic=request.last_topic, last_stage=request.last_stage, 
conversation_context=request.conversation_context)
    return respons


@app.post("/date_extract")
async def date_extract(request: Post):
    today = def_current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y")
    respons = await ai_answer(task="date_extract", current_post=request.current_post, current_date=today, conversation_context=request.conversation_context)
    return respons


@app.post("/date_hour_extract")
async def date_hour_extract(request: Post):
    today = def_current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y", hour_format="%H:%M")
    respons = await ai_answer(task="date_hour_extract", current_post=request.current_post, current_date=today, conversation_context=request.conversation_context)
    return respons


@app.post("/today")
async def today():
    now = current_date(time_zone="Europe/Warsaw", date_format="%d-%m-%Y", hour_format="%H:%M:%")
    return now




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)