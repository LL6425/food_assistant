import json
from typing import List, Dict, Type

from pydantic import BaseModel

from src.prompt.guardian import GuardianPrompt
from src.conf.data_model.control import InputValidation

class StructOutput:

    indent: int = 1
    output_structure: Type[BaseModel] = None

    def __init__(self):

        assert isinstance(self.indent, int) and self.indent >= 0, "Indent must be a non-negative integer."
        assert issubclass(self.output_structure, BaseModel), "Output structure must be a subclass of pydantic BaseModel."

    def _get_system_add(self):

        return f"The answer must use the JSON schema: {json.dumps(self.output_structure.model_json_schema(), indent=self.indent)}"
    
    def require_struct_output(
        self, history: List[Dict[str, str]], prompt: str
    ) -> List[Dict[str, str]]:
        return history + [
            {
                "role": "system",
                "content": self._get_system_add()
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    
    def json_to_model(self, response: str) -> BaseModel:

        return self.output_structure.model_validate_json(response)

class Guardian(StructOutput):

    output_structure = InputValidation

    def __init__(self, guardian_prompt: GuardianPrompt):
        StructOutput.__init__(self)
        self.guardian_prompt = guardian_prompt

    def complete_history(
        self, history: List[Dict[str, str]], prompt: str
    ) -> List[Dict[str, str]]:
        return history + [
            {
                "role": "system",
                "content": self.guardian_prompt.system_description + ' ' + self._get_system_add()
            },
            {
                "role": "user",
                "content": self.guardian_prompt.get_guardian_prompt(prompt=prompt)
            }
        ]
    
    def validate(self, history: List[Dict], prompt: str) -> bool:

        pass