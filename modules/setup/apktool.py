import os
import requests as rq
from tqdm import tqdm


def setup_apktool():
    dnld_url = "https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar"
    dnld_path = "apktool.jar"
    if os.path.isfile(dnld_path):
        print("apktool already exists, skipping download.")
        return
    print("Downloading apktool from Bitbucket...")
    response = rq.get(dnld_url, stream=True)
    with open(dnld_path, "wb") as file:
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="iB",
            unit_scale=True,
            bar_format="{l_bar}•{bar}• {n_fmt}/{total_fmt}",
            desc="Downloading apktool",
        )
        for data in response.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
            return
    print("Downloaded apktool successfully.")
