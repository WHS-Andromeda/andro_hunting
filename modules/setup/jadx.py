import subprocess
import os
import requests as rq
from tqdm import tqdm
import zipfile


def setup_jadx():
    dnld_url = "https://github.com/skylot/jadx/releases/download/v1.5.0/jadx-1.5.0.zip"
    dnld_path = "jadx.zip"
    output_dir = "jadx-1.5.0"
    if os.path.isdir(output_dir):
        print("jadx already exists, skipping download.")
        return
    print("Downloading jadx from GitHub...")
    response = rq.get(dnld_url, stream=True)
    with open(dnld_path, "wb") as file:
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="iB",
            unit_scale=True,
            bar_format="{l_bar}•{bar}• {n_fmt}/{total_fmt}",
            desc="Downloading jadx",
        )
        for data in response.iter_content(chunk_size=1024):
            progress_bar.update(len(data))
            file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
            return
    print("Downloaded jadx successfully.")
    unzip_jadx(dnld_path, output_dir)


def unzip_jadx(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print("Unzipped jadx successfully.")
