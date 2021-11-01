import time
from typing import Union, Any, List

from timezonefinder import TimezoneFinder, TimezoneFinderL
from fastapi import FastAPI

app = FastAPI()
JSONArray = List[Any]
JSONStructure = Union[JSONArray]


def timing_val(func):
    def wrapper(*args, **kwarg):
        ts = time.time()
        result = func(*args, **kwarg)
        te = time.time()
        print(f'Func: {func.__name__} timer: {te - ts} sec')
        return result
    return wrapper


@timing_val
def tfinderl(latitude=None, longitude=None):
    tf = TimezoneFinderL(in_memory=True)
    TimezoneFinderL.using_numba()
    # latitude, longitude = 45.4333, 40.5667
    returns = tf.timezone_at(lng=longitude, lat=latitude)  # returns 'Europe/Berlin'\
    print(returns)
    return returns


@timing_val
def tfinder(latitude=None, longitude=None):
    tf = TimezoneFinder(in_memory=True)
    TimezoneFinder.using_numba()
    # latitude, longitude = 45.4333, 40.5667
    returns = tf.timezone_at(lng=longitude, lat=latitude)  # returns 'Europe/Berlin'\
    print(returns)
    return returns


@app.get("/")
async def read_root():
    return {"message": "Welcome"}


@app.get("/status")
async def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@app.get("/timezone")
async def timezone(latitude, longitude):
    response_json = None
    try:
        response_json = {"latitude": latitude, "longitude": longitude,
                         "timezone": tfinder(latitude=float(latitude), longitude=float(longitude))}
    except BaseException as ex:
        print(ex)
    finally:
        return response_json


@app.get("/timezonel")
async def timezonel(latitude, longitude):
    response_json = None
    try:
        response_json = {"latitude": latitude, "longitude": longitude,
                         "timezone": tfinderl(latitude=float(latitude), longitude=float(longitude))}
    except BaseException as ex:
        print(ex)
    finally:
        return response_json


@app.post("/timezone")
async def timezone_array(message: JSONStructure = None):
    """[{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    try:
        for item in message:
            item["timezone"] = tfinder(latitude=float(item["latitude"]), longitude=float(item["longitude"]))
    except BaseException as ex:
        print(ex)
    finally:
        return message


@app.post("/timezonel")
async def timezonel_array(message: JSONStructure = None):
    """[{"id" : "0","latitude":"59.93","longitude":"30.332"}]"""
    try:
        for item in message:
            item["timezone"] = tfinderl(latitude=float(item["latitude"]), longitude=float(item["longitude"]))
    except BaseException as ex:
        print(ex)
    finally:
        return message
