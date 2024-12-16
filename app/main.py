from fastapi import FastAPI, HTTPException, Depends, status, Request, Form, File, UploadFile
from typing import Optional, Annotated
from pydantic import BaseModel
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
import cv2
import os
import joblib
import pickle
import sklearn

import models
from database import engine, SessionLocal
from models import ImageDB
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")
#app.mount("/Images", StaticFiles(directory=os.path.abspath("../Images")), name="Images")
app.mount("/Images", StaticFiles(directory="../Images"), name="Images")


class ImageDBBase(BaseModel):
    file_name: str
    prediction: str
    upload_time: datetime | None = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependencies = Annotated[Session,Depends(get_db)]

model = joblib.load("../Model/smile_svc.pkl")

def convert_type(file_location: str) -> str:
    image = cv2.imread(file_location)
    new_location = file_location.rsplit('.', 1)[0] + '.jpg' # define maxSplit as 1
    cv2.imwrite(new_location, image)
    os.remove(file_location)
    return new_location

def preprocess_image(file_loc):
    image = np.array(cv2.imread(file_loc,1))
    if image is None:
        raise FileNotFoundError(f"Unable to read the image at {file_loc}")
    image = cv2.resize(image, (64,64)).flatten()
    #print(image)
    return image

def prediction_from_data(image):
    prediction = model.predict([image])
    print(f"Prediction output: {prediction}, Type: {type(prediction)}")

    return "Smiling" if prediction == 1 else "Not Smiling"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(name="home.html", request=request)

@app.get("/classify", response_class=HTMLResponse)
def classify(request: Request):
    return templates.TemplateResponse(name="classify.html", request=request)

@app.post("/classify", response_class=HTMLResponse)
async def upload_image(request: Request, db: db_dependencies, image: UploadFile = File(...)):
    # Access file details
    try:
        file_name = image.filename
        content_type = image.content_type
        file_loc = f"../Images/{file_name}"
        with open(file_loc, "wb") as f:
            f.write(image.file.read())
        #print(file_name)
        # Convert image to JPG format if necessary
        if file_name.lower().endswith(('.png', '.jpeg')):
            file_loc = convert_type(file_loc)

        # Preprocess the image
        image_data = preprocess_image(file_loc)
        prediction = prediction_from_data(image_data)
        print(prediction)
        current_prediction = ImageDB(
            file_name = file_loc,
            prediction = prediction,
            upload_time = datetime.utcnow()
        )

        db.add(current_prediction)
        db.commit()

        print(f"File: {file_loc} and Prediction: {prediction}")
        return templates.TemplateResponse("classify.html",{
            "request": request,
            "file_name": file_loc,
            "prediction": prediction
        })
        #return {"file_name": file_name, "content_type": content_type}

    except Exception as e:
        print(f"Error in upload_image: {e}")
        return HTMLResponse("An error occurred during image upload. Try Again.", status_code = 500)

@app.get("/history", response_class=HTMLResponse)
def history(request: Request, db: db_dependencies):
    try:
        dbhistory = db.query(ImageDB).order_by(ImageDB.upload_time.desc()).all()

        return templates.TemplateResponse("history.html", {
            "request": request,
            "history": dbhistory
        })
    except Exception as e:
        print(f"Error in history endpoint: {e}")
        return HTMLResponse("An error occurred while fetching the history.", status_code = 500)
