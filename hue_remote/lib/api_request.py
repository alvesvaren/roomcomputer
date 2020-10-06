import requests as req
from .. import config

def gen_url(params: str):
	return "http://" + config.address + "/api/" + config.username + params

async def get(dest: str = "", payload: str = ""):
	try:
		api_resp = req.get(gen_url(dest), data=payload)

		if(not api_resp.ok):  # print out the error if the status code is not 200
			print(api_resp)
			print(api_resp.text)

		return api_resp

	except req.exceptions.RequestException as err:
		print(err)

# PUT Req

async def put(dest: str = "", payload: str = ""):
	try:
		api_resp = req.put(gen_url(dest), data=payload)  # send the payload

		if(not api_resp.ok):
			print(api_resp)
			print(api_resp.text)

		return api_resp

	except req.exceptions.RequestException as err:
		print(err)
