from typing import List, Dict, Type

from groq import Groq
from pydantic import BaseModel

from src.prompt.guardian import GuardianPrompt
from src.conf.data_model.llm import Guardian
from src.conf.data_model.control import InputValidation

class GroqGuardian(Guardian):
    def __init__(
        self,
        groq_api_key: str,
        guardian_prompt: GuardianPrompt = None,
        model: str = "llama3-70b-8192",
        valid_structure: Type[BaseModel] = InputValidation
    ):
        super().__init__(guardian_prompt=guardian_prompt, valid_structure=valid_structure)

        self.client = Groq(api_key=groq_api_key)
        self.model = model

    def validate(self, history: List[Dict], prompt: str) -> bool:

        history = self._complete_history(history=history, prompt=prompt)

        chat_completion = self.client.chat.completions.create(
            messages=history,
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        )

        return InputValidation.model_validate_json(
            chat_completion.choices[0].message.content
        ).is_valid
