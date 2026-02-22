from adk import Orchestrator, Agent
from google import genai
from google.adk.tools import FunctionTool
from agents import TEAAgent, SurdezAgent, TDAHAgent, DislexiaAgent, NarradorAgent
from agents import (
    TEAAgent,
    SurdezAgent,
    TDAHAgent,
    DislexiaAgent,
    NarradorAgent
)

class ProvaOrchestrator:
    """Orquestrador principal que coordena os agentes de adaptação"""
    
    def _init_(self):
        self.agents = {
            "tea": TEAAgent(),
            "surdez": SurdezAgent(),
            "tdah": TDAHAgent(),
            "dislexia": DislexiaAgent(),
            "narrador": NarradorAgent()
        }
        
        # Criar orquestrador ADK
        self.orchestrator = Orchestrator(
            name="Orquestrador de Adaptação",
            model="gemini-3-flash-preview",
            agents=list(self.agents.values()),
            instructions=self._get_orchestrator_instructions()
        )
    
    def _get_orchestrator_instructions(self) -> str:
        return """
        Você é o orquestrador de um sistema de adaptação de provas educacionais.
        
        Sua função é:
        1. Receber o conteúdo da prova/questão
        2. Identificar o tipo de adaptação solicitada
        3. Delegar para o agente especializado correto
        4. Validar e refinar o resultado
        5. Retornar o conteúdo adaptado
        
        Agentes disponíveis:
        - TEA: Transtorno do Espectro Autista
        - Surdez: Deficiência auditiva
        - TDAH: Déficit de Atenção e Hiperatividade
        - Dislexia: Dificuldades de leitura
        - Narrador: Conversão para áudio/narração
        
        Sempre mantenha a integridade acadêmica do conteúdo.
        """
    
    async def process_prova(
        self, 
        content: str, 
        adaptation_type: str,
        difficulty_level: str = "medium"
    ) -> dict:
        """
        Processa uma prova e retorna versão adaptada
        
        Args:
            content: Conteúdo da prova (texto extraído do PDF/DOCX)
            adaptation_type: Tipo de adaptação (tea, surdez, tdah, dislexia, narrador)
            difficulty_level: Nível de adaptação (easy, medium, hard)
        
        Returns:
            Dict com conteúdo adaptado e metadados
        """
        
        # Validar tipo de adaptação
        if adaptation_type not in self.agents:
            raise ValueError(f"Tipo de adaptação inválido: {adaptation_type}")
        
        # Selecionar agente
        agent = self.agents[adaptation_type]
        
        # Aplicar modificador de dificuldade
        modified_content = self._apply_difficulty(content, difficulty_level)
        
        # Executar adaptação
        adapted_content = await agent.adapt(modified_content)
        
        # Pós-processamento e validação
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
        """Ajusta o conteúdo baseado no nível de dificuldade"""
        difficulty_prompts = {
            "easy": "Simplifique ao máximo, use vocabulário básico",
            "medium": "Mantenha complexidade moderada",
            "hard": "Mantenha a complexidade original, apenas adapte o formato"
        }
        return f"[NÍVEL: {difficulty_prompts.get(level, 'medium')}]\n\n{content}"
    
    async def _validate_adaptation(
        self, 
        original: str, 
        adapted: str, 
        adaptation_type: str
    ) -> str:
        """Valida se a adaptação mantém a integridade do conteúdo"""
        
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
        
        model = genai.GenerativeModel("gemini-3-flash-preview")
        response = await model.generate_content_async(validation_prompt)
        return response.text if response.text else adapted