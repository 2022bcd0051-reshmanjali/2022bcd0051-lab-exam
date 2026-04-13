from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

model = joblib.load("output/model.pkl")

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict():
    # dummy input (since no JSON provided)
    sample = np.array([[7.4,0.7,0,1.9,0.076,11,34,0.9978,3.51,0.56,9.4]])
    prediction = model.predict(sample)[0]

    return {
        "name": "Reshmanjali Maddula",
        "roll_no": "2022BCD0051",
        "wine_quality": float(prediction)
    }