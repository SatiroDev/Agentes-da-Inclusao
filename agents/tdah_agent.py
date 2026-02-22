from .base_agent import AdaptationAgent

class TDAHAgent(AdaptationAgent):
    """Agente para alunos com TDAH"""
    
    def __init__(self):
        super().__init__(
            name="Agente TDAH",
            description="Divide atividades e adiciona engajamento",
            adaptation_rules={
                "segmentação": "Dividir em blocos de 5-10 minutos",
                "engajamento": "Elementos gamificados e interativos",
                "foco": "Destacar informações essenciais",
                "pausas": "Inserir checkpoints e pausas",
                "recompensas": "Sistema de progresso visível"
            }
        )
    
    async def adapt(self, content: str) -> str:
        prompt = f"""
        Adapte para um aluno com TDAH:
        
        REGRAS:
        1. Divida em micro-tarefas (máximo 5-10 min cada)
        2. Adicione checkboxes de progresso ☐ → ☑
        3. Destaque palavras-chave com *negrito*
        4. Insira pausas estratégicas "⏸️ Pausa: respire fundo!"
        5. Use emojis para engajamento visual 🎯 ✅ 💡
        6. Adicione elementos de gamificação (pontos, níveis)
        7. Mantenha parágrafos curtos (2-3 linhas máx)
        
        CONTEÚDO ORIGINAL:
        {content}
        
        CONTEÚDO ADAPTADO:
        """
        return await self.generate(prompt)