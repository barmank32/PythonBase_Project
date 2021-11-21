import os
import time
from typing import Any, List
import logging
from timezonefinder import TimezoneFinder, TimezoneFinderL
from fastapi import FastAPI

app = FastAPI()
JSONArray = List[Any]
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
    tf = TimezoneFinderL(in_memory=True)
    TimezoneFinderL.using_numba()
    # latitude, longitude = 45.4333, 40.5667
    returns = tf.timezone_at(lng=longitude, lat=latitude)
    logging.info(returns)
    return returns


@timing_val
def tfinder(latitude, longitude):
    tf = TimezoneFinder(in_memory=True)
    TimezoneFinder.using_numba()
    # latitude, longitude = 45.4333, 40.5667
    returns = tf.timezone_at(lng=longitude, lat=latitude)
    logging.info(returns)
    return returns


@app.get("/")
def read_root():
    return {"message": "Welcome"}


@app.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.get("/timezone")
def timezone(latitude, longitude):
    response_json = None
    try:
        response_json = {"latitude": latitude, "longitude": longitude,
                         "timezone": tfinder(latitude=float(latitude), longitude=float(longitude))}
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return response_json


@app.get("/timezonel")
def timezonel(latitude, longitude):
    response_json = None
    try:
        response_json = {"latitude": latitude, "longitude": longitude,
                         "timezone": tfinderl(latitude=float(latitude), longitude=float(longitude))}
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return response_json


@app.post("/timezone")
def timezone_array(message: JSONStructure):
    """[{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    try:
        for item in message:
            item["timezone"] = tfinder(latitude=float(item["latitude"]), longitude=float(item["longitude"]))
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return message


@app.post("/timezonel")
def timezonel_array(message: JSONStructure):
    """[{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    try:
        for item in message:
            item["timezone"] = tfinderl(latitude=float(item["latitude"]), longitude=float(item["longitude"]))
    except BaseException as ex:
        logging.exception(ex)
    finally:
        return message
