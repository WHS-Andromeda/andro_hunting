import subprocess
import os
from concurrent.futures import ProcessPoolExecutor


def decompileApkUsingJadx(package_name):
    apkPath = f"./data/apk/{package_name}.apk"
    output_directory = f"./data/decompiled/{package_name}/"
    command = f"./jadx/build/jadx/bin/jadx -d {output_directory} {apkPath}"

    if os.path.isdir(output_directory):
        return True

    try:
        result = subprocess.run(
            command, shell=True, check=True, text=True, capture_output=True
        )
        print("Decompilation completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to decompile the APK:", e)
        print(e.output)
