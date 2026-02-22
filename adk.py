from google import genai

class Agent:
    def __init__(self, name, model, description, instructions):
        self.name = name
        self.model = model
        self.description = description
        self.instructions = instructions
        self.client = genai.Client()

    def run(self, text: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=f"{self.instructions}\n\n{text}"
        )
        return response.text


class Orchestrator:
    def __init__(self, agents: list[Agent]):
        self.agents = agents

    def run(self, text: str) -> dict:
        results = {}
        for agent in self.agents:
            results[agent.name] = agent.run(text)
        return results
