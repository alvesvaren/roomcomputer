import requests as req # Used for HTTP requests for the Hue API
import json # API uses JSON
import asyncio # ASync stuff
import time

from .lib.func import * # useful functions

from . import config # Configuration for the controller (/config.py <- change this file)
from .presets import * # presets for the lights
from .lib import api_request

LIGHTS = {} # dictionary of all the lights

loop = asyncio.get_event_loop() # ASync loop

	# Internal get functions
async def get_lights():
	return await api_request.get("/lights")

async def get_light(index: int=1):
	return await api_request.get( f"/lights/{index}" )

# Lower level light manipulation (async)
async def toggle_light(index: int = 1, isOn: bool = True):
	await api_request.put( f"/lights/{index}/state", json.dumps({"on": isOn}))

async def toggle_lights(isOn: bool=True):
	for key in LIGHTS:
		await toggle_light(key, isOn)

async def set_light_RGB( index: int, r: int, g: int, b: int ):
	h, s, v = rgb_to_hsv(r, g, b)
	payload = {"sat": s, "bri": v, "hue": h}

	await api_request.put( f"/lights/{index}/state", payload )

# Normal functions
def switch_light( index: int=1 ):
	key = LIGHTS.get(str(index))
	if(key):
		if( key.get("state") ):
			curPower = LIGHTS[str(index)]["state"]["on"]
			loop.run_until_complete( toggle_light(index, not curPower))
	else:
		print(f"Error: Light index '{index}' out of range")

def switch_lights():
	for key in LIGHTS:
		switch_light(key)

# Light control
def set_light_color( index: int, r: int, g: int, b: int ):
	if( LIGHTS.get(str(index)) ):
		loop.run_until_complete( set_light_RGB(index, r, g, b) )
	else:
		print(f"Error: Light index '{index}' out of range")

def set_light_brightness( index: int, b: int ):
	if( LIGHTS.get(str(index)) ):
		payload = {"bri": b}
		loop.run_until_complete( api_request.put( f"/lights/{index}/state", payload ) )
	else:
		print(f"Error: Light index '{index}' out of range")

def set_brightness( b: int ):
	for key in LIGHTS:
		set_light_brightness( key, b )

def set_all_lights_color( r: int, g: int, b: int ):
	for key in LIGHTS:
		set_light_color( key, r, g, b )

def power(isOn: bool = True): # Controlling the power of the lights
	loop.run_until_complete( toggle_lights(isOn) )

def power_light( index: int, isOn:bool = True ):
	loop.run_until_complete( toggle_light( index, isOn ) )

# Presets
def setLightPreset( index:int, p:str ):
	if( LIGHTS.get(str(index)) ):
		if( PRESETS.get(p) ):
			preset = PRESETS[p]
			r, g, b = preset["color"]
			brightness = preset["brightness"]

			set_light_color( index, r, g, b )
			set_light_brightness( index, brightness )
		else:
			print("Error: Unknown preset '" + p + "'")
	else:
		print(f"Error: Light index '{index}' out of range")

def set_preset( presetID: str, index: int = -1 ):
	if( PRESETS.get(presetID) ):
		if( index == -1 ):
			for key in LIGHTS:
				setLightPreset( key, presetID )
		else:
			setLightPreset( index, presetID )
	else:
		print(f"Error: Unknown preset '{presetID}'")

def count_lights():
	return len(LIGHTS)

# Controller "system" functions
def delay(n:int):
	time.sleep(n)

def init():
	jsonLights = loop.run_until_complete(api_request.get("/lights"))
	LIGHTS = json.loads(jsonLights.text)

def end():
	loop.close()
