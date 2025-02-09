import pprint
import time
import requests

streams =  {
    "depth": "Oak-D Stereo Disparity",
    "rgb": "Oak-D RGB"
}

mcm_endpoint = "http://127.0.0.1:6020/streams"

def has_oak_stream(current_streams, name):
    for stream in current_streams:
        if stream["video_and_stream"]["name"] == name:
            return True
    return False


def add_mcm_stream(endpoint):
    name = streams[endpoint]
    new_stream = {
        "name": name,
        "source": "Redirect",
        "stream_information": {
            "endpoints": [
                f"rtsp://127.0.0.1:8554/{endpoint}"
            ],
            "configuration": {
                "type": "redirect"
            },
            "extended_configuration": {
                "thermal": False,
                "disable_mavlink": True
            }
        }
    }

    print(f"adding stream {endpoint}")
    stream_add_response = requests.post(mcm_endpoint, json=new_stream)
    pprint.pprint(stream_add_response.text)


def check_streams():
    while True:
        time.sleep(4)
        current_streams = requests.get(mcm_endpoint).json()
        for endpoint, name in streams.items():
            try:
                if not has_oak_stream(current_streams, name):
                    add_mcm_stream(endpoint)
            except Exception as ex:
                print(ex)
