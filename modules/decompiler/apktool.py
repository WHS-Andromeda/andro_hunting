import subprocess
import os
from concurrent.futures import ProcessPoolExecutor


def decompileApkUsingApktool(package_name):
    apkPath = f"./data/apk/{package_name}.apk"
    output_directory = f"./data/decompiled/apktool_{package_name}/"
    command = f"java -jar apktool.jar d {apkPath} -o {output_directory}"

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


# def decompileApkUsingApktoolFutures(package_names, num_workers=None):
#     if num_workers is None:
#         num_workers = os.cpu_count() or 1
#     with ProcessPoolExecutor(max_workers=num_workers) as executor:
#         executor.map(decompileApkUsingApktool, package_names)
