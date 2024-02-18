import os
import requests

def download_benchmark(downloadurl : str, destination : str):
    req = requests.get(downloadurl)

    filename = req.url[downloadurl.rfind('/')+1:-11]

    file_path = os.path.join(destination, filename)
    with open(file_path, 'wb') as f:
        for chunk in req.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                