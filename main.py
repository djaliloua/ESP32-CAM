from camera_module.camera_module import start_streaming_video
import time
import _thread
import asyncio
from wifi_module.wifi import do_connect, read_wifi_json
from update_service.fetch_remote_data import fetch_data, _fetch_


################## WIFI CONNECTION #########################
do_connect()
############################################################
time.sleep(1)

config = _fetch_()

time.sleep(1)


async def main():
    stream_task = asyncio.create_task(start_streaming_video(config))
    fetch_data_task = asyncio.create_task(fetch_data())
    await asyncio.gather(stream_task, fetch_data_task)
            

if __name__ == "__main__":
    asyncio.run(main())

