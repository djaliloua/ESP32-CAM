import urequests
import json
import asyncio
import os
from .model import MQTTConfig
import machine





def get_data_from_api(url):
    try:
        print("Sending request to:", url)
        response = urequests.get(url)  # Make a GET request
        if response.status_code == 200:  # Check if the request was successful
            #print("Response data:", response.text)
            return response.text
        else:
            pass
            #print(f"Failed to get data. Status code: {response.status_code}")
    except Exception as e:
        print("Error occurred:", e)
    finally:
        if 'response' in locals():  # Ensure response object is properly closed
            response.close()
    return ""

def _fetch_():
    api_url = "http://192.168.1.131:5000/MQTTConfig/1"  # Replace with your API URL
    localConfig = MQTTConfig.load_from_json()
    try:
        print("fetching data....")
        remoteConfig = MQTTConfig.from_dict(get_data_from_api(api_url))
        #print(remoteConfig.hostName)
        
        if localConfig != remoteConfig:
            print("saving.....")
            remoteConfig.save_to_json()
            machine.reset()
            return remoteConfig
    except Exception as ex:
        print(ex)
    return localConfig
async def fetch_data():
    try:
        while True:
            try:
                print("fetching data...")
                _fetch_()
                await asyncio.sleep(60)
            except:
                print("Exiting...")
                break
    except:
        pass
    

# Example usage

#get_data_from_api(api_url)
#root = MQTTConfig.from_dict(get_data_from_api(api_url))
#root.save_to_json()



