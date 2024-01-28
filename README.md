## 安装

### 1、下载模型

https://huggingface.co/hahahafofo/Qwen-1_8B-Stable-Diffusion-Prompt-GGUF/tree/main

下载ggml-model-q4_0.gguf到models/GPTcheckpoints

```
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download hahahafofo/Qwen-1_8B-Stable-Diffusion-Prompt-GGUF --local-dir GPTcheckpoints
```

### 2、安装llama-cpp-python

下载对应版本的whl
https://github.com/abetlen/llama-cpp-python/releases

安装对应版本的whl
```
pip install llama_cpp_python-0.2.33-xxx.whl 
```
请确保版本高于或等于 v0.2.33

### 3、安装插件
Clone the repository: git clone https://github.com/zhongpei/Comfyui-Qwen-Prompt
to your ComfyUI custom_nodes directory