from typing import List, Dict, Type

from groq import Groq
from pydantic import BaseModel

from src.prompt.guardian import GuardianPrompt
from src.conf.data_model.llm import Guardian
from src.conf.data_model.tools import RecipeSuggest, ChatBot
from src.conf.data_model.output import Recipe, Text


class GroqGuardian(Guardian):
    def __init__(
        self,
        guardian_prompt: GuardianPrompt
    ):
        Guardian.__init__(self, guardian_prompt=guardian_prompt)

    def validate(self, client: Groq, model: str, history: List[Dict], prompt: str) -> bool:

        history = self.complete_history(history=history, prompt=prompt)

        chat_completion = client.chat.completions.create(
            messages=history,
            model=model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        )

        return self.output_structure.model_validate_json(
            chat_completion.choices[0].message.content
        ).is_valid
    

class GroqRecipeSuggest(RecipeSuggest):
    def __init__(
        self, client, model:str
    ):
        RecipeSuggest.__init__(self, client=client, model=model)

    def __call__(self, inp: Text) -> Recipe:

        history = self.require_struct_output(history=[], prompt=inp.text)

        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        )

        return self.json_to_model(
            chat_completion.choices[0].message.content
        )
    
class GroqChatBot(ChatBot):
    def __init__(
        self, client, model:str
    ):
        ChatBot.__init__(self, client=client, model=model)

    def __call__(self, inp: Text) -> Text:

        history = self.require_struct_output(history=[], prompt=inp.text)

        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        )

        return chat_completion.choices[0].message.content
