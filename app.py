from fastapi import FastAPI, Depends, Request, Form, status, UploadFile, File
from fastapi.staticfiles import StaticFiles

from starlette.responses import RedirectResponse, Response
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

import io
from PIL import Image
from fastapi.responses import StreamingResponse

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/items/{item_id}")
async def get_item(req: Request, item_id: str):
    return templates.TemplateResponse("item.html", {"request": req, "id": item_id})


@app.get("/")
async def home(req: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("base.html", {"request": req, "todo_list": todos})


@app.post("/add")
def add(req: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update/{todo_id}")
def add(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    todo.complete = not todo.complete
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{todo_id}")
def add(req: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()
    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/image",
         responses={
             200: {
                 "content": {"image/jpg": {}}
             }
         },
         response_class=Response)
def image():
    pil_image = Image.open("C:/Users/Ted/Desktop/images.jpg")
    imgio = io.BytesIO()
    pil_image.save(imgio, 'JPEG')
    imgio.seek(0)
    return StreamingResponse(content=imgio, media_type="image/jpg")


@app.post("/uploadfiles/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}
