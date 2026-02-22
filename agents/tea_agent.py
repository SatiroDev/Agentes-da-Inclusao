from .base_agent import AdaptationAgent

class TEAAgent(AdaptationAgent):
    """Agente especializado para Transtorno do Espectro Autista"""
    
    def __init__(self):
        super().__init__(
            name="Agente TEA",
            description="Adapta conteúdo para alunos com TEA",
            adaptation_rules={
                "linguagem": "Clara, direta e literal (evitar metáforas)",
                "estrutura": "Sequencial e previsível com roteiros visuais",
                "instruções": "Passo a passo numerado",
                "estímulos": "Reduzir sobrecarga sensorial",
                "contexto": "Fornecer contexto explícito para situações sociais",
                "tempo": "Permitir tempo extra para processamento"
            }
        )
    
    async def adapt(self, content: str) -> str:
        prompt = f"""
        Adapte o seguinte conteúdo educacional para um aluno com TEA:
        
        REGRAS DE ADAPTAÇÃO:
        1. Use linguagem clara e literal (sem metáforas ou expressões idiomáticas)
        2. Organize em passos numerados e sequenciais
        3. Adicione apoios visuais quando possível (descrições de diagramas)
        4. Mantenha formato consistente e previsível
        5. Explicite informações implícitas
        6. Use frases curtas e diretas
        
        CONTEÚDO ORIGINAL:
        {content}
        
        CONTEÚDO ADAPTADO:
        """
        return await self.generate(prompt)