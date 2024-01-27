import asyncio
import os
import json
import shutil
import inspect
import aiohttp
from server import PromptServer
from tqdm import tqdm
import requests
import subprocess
import platform
import importlib.util
import torch
import folder_paths
import sys

config = None




def check_nvidia_gpu():
    try:
        # Utilizza torch per verificare la presenza di una GPU NVIDIA
        return torch.cuda.is_available() and 'NVIDIA' in torch.cuda.get_device_name(0)
    except Exception as e:
        print(f"Error while checking for NVIDIA GPU: {e}")
        return False

def get_cuda_version():
    try:
        if torch.cuda.is_available():
            cuda_version = torch.version.cuda.replace(".","").strip()

            return "cu"+cuda_version
        else:
            return "No NVIDIA GPU available"
    except Exception as e:
        print(f"Error while checking CUDA version: {e}")
        return "Unable to determine CUDA version"

def check_avx2_support():
    import cpuinfo
    try:
        info = cpuinfo.get_cpu_info()
        return 'avx2' in info['flags']
    except Exception as e:
        print(f"Error while checking AVX2 support: {e}")
        return False

def get_python_version():
    if "3.9" in platform.python_version():
        return "39"
    elif "3.10" in platform.python_version():
        return "310"
    elif "3.11" in platform.python_version():
        return "311"
    else:
        return None


def get_os():
    return platform.system()

def get_os_bit():
    return platform.architecture()[0].replace("bit","")

def get_platform_tag():
    #return the first tag in the list of tags
    try:
        import packaging.tags
        return list(packaging.tags.sys_tags())[0]
    except:
        return None
def get_last_llcpppy_version():
    try:
        import requests
    
        response = requests.get("https://api.github.com/repos/abetlen/llama-cpp-python/releases/latest")
        return response.json()["tag_name"] .replace("v","")
    except:
        return "0.2.33"


def check_and_install(package, import_name=""):
    if import_name == "":
        import_name = package
    try:
        importlib.import_module(import_name)
        print(f"{import_name} is already installed.")
    except ImportError:
        print(f"Installing {import_name}...")
        if package == "llama_cpp":
            install_llama()
        else:
            install_package(package)

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", package])

def install_llama():


    try:
        gpu = check_nvidia_gpu()
        avx2 = check_avx2_support()
        lcpVersion = get_last_llcpppy_version()
        python_version = get_python_version()
        os = get_os()
        os_bit = get_os_bit()
        platform_tag = get_platform_tag()
        print(f"Python version: {python_version}")
        print(f"OS: {os}")
        print(f"OS bit: {os_bit}")
        print(f"Platform tag: {platform_tag}")
        if python_version == None:
            print("Unsupported Python version. Please use Python 3.9, 3.10 or 3.11.")
            return
        

        #python -m pip install llama-cpp-python --force-reinstall --no-deps --index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/AVX2/cu117
        if avx2:
            avx="AVX2"
        else:
            avx="AVX"

        #if gpu:
        #    cuda = get_cuda_version()
        #    subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-cpp-python", "--no-cache-dir", "--force-reinstall", "--no-deps" , f"--index-url=https://jllllll.github.io/llama-cpp-python-cuBLAS-wheels/{avx}/{cuda}"])
        #else:
        print(f"pip install https://github.com/abetlen/llama-cpp-python/releases/download/v{lcpVersion}/llama_cpp_python-{lcpVersion}-{platform_tag}.whl")
        subprocess.check_call([sys.executable, "-m", "pip", "install", f"https://github.com/abetlen/llama-cpp-python/releases/download/v{lcpVersion}/llama_cpp_python-{lcpVersion}-{platform_tag}.whl"])
    except Exception as e:
        print(f"Error while installing LLAMA: {e}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install","--upgrade","--force-reinstall","--no-cache-dir", f"llama_cpp_python={lcpVersion}"])
        except Exception as e:
            print(f"Error while installing LLAMA: {e}")

# llama wheels https://github.com/jllllll/llama-cpp-python-cuBLAS-wheels

def check_module(package):
    import importlib
    try:
        print("Detected: ", package)
        importlib.import_module(package)
        return True
    except ImportError:
        return False



def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir


def get_comfy_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(inspect.getfile(PromptServer))
    if subpath is not None:
        dir = os.path.join(dir, subpath)

    dir = os.path.abspath(dir)

    if mkdir and not os.path.exists(dir):
        os.makedirs(dir)
    return dir







async def download_to_file(url, destination, update_callback=None, is_ext_subpath=True, session=None):
    if is_ext_subpath:
        destination = get_ext_dir(destination)
    with open(destination, mode='wb') as f:
        download(url, f, update_callback, session)




def is_inside_dir(root_dir, check_path):
    root_dir = os.path.abspath(root_dir)
    if not os.path.isabs(check_path):
        check_path = os.path.abspath(os.path.join(root_dir, check_path))
    return os.path.commonpath([check_path, root_dir]) == root_dir


def get_child_dir(root_dir, child_path, throw_if_outside=True):
    child_path = os.path.abspath(os.path.join(root_dir, child_path))
    if is_inside_dir(root_dir, child_path):
        return child_path
    if throw_if_outside:
        raise NotADirectoryError(
            "Saving outside the target folder is not allowed.")
    return None