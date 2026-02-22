from .base_agent import AdaptationAgent

class NarradorAgent(AdaptationAgent):
    """Agente narrador para áudio-descrição"""
    
    def __init__(self):
        super().__init__(
            name="Agente Narrador",
            description="Cria versões para áudio e leitura em voz alta",
            adaptation_rules={
                "ritmo": "Pausas naturais para respiração",
                "clareza": "Pronúncia clara de termos técnicos",
                "descrição": "Descrever elementos visuais",
                "estrutura": "Marcadores de navegação por voz"
            }
        )
    
    async def adapt(self, content: str) -> str:
        prompt = f"""
        Adapte para formato de áudio/narração:
        
        REGRAS:
        1. Adicione marcações de pausa [PAUSA]
        2. Descreva elementos visuais em texto
        3. Use pontuação para ritmo natural
        4. Adicione indicadores "Questão 1 de 10..."
        5. Inclua instruções de navegação por voz
        6. Soletrar siglas e termos técnicos
        
        CONTEÚDO ORIGINAL:
        {content}
        
        CONTEÚDO ADAPTADO PARA NARRAÇÃO:
        """
        return await self.generate(prompt)