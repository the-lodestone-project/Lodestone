from typing import Dict, List, Optional, Union
from lodestonegpt.models.base import BaseModel
import requests
import g4f
import time

from g4f.Provider import (
    AItianhu,
    Aichat,
    Bard,
    Bing,
    ChatBase,
    ChatgptAi,
    OpenaiChat,
    Vercel,
    You,
    Yqcloud,
)

import g4f, asyncio

_providers = [
    g4f.Provider.Liaobots,
    g4f.Provider.GeekGpt,
    # g4f.Provider.Bing,
    g4f.Provider.Phind
]

_backup = [
    g4f.Provider.Yqcloud,
    g4f.Provider.AiAsk,
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.ChatgptAi,
    g4f.Provider.FreeGpt,
    g4f.Provider.GPTalk,
    g4f.Provider.GptForLove,
    g4f.Provider.GptGo,
    g4f.Provider.Llama2,
    g4f.Provider.NoowAi,
]

try:
    from transformers import StoppingCriteria

    class StopOnTokens(StoppingCriteria):
        def __call__(self, input_ids, scores, **kwargs) -> bool:
            stop_ids = [50278, 50279, 50277, 1, 0]
            for stop_id in stop_ids:
                if input_ids[0][-1] == stop_id:
                    return True
            return False

except ImportError:
    pass


class HuggingFaceApi(BaseModel):
    def __init__(self, API_TOKEN, model="stabilityai/stablelm-tuned-alpha-7b",):
        import torch

        try:
            from transformers import (
                AutoModelForCausalLM,
                AutoTokenizer,
                StoppingCriteria,
                StoppingCriteriaList,
            )
        except ImportError as e:
            raise ImportError(
                "Please install transformers (pip install transformers) to use hugging face model."
            ) from e

        super(HuggingFaceApi, self).__init__()
        self.model = f"https://api-inference.huggingface.co/models/{model}"
        self.api_token = {"Authorization": f"Bearer {API_TOKEN}"}
        self.load_in_8bit= False
        self.stopping_criteria = StoppingCriteriaList([StopOnTokens()])

    def chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
    ) -> str:
        # response = requests.post(self.model, headers=self.api_token, json={"inputs": f"{messages}", "wait_for_model": True}).json()
        responses = []
        def run_provider(provider: g4f.Provider.BaseProvider):
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4,
                    messages=messages,
                    provider=provider,
                )
                if response != "":
                    if not "vh" in str(response):
                        if len(str(response)) > 130:
                            
                            responses.append(str(response).replace("\n", ""))
                            return str(response)
            except Exception as e:
                print(e)
                pass
                
        def run_all():
            output = 'got an error'
            for provider in _providers:
                output = run_provider(provider)
            return output
            
        def run_all_backup():
            output = 'got an error'
            for provider in _backup:
                output = run_provider(provider)
            return output
            
        

        # response = run_all_backup()
        while True:
            try:
                response = g4f.ChatCompletion.create(
                    model=g4f.models.gpt_4_32k_0613,
                    messages=messages,
                )  #
                return str(response)
            except:
                print("got an error, retrying...")
                output = run_all_backup()
                return str(output)

    def encode_messages(self, messages: List[Dict[str, str]]) -> str:
        message_format = {
            "system": "<|SYSTEM|>{0}",
            "user": "<|USER|>{0}",
            "assistant": "<|ASSISTANT|>{0}",
        }

        data = []
        for message in messages:
            data.append(message_format[message["role"]].format(message["content"]))
        data.append(message_format["assistant"].format(""))
        print(message_format)
        return "".join(data)

    def count_tokens(self, messages: Union[List[Dict[str, str]], str]) -> int:
        return 10

    def get_token_limit(self):
        return 1024

    def config(self):
        cfg = super().config()
        cfg.update(
            {
                "model": self.model,
                "load_in_8bit": self.load_in_8bit,
            }
        )
        return cfg

    @classmethod
    def from_config(cls, config):
        return cls(config["model"], config["load_in_8_bit"])
