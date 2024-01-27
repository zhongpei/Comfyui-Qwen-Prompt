# code based on pysssss repo
import importlib.util
import glob
import os
import sys
from .install import get_ext_dir,check_and_install
import folder_paths
import traceback
from .qwen_node import QwenLoaderSimple,QwenSampler

NODE_CLASS_MAPPINGS = {
    "Qwen Loader Simple": QwenLoaderSimple,
    "QwenSampler": QwenSampler
}
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen Loader Simple": "Qwen Loader Simple",
    "QwenSampler": "Qwen Text Sampler"
}


  




#LLAMA DEPENTENCIES
check_and_install('packaging')
check_and_install('py-cpuinfo',"cpuinfo")
check_and_install('scikit-build',"skbuild")
check_and_install('typing')
check_and_install('diskcache')
check_and_install('llama_cpp')





__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]