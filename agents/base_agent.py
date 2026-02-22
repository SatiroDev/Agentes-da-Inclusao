from google import genai

class AdaptationAgent:
    """Classe base para agentes de adaptação"""

    def __init__(self, name: str, description: str, adaptation_rules: dict):
        self.name = name
        self.description = description
        self.adaptation_rules = adaptation_rules
        self.client = genai.Client()
        self.instructions = self._build_instructions(adaptation_rules)

    def _build_instructions(self, rules: dict) -> str:
        return f"""
Você é um especialista em adaptação de conteúdo educacional.

Regras de adaptação:
{rules}
"""

    def adapt(self, text: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{self.instructions}\n\nTexto:\n{text}"
        )
        return response.text