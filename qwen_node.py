import folder_paths
import os
from llama_cpp import Llama
import copy
from typing_extensions import TypedDict, Literal
from typing import List, Optional


_choice = ["YES", "NO"]
_system_prompts = [
    "You are a helpful assistant.",
    "你擅长翻译中文到英语。",
    "你擅长文言文翻译为英语。",
    "你是绘画大师，擅长描绘画面细节。",
    "你是剧作家，擅长创作连续的漫画脚本。"
]
def env_or_def(env, default):
	if (env in os.environ):
		return os.environ[env]
	return default


supported_gpt_extensions = set(['.gguf'])



try:
    folder_paths.folder_names_and_paths["GPTcheckpoints"] = (folder_paths.folder_names_and_paths["GPTcheckpoints"][0], supported_gpt_extensions)
except:
    # check if GPTcheckpoints exists otherwise create
    if not os.path.isdir(os.path.join(folder_paths.models_dir, "GPTcheckpoints")):
        os.mkdir(os.path.join(folder_paths.models_dir, "GPTcheckpoints"))
        
    folder_paths.folder_names_and_paths["GPTcheckpoints"] = ([os.path.join(folder_paths.models_dir, "GPTcheckpoints")], supported_gpt_extensions)
    


class QwenLoaderSimple:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
              "ckpt_name": (folder_paths.get_filename_list("GPTcheckpoints"), ),
              "gpu_layers": ("INT", {"default": 0, "min": 0, "max": 25, "step": 1}),
              "n_threads": ("INT", {"default": 8, "min": 1, "max": 100, "step": 1}),
              "max_ctx": ("INT", {"default": 512, "min": 300, "max": 100000, "step": 64}),
              "chat_format":("STRING",{"default": "chatml"})
            }
        }
    


    RETURN_TYPES = ("CUSTOM","STRING")
    RETURN_NAMES = ("model", "model_path")
    FUNCTION = "load_gpt_checkpoint"

    CATEGORY = "Qwen"
    print()
    def load_gpt_checkpoint(
            self, 
            ckpt_name, 
            gpu_layers,
            n_threads,
            max_ctx,
            chat_format
            ):
        ckpt_path = folder_paths.get_full_path("GPTcheckpoints", ckpt_name)
        llm = Llama(model_path=ckpt_path,n_gpu_layers=gpu_layers,verbose=False,n_threads=n_threads, n_ctx=max_ctx, chat_format=chat_format)
        
        return llm, ckpt_path


class QwenSampler:
    
    """
    A custom node for text generation using GPT

    Attributes
    ----------
    max_tokens (`int`): Maximum number of tokens in the generated text.
    temperature (`float`): Temperature parameter for controlling randomness (0.2 to 1.0).
    top_p (`float`): Top-p probability for nucleus sampling.
    logprobs (`int`|`None`): Number of log probabilities to output alongside the generated text.
    echo (`bool`): Whether to print the input prompt alongside the generated text.
    stop (`str`|`List[str]`|`None`): Tokens at which to stop generation.
    frequency_penalty (`float`): Frequency penalty for word repetition.
    presence_penalty (`float`): Presence penalty for word diversity.
    repeat_penalty (`float`): Penalty for repeating a prompt's output.
    top_k (`int`): Top-k tokens to consider during generation.
    stream (`bool`): Whether to generate the text in a streaming fashion.
    tfs_z (`float`): Temperature scaling factor for top frequent samples.
    model (`str`): The GPT model to use for text generation.
    """
    def __init__(self):
        self.temp_prompt = ""
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING",{"forceInput": True} ),
                "model": ("CUSTOM", {"default": ""}),
                "model_path": ("STRING", {"default": "","forceInput": True}),
                "max_tokens": ("INT", {"default": 77}),
                "temperature": ("FLOAT", {"default": 0.9, "min": 0.2, "max": 1.0}),
                "top_p": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 1.0}),
                "frequency_penalty": ("FLOAT", {"default": 0.0}),
                "presence_penalty": ("FLOAT", {"default": 0.0}),
                "repeat_penalty": ("FLOAT", {"default": 1.4,"min": 1.1}),
                "top_k": ("INT", {"default": 50,  "min": 0, "max": 100}),
                "tfs_z": ("FLOAT", {"default": 1.0}),
                "print_output": (["enable", "disable"], {"default": "disable"}),
                "cached": (_choice,{"default": "NO"} ),
                "prefix": ("STRING", {"default": "必须使用英语根据主题描述一张照片，详细描述照片细节："}),
                "system_prompt": (_system_prompts, {"default": "You are a helpful assistant."}),
                
                
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "generate_text"
    CATEGORY = "Qwen"

    def generate_text(self,prompt, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, repeat_penalty, top_k, tfs_z, model,model_path,print_output,cached,prefix,system_prompt):
        
        
        if cached == "NO":
            # Call your GPT generation function here using the provided parameters
            messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"{prefix} {prompt}"
            }
            ]
            stream  = model.create_chat_completion(
                    messages,
                    max_tokens=max_tokens,
                    top_k=top_k,
                    top_p=top_p,
                    temperature=temperature,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    tfs_z=tfs_z,
                   
            #        stream=True,
                    repeat_penalty=repeat_penalty,
                stop=["\n"]
            )

            #print(len(stream))
            #print(stream)
            cont= stream["choices"][0]["message"]["content"]
            cont = cont.strip()
            self.temp_prompt  = cont.strip()
        else:
            cont = self.temp_prompt 
        #remove fist 30 characters of cont
        try:
            if print_output == "enable":
                print(f"Input: {prompt}\nGenerated Text: {cont}")
            return {"ui": {"text": cont}, "result": (cont,)}

        except:
            if print_output == "enable":
                print(f"Input: {prompt}\nGenerated Text: ")
            return {"ui": {"text": " "}, "result": (" ",)}



class TextBox:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "Text": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_value"
    CATEGORY = "Qwen"

    def get_value(self, Text):
        return (Text,)



NODE_CLASS_MAPPINGS = {
    "TextBox": TextBox,
    "Qwen Loader Simple": QwenLoaderSimple,
    "QwenSampler": QwenSampler
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Qwen Loader Simple": "Qwen Loader Simple",
    "QwenSampler": "Qwen Text Sampler",
    "TextBox": "Text Box",
}
