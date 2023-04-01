import jinja2 as jinja2
import pydantic as pydantic
import uvicorn as uvicorn
from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from pydantic.main import BaseModel
from starlette.requests import Request

from scripts import get_links, prepare, search

app = FastAPI()
env = jinja2.Environment()
env.globals.update(zip=zip)

templates = Jinja2Templates(directory="templates")


@app.get('/')
async def index_view(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/search')
async def search_view(request: Request):
    line = request.query_params.get('line')
    pages = search(line)
    links_titles = pages

    return templates.TemplateResponse("index.html", {"request": request, "line": line, 'links_titles': links_titles})


if __name__ == '__main__':
    uvicorn.run("server:app", host='0.0.0.0', port=88, reload=False,
                )
