import requests as req
from .. import config
from typing import Union, Callable

def gen_url(params: str):
	return "http://" + config.address + "/api/" + config.username + params

async def _fetch(method: Callable, dest: str = "", payload: Union[str, dict] = ""):
	try:
		api_resp = method(gen_url(dest), data=payload)

		if(not api_resp.ok):  # print out the error if the status code is not 200
			print(api_resp)
			print(api_resp.text)

		return api_resp

	except req.exceptions.RequestException as err:
		print(err)

async def get(dest: str = "", payload: Union[str, dict] = ""):
	return _fetch(req.get, dest, payload)

async def put(dest: str = "", payload: Union[str, dict] = ""):
	return _fetch(req.put, dest, payload)
