from ai import EligibilityPrediction
from fastapi import FastAPI
from pydantic import BaseModel
import config


app = FastAPI()
# initialize the ai model
ai = EligibilityPrediction(config.PREPROCESSED_DATASET_FILE)


class Input(BaseModel):
    age: int | None = None
    health_conditions: list[str] = []
    professions: list[str] = []
    genre: str | None = None


class Entry(BaseModel):
    # age: Ellipsis = ...
    health_conditions: list[str]
    professions: list[str]
    genres: list[str]


class Output(BaseModel):
    score: float


@app.get("/entries")
def get_entries() -> Entry:
    entries = Entry(
        health_conditions=ai.get_health_conditions(),
        professions=ai.get_professions(),
        genres=ai.get_genres(),
    )

    return entries


@app.post("/input")
def post_input(_input: Input) -> Output:
    score = ai.predict(
        health_conditions=_input.health_conditions,
        professions=_input.professions,
        age=_input.age,
        genre=_input.genre,
    )

    return Output(score=score)
