from google import genai
from agents import TEAAgent, SurdezAgent, TDAHAgent, DislexiaAgent, NarradorAgent


class ProvaOrchestrator:
    """Orquestrador principal que coordena os agentes de adaptação"""

    def __init__(self):
        self.client = genai.Client()

        self.agents = {
            "tea": TEAAgent(),
            "surdez": SurdezAgent(),
            "tdah": TDAHAgent(),
            "dislexia": DislexiaAgent(),
            "narrador": NarradorAgent()
        }

    async def process_prova(
        self,
        content: str,
        adaptation_type: str,
        difficulty_level: str = "medium"
    ) -> dict:

        if adaptation_type not in self.agents:
            raise ValueError(f"Tipo de adaptação inválido: {adaptation_type}")

        agent = self.agents[adaptation_type]

        modified_content = self._apply_difficulty(content, difficulty_level)

        adapted_content = await agent.adapt(modified_content)

        validated_content = await self._validate_adaptation(
            original=content,
            adapted=adapted_content,
            adaptation_type=adaptation_type
        )

        return {
            "original": content,
            "adapted": validated_content,
            "adaptation_type": adaptation_type,
            "difficulty_level": difficulty_level,
            "agent_used": agent.name,
            "metadata": {
                "word_count_original": len(content.split()),
                "word_count_adapted": len(validated_content.split())
            }
        }

    def _apply_difficulty(self, content: str, level: str) -> str:
        difficulty_prompts = {
            "easy": "Simplifique ao máximo, use vocabulário básico",
            "medium": "Mantenha complexidade moderada",
            "hard": "Mantenha a complexidade original, apenas adapte o formato"
        }

        instruction = difficulty_prompts.get(level, difficulty_prompts["medium"])
        return f"[NÍVEL: {instruction}]\n\n{content}"

    async def _validate_adaptation(
        self,
        original: str,
        adapted: str,
        adaptation_type: str
    ) -> str:

        validation_prompt = f"""
Verifique se a adaptação mantém:

1. Todas as questões originais
2. As respostas corretas inalteradas
3. O nível de dificuldade acadêmica

ORIGINAL:
{original[:1000]}

ADAPTADO:
{adapted[:1000]}

Se houver problemas, corrija e retorne a versão corrigida.
Se estiver OK, retorne o texto adaptado sem alterações.
"""

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=validation_prompt
        )

        return response.text if response.text else adapted