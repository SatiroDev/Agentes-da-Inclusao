from .base_agent import AdaptationAgent

class SurdezAgent(AdaptationAgent):
    """Agente para alunos surdos ou com deficiência auditiva"""
    
    def __init__(self):
        super().__init__(
            name="Agente Surdez",
            description="Otimiza conteúdo visual para alunos surdos",
            adaptation_rules={
                "visual": "Priorizar elementos visuais e gráficos",
                "texto": "Simplificar estruturas gramaticais complexas",
                "vocabulário": "Glossário visual de termos técnicos",
                "libras": "Sugerir sinais em LIBRAS quando relevante",
                "estrutura": "Usar bullets, tabelas e diagramas"
            }
        )
    
    async def adapt(self, content: str) -> str:
        prompt = f"""
        Adapte para um aluno surdo/deficiente auditivo:
        
        REGRAS:
        1. Transforme informações auditivas em visuais
        2. Simplifique estruturas gramaticais (português é L2)
        3. Use tabelas, listas e diagramas
        4. Adicione glossário visual para termos técnicos
        5. Destaque palavras-chave em negrito
        6. Evite expressões que dependem de contexto sonoro
        
        CONTEÚDO ORIGINAL:
        {content}
        
        CONTEÚDO ADAPTADO:
        """
        return await self.generate(prompt)