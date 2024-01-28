# code based on pysssss repo
import importlib.util
import glob
import os
import sys
from .install import get_ext_dir,check_and_install
import folder_paths
import traceback
from .qwen_node import NODE_CLASS_MAPPINGS as NODE_CLASS_MAPPINGS_QWEN, NODE_DISPLAY_NAME_MAPPINGS as NODE_DISPLAY_NAME_MAPPINGS_QWEN
from .format_prompt import NODE_CLASS_MAPPINGS as NODE_CLASS_MAPPINGS_FORMAT_PROMPT, NODE_DISPLAY_NAME_MAPPINGS as NODE_DISPLAY_NAME_MAPPINGS_FORMAT_PROMPT 

NODE_CLASS_MAPPINGS = {}
NODE_CLASS_MAPPINGS.update(NODE_CLASS_MAPPINGS_QWEN)
NODE_CLASS_MAPPINGS.update(NODE_CLASS_MAPPINGS_FORMAT_PROMPT)
# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS.update(NODE_DISPLAY_NAME_MAPPINGS_QWEN)
NODE_DISPLAY_NAME_MAPPINGS.update(NODE_DISPLAY_NAME_MAPPINGS_FORMAT_PROMPT)



  




#LLAMA DEPENTENCIES
check_and_install('packaging')
check_and_install('py-cpuinfo',"cpuinfo")
check_and_install('scikit-build',"skbuild")
check_and_install('typing')
check_and_install('diskcache')
check_and_install('llama_cpp')





__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]