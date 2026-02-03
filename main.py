from fastapi import FastAPI
import uvicorn
from utils import IdsData, generate_link   

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)