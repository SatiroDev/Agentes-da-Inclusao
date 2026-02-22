from google.adk import Agent

class AdaptationAgent(Agent):
    """Classe base para agentes de adaptação"""
    
    def __init__(self, name: str, description: str, adaptation_rules: dict):
        super()._init_(
            name=name,
            model="gemini-3.0-flash",
            description=description,
            instructions=self._build_instructions(adaptation_rules)
        )
        self.adaptation_rules = adaptation_rules
    
    def _build_instructions(self, rules: dict) -> str:
        return f"""
        Você é um especialista em adaptação de conteúdo educacional.
        Regras de adaptação:
        {rules}
        """