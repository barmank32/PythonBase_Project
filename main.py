import os
import time
from typing import List
import logging
from timezonefinder import TimezoneFinder, TimezoneFinderL
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    # id: int
    latitude: float = Field(..., description='Широта')
    longitude: float = Field(..., description='Долгата')


class ArrayItem(Item):
    id: int = Field(..., ge=0, description='Уникальный идентификатор')


class RespItem(Item):
    timezone: str = Field(..., description='Временная зона')


class RespArrayItem(ArrayItem):
    timezone: str = Field(..., description='Временная зона')


JSONRespArray = List[RespArrayItem]
JSONArray = List[ArrayItem]
JSONStructure = JSONArray

DEBUG = os.environ.get('DEBUG', False)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
)


def timing_val(func):
    def wrapper(*args, **kwarg):
        if DEBUG:
            ts = time.time()
        result = func(*args, **kwarg)
        if DEBUG:
            te = time.time()
            logging.debug(f'Func: {func.__name__} timer: {te - ts} sec')
        return result

    return wrapper


@timing_val
def tfinderl(latitude, longitude):
    returns = None
    try:
        tf = TimezoneFinderL(in_memory=True)
        TimezoneFinderL.using_numba()
        # latitude, longitude = 45.4333, 40.5667
        returns = tf.timezone_at(lng=longitude, lat=latitude)
    except BaseException as ex:
        logging.exception(ex)
    logging.info(returns)
    return returns


@timing_val
def tfinder(latitude, longitude):
    returns = None
    try:
        tf = TimezoneFinder(in_memory=True)
        TimezoneFinder.using_numba()
        # latitude, longitude = 45.4333, 40.5667
        returns = tf.timezone_at(lng=longitude, lat=latitude)
    except BaseException as ex:
        logging.exception(ex)
    logging.info(returns)
    return returns


@app.get("/")
def read_root():
    """Root"""
    return {"message": "Welcome"}


def depend_params(latitude: float, longitude: float):
    return {"latitude": latitude, "longitude": longitude}


@app.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.get("/timezone", response_model=RespItem)
def timezone(params: dict = Depends(depend_params)):
    """Определение зоны по координатам GPS."""
    response_json = None
    try:
        response_json = {
            "latitude": params['latitude'],
            "longitude": params['longitude'],
            "timezone": tfinder(latitude=params['latitude'], longitude=params['longitude'])
        }
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return response_json


@app.get("/timezonel", response_model=RespItem)
def timezonel(params: dict = Depends(depend_params)):
    """Определение зоны по координатам GPS. Предрассчитанная."""
    response_json = None
    try:
        response_json = {
            "latitude": params['latitude'],
            "longitude": params['longitude'],
            "timezone": tfinderl(latitude=params['latitude'], longitude=params['longitude'])
        }
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return response_json


@app.post("/timezone", response_model=JSONRespArray)
def timezone_array(message: JSONStructure):
    """Определение зоны по координатам GPS.\n
    Функция позволяет отправить массив координат\n
    Пример: [{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    response_json: List = []
    for item in message:
        item = dict(item)
        response_json.append({
            "id": item["id"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone": tfinder(latitude=float(item["latitude"]), longitude=float(item["longitude"])),
        })
    return response_json


@app.post("/timezonel", response_model=JSONRespArray)
def timezonel_array(message: JSONStructure):
    """Определение зоны по координатам GPS. Предрассчитанная.\n
    Функция позволяет отправить массив координат\n
    Пример: [{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    response_json: List = []
    for item in message:
        item = dict(item)
        response_json.append({
            "id": item["id"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone": tfinderl(latitude=item["latitude"], longitude=item["longitude"]),
        })
    return response_json
