from .base_agent import AdaptationAgent

class DislexiaAgent(AdaptationAgent):
    """Agente para alunos com dislexia"""
    
    def __init__(self):
        super().__init__(
            name="Agente Dislexia",
            description="Adapta textos para facilitar leitura",
            adaptation_rules={
                "fonte": "Recomendar OpenDyslexic ou similar",
                "espaçamento": "Aumentar entre linhas e palavras",
                "alinhamento": "Texto alinhado à esquerda",
                "contraste": "Alto contraste, evitar branco puro",
                "estrutura": "Frases curtas, vocabulário simples"
            }
        )
    
    async def adapt(self, content: str) -> str:
        prompt = f"""
        Adapte para um aluno com dislexia:
        
        REGRAS:
        1. Frases curtas (máx 15-20 palavras)
        2. Uma ideia por parágrafo
        3. Evite palavras com grafias similares próximas
        4. Use marcadores visuais para listas
        5. Adicione espaçamento extra entre seções
        6. Substitua palavras complexas por sinônimos simples
        7. Evite blocos densos de texto
        8. Use negrito para termos importantes
        
        CONTEÚDO ORIGINAL:
        {content}
        
        CONTEÚDO ADAPTADO:
        """
        return await self.generate(prompt)