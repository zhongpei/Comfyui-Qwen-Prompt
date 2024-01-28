## 安装ComfyUI Qwen Prompt插件指南

### 第1步：下载模型

首先，请从以下链接下载Qwen-1.8B稳定扩散提示GGUF模型：https://huggingface.co/hahahafofo/Qwen-1_8B-Stable-Diffusion-Prompt-GGUF/tree/main

您需要将`ggml-model-q4_0.gguf`文件保存到系统上的`models/GPTcheckpoints`目录中。


可以使用镜像，请在终端中执行以下命令：

```
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download --resume-download hahahafofo/Qwen-1_8B-Stable-Diffusion-Prompt-GGUF --local-dir GPTcheckpoints
```

### 第2步：安装llama-cpp-python

接下来，从此链接下载适合版本的llama-cpp-python文件：https://github.com/abetlen/llama-cpp-python/releases

下载正确的轮子文件后，使用pip进行安装。例如：

```
pip install llama_cpp_python-0.2.33-xxx.whl
```

请确保您安装的版本是v0.2.33或更高。

### 第3步：安装插件

最后，将ComfyUI Qwen Prompt存储库克隆到您的ComfyUI custom_nodes目录中。使用以下命令克隆存储库：

```
git clone https://github.com/zhongpei/Comfyui-Qwen-Prompt
```

按照这些步骤操作，您应该已经成功安装了ComfyUI Qwen Prompt插件。




# English

## Installation Instructions for the ComfyUI Qwen Prompt Plugin

### Step 1: Download the Model

To begin, download the Qwen-1.8B Stable Diffusion Prompt GGUF model from the following URL: https://huggingface.co/hahahafofo/Qwen-1_8B-Stable-Diffusion-Prompt-GGUF/tree/main

You need to save the `ggml-model-q4_0.gguf` file into the `models/GPTcheckpoints` directory on your system. 

### Step 2: Install llama-cpp-python

Next, download the appropriate version of the llama-cpp-python wheel file from this link: https://github.com/abetlen/llama-cpp-python/releases

Once you have the correct wheel file, install it using pip. For example:

```
pip install llama_cpp_python-0.2.33-xxx.whl
```

Ensure that the version you install is v0.2.33 or higher.

### Step 3: Install the Plugin

Finally, clone the ComfyUI Qwen Prompt repository into your ComfyUI custom_nodes directory. Use the following command to clone the repository:

```
git clone https://github.com/zhongpei/Comfyui-Qwen-Prompt
```

With these steps, you should have successfully installed the ComfyUI Qwen Prompt plugin.