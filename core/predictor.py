# core/predictor.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import numpy as np

_model = None  # cache

def train_model(tasks):
    texts = []
    durations = []

    for task in tasks:
        if not task.start_time or not task.end_time:
            continue
        duration = (task.end_time - task.start_time).total_seconds() / 60
        if duration < 1:
            continue

        text = f"{task.title} {task.description}"
        texts.append(text)
        durations.append(duration)

    if len(texts) < 5:
        return None  # túl kevés adat

    model = make_pipeline(
        TfidfVectorizer(),
        LinearRegression()
    )

    model.fit(texts, durations)
    return model

def predict_duration(title, description, tasks):
    global _model
    if _model is None:
        _model = train_model(tasks)
    
    if not _model:
        return None  # nincs elég adat

    text = f"{title} {description}"
    prediction = _model.predict([text])[0]
    return round(prediction, 1)
