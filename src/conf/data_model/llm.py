import json
from typing import List, Dict, Type

from pydantic import BaseModel

from src.prompt.guardian import GuardianPrompt

class StructOutput:

    def __init__(self):

        self.indent = 1

    def get_system_add(self, output_structure: Type[BaseModel]):

        return f"The JSON answer must use the schema: {json.dumps(output_structure.model_json_schema(), indent=self.indent)}"

class Guardian(StructOutput):
    def __init__(self, guardian_prompt: GuardianPrompt, valid_structure: Type[BaseModel]):
        super().__init__()
        self.guardian_prompt = guardian_prompt
        self.valid_structure = valid_structure

    def _complete_history(
        self, history: List[Dict[str, str]], prompt: str
    ) -> List[Dict[str, str]]:
        return history + [
            {
                "role": "system",
                "content": self.guardian_prompt.system_description + ' ' + self.get_system_add(output_structure=self.valid_structure)
            },
            {
                "role": "user",
                "content": self.guardian_prompt.get_guardian_prompt(prompt=prompt)
            }
        ]
    
    def validate(self, history: List[Dict], prompt: str) -> bool:

        pass


