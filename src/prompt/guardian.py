import json

from src.conf.data_model.control import InputValidation

class GuardianPrompt:

    def __init__(self):

        self.system_description = f"Act as a guardian whose task is assessing whether or not the prompt is food related.\nThe JSON answer must use the schema: \n{json.dumps(InputValidation.model_json_schema(), indent=2)}"

    def get_guardian_prompt(self, prompt: str) -> str:

        return f"""The following request is provided: \n{prompt} \nIs it a food related request?"""

    