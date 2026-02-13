from fastapi import FastAPI
import uvicorn
from utils import IdsData, generate_link, Post, ai_answer, current_date

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Cześć nazywam się ToolBox",
    "version": "1.0.0",
    "author": "Szymon Suchodolski"}


@app.post("/client_opinion/link_generator")
def client_opinion_link_generator(request: IdsData):
    task = request.task
    id = request.id
    generated_link = generate_link(id, task)
    return {"link": generated_link}


@app.post("/classyfi")
async def classyfi(request: Post):
    respons = await ai_answer(text=request.post, task=request.task)
    return respons


@app.post("/date_extract")
async def date_extract(request: Post):
    today = current_date()
    respons = await ai_answer(text=request.post, current_date=today, task=request.task)
    return respons


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)