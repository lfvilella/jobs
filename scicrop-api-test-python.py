import datetime
import requests
import typing

import pydantic


class Degree(pydantic.BaseModel):
    institution_name: str
    degree_name: str
    begin_date: datetime.date
    end_date: datetime.date


class Resume(pydantic.BaseModel):
    full_name: str
    email: pydantic.EmailStr
    mobile_phone: str
    age: pydantic.PositiveInt
    home_address: str
    start_date: datetime.date
    opportunity_tag: str
    past_jobs_experience: str
    degrees: typing.List[Degree]
    programming_skills: typing.List[str]
    database_skills: typing.List[str]
    hobbies: typing.List[str]
    why: str
    git_url_repositories: pydantic.HttpUrl


def _date_to_unix_epoch(date: datetime.date) -> int:
    return int(
        datetime.datetime.combine(
            date, datetime.datetime.min.time()
        ).timestamp()
    )


def post_resume(resume: typing.Union[Resume, dict]):
    """ Post Resume
    Send resume to scicrop.
    """
    if not isinstance(resume, Resume):
        resume = Resume(**resume)

    data = resume.dict()
    data["start_date"] = _date_to_unix_epoch(data["start_date"])
    for degree in data["degrees"]:
        degree["begin_date"] = _date_to_unix_epoch(degree["begin_date"])
        degree["end_date"] = _date_to_unix_epoch(degree["end_date"])

    url = (
        "https://engine.scicrop.com/scicrop-engine-web/api/v1/jobs/post_resume"
    )
    response = requests.post(url, json=data)
    if not response.ok:
        raise Exception(response.reason)

    return response


def _get_my_resume():
    return {
        "full_name": "Luis Felipe Fabro Vilella",
        "email": "vilella.luisfelipe@gmail.com",
        "mobile_phone": "+55 (14) 99679-7600",
        "age": 19,
        "home_address": "Av. Maximiano de Andrade, Fartura-SP",
        "start_date": "2020-07-08",
        "opportunity_tag": "python_developer",
        "past_jobs_experience": (
            "Worked as a freelancer developing web systems for small "
            "and median business, such as an accounting company and "
            "a gym, also developed various experimental projects to test web "
            "frameworks such as Django, Flask, FastAPI in the backend, "
            "and used HTML, CSS, JQuery and VueJS in the frontend."
        ),
        "degrees": [
            {
                "institution_name": "UENP-CLM",
                "degree_name": "Science of Computation",
                "begin_date": "2019-03-15",
                "end_date": "2022-01-05",
            }
        ],
        "programming_skills": [
            "python",
            "django",
            "flask",
            "fastapi",
            "html",
            "javascript",
            "css",
            "docker",
        ],
        "database_skills": ["mysql", "postgresql", "sqlalchemy"],
        "hobbies": ["fitness", "series", "learn_techs"],
        "why": (
            "I started on web development and I just start on IT bussines "
            "so I looking for learn a lot and contribute."
        ),
        "git_url_repositories": "https://github.com/lfvilella",
    }


if __name__ == "__main__":
    post = post_resume(_get_my_resume())
    assert post.status_code == 200
    print('Resume Posted')
