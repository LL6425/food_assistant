from groq import Groq

from src.prompt.guardian import GuardianPrompt
from src.conf.data_model.control import InputValidation


class GroqGuardian:
    def __init__(
        self,
        groq_api_key: str,
        prompt: GuardianPrompt,
        model: str = "llama3-70b-8192",
    ):
        self.client = Groq(api_key=groq_api_key)
        self.prompt = prompt
        self.model = model

    def validate(self, prompt: str) -> bool:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.prompt.system_description},
                {
                    "role": "user",
                    "content": self.prompt.get_guardian_prompt(prompt=prompt),
                },
            ],
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        )

        return InputValidation.model_validate_json(
            chat_completion.choices[0].message.content
        ).is_valid
