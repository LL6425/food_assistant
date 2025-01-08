class GuardianPrompt:
    def __init__(self):
        self.system_description = f"Act as a guardian whose task is assessing whether or not the prompt is food related."

    def get_guardian_prompt(self, prompt: str) -> str:
        return f"""The following request is provided: "{prompt}". Is it a food related request?"""
