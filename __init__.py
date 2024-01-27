# code based on pysssss repo
import importlib.util
import glob
import os
import sys
from .install import get_ext_dir,check_and_install,downloader
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
check_and_install('typing')
check_and_install('diskcache')
check_and_install('llama_cpp')


py = get_ext_dir("py")
files = glob.glob("*.py", root_dir=py, recursive=False)

for file in files:
    try:
        name = os.path.splitext(file)[0]
        spec = importlib.util.spec_from_file_location(name, os.path.join(py, file))
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if hasattr(module, "NODE_CLASS_MAPPINGS") and getattr(module, "NODE_CLASS_MAPPINGS") is not None:
            print(f"load {module.NODE_CLASS_MAPPINGS}")
            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
            if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS") and getattr(module, "NODE_DISPLAY_NAME_MAPPINGS") is not None:
                NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
    except Exception as e:
        traceback.print_exc()


__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]