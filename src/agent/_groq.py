from typing import Iterable, Type


from groq import Groq

from src.llm import GroqGuardian
from src.prompt.system import SystemPrompt
from src.conf.data_model.tools import Tool
from src.agent import FoodAssistant
from src.conf.data_model.pipeline import Pipeline


class GroqFoodAssistant(FoodAssistant):
    def __init__(
        self,
        api_key: str,
        system: SystemPrompt,
        guardian: GroqGuardian,
        tools: Iterable[Type[Tool]] = None,
        model: str = "llama-3.3-70b-versatile"
    ):
        FoodAssistant.__init__(
            self,
            api_key=api_key,
            system=system,
            guardian=guardian,
            model=model,
            tools=tools
        )

    def _get_client(self, api_key: str) -> Groq:
        return Groq(api_key=api_key)
    
    def execute(self, prompt):

        self._guard(prompt=prompt)

        pipeline: Pipeline = self.json_to_model(self.client.chat.completions.create(
            messages=self.require_struct_output(history=self._provide_tools(history=self.history), prompt=prompt),
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.0,
            stream=False
        ).choices[0].message.content)

        answer = pipeline.execute(tools_d=self.tools_d) # as text

        print(1)


if __name__=='__main__':

    import os

    from src.llm._groq import GroqRecipeSuggest, GroqChatBot
    from src.prompt.guardian import GuardianPrompt
    from src.conf.data_model.output import Recipe


    gfa = GroqFoodAssistant(api_key=os.environ['GROQ_API_KEY'],
                            guardian=GroqGuardian(guardian_prompt=GuardianPrompt()),
                            system=SystemPrompt(),
                            tools=[GroqRecipeSuggest, GroqChatBot])
    
    gfa.execute('Provide lasagne recipe')
        

