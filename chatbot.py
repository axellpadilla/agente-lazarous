"""
Agente Chatbot usando DSPy y API de OpenRouter
Implementa respuesta de preguntas basada en RAG con simulación de transferencia de agente
"""

import os
from typing import Optional, Dict
import dspy
from rag_knowledge_base import FAQKnowledgeBase
import dotenv


class RAGSignature(dspy.Signature):
    """Firma para respuesta de preguntas basada en RAG"""
    context = dspy.InputField(
        desc="Contexto relevante de la base de conocimiento")
    question = dspy.InputField(desc="Pregunta del usuario")
    answer = dspy.OutputField(desc="Respuesta basada en el contexto")


class TransferDecisionSignature(dspy.Signature):
    """Firma para decidir si la pregunta necesita transferencia de agente"""
    question = dspy.InputField(desc="Pregunta del usuario")
    search_result = dspy.InputField(
        desc="Resultado de la búsqueda en la base de conocimiento")
    should_transfer = dspy.OutputField(
        desc="Si transferir a agente humano (Sí/No)")
    reason = dspy.OutputField(desc="Razón de la decisión")


class LazarusChatbot:
    """
    Chatbot inteligente para Grupo Lazarus
    Usa RAG para responder preguntas desde base de datos FAQ
    Transfiere a agente humano cuando no se encuentra información
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = None,
        excel_file: str = "data_limpia/faq_limpio.csv"
    ):
        """
        Inicializar el chatbot

        Args:
            api_key: Clave API de OpenRouter (o establecer variable de entorno OPENROUTER_API_KEY)
            model: Modelo a usar (por defecto: openai/gpt-3.5-turbo)
            excel_file: Ruta al archivo CSV de FAQ
        """

        # Obtener clave API del parámetro o entorno
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print(
                "⚠ Advertencia: No se proporcionó clave API. Establezca la variable de entorno OPENROUTER_API_KEY.")
            print("⚠ Ejecutándose en modo demo con funcionalidad limitada.")

        # Inicializar base de conocimiento
        self.model = model or os.getenv(
            "OPENROUTER_CHAT_MODEL", "openrouter/gpt-3.5-turbo")
        self.kb = FAQKnowledgeBase(excel_file)

        # Configurar DSPy con OpenRouter
        if self.api_key:
            try:
                lm = dspy.LM(
                    model=self.model,
                    api_key=self.api_key,
                    api_base="https://openrouter.ai/api/v1",
                )
                dspy.settings.configure(lm=lm)
                self.rag_module = dspy.ChainOfThought(RAGSignature)
                self.transfer_module = dspy.ChainOfThought(
                    TransferDecisionSignature)
                print(f"✓ DSPy configurado con modelo: {self.model}")
            except Exception as e:
                print(f"⚠ Error al configurar DSPy: {e}")
                print("⚠ Ejecutándose en modo fallback")
                self.rag_module = None
                self.transfer_module = None
        else:
            self.rag_module = None
            self.transfer_module = None

    def answer(self, question: str) -> Dict[str, any]:
        """
        Responder a una pregunta del usuario usando RAG

        Args:
            question: Pregunta del usuario

        Returns:
            Diccionario con respuesta, fuente y estado de transferencia
        """
        # Buscar en base de conocimiento
        search_result = self.kb.search(question)

        # Preparar respuesta
        response = {
            "question": question,
            "answer": "",
            "source": "knowledge_base",
            "transfer_to_agent": False,
            "transfer_reason": ""
        }

        # Gestionar saludos o conversación casual sin activar transferencia
        if not search_result and self._is_small_talk(question):
            response["answer"] = self._small_talk_reply(question)
            response["source"] = "small_talk"
            return response

        if search_result:
            # Se encontró información relevante
            if self.rag_module:
                # Usar DSPy para generar respuesta contextualizada
                try:
                    context = f"Pregunta relacionada: {search_result['pregunta']}\nRespuesta: {search_result['respuesta']}"
                    result = self.rag_module(
                        context=context, question=question)
                    response["answer"] = result.answer
                except Exception as e:
                    # Respuesta de respaldo directo
                    response["answer"] = search_result['respuesta']
            else:
                # Modo de respaldo - usar respuesta directa
                response["answer"] = search_result['respuesta']

            response["source"] = f"FAQ - Categoría: {search_result['categoria']}"
        else:
            # No se encontró información relevante
            if self.rag_module:
                # Usar LLM para generar respuesta
                try:
                    context = "No hay información relevante en la base de conocimientos para esta pregunta."
                    result = self.rag_module(
                        context=context, question=question)
                    response["answer"] = result.answer
                    response["source"] = "LLM"

                    # Determinar si transferir a agente
                    if self.transfer_module:
                        transfer_result = self.transfer_module(
                            question=question,
                            search_result="sin_resultados"
                        )
                        should_transfer = transfer_result.should_transfer.lower() in [
                            'si', 'sí', 'yes', 'true']
                        if should_transfer and self._is_small_talk(question):
                            should_transfer = False
                        if should_transfer:
                            response["transfer_to_agent"] = True
                            response["transfer_reason"] = transfer_result.reason
                            self._simulate_transfer(question)
                except Exception as e:
                    # Respaldo a transferencia
                    response["transfer_to_agent"] = True
                    response["transfer_reason"] = "Error al generar respuesta con LLM"
                    response["answer"] = (
                        "Lo siento, no tengo información específica sobre esa pregunta en mi base de datos. "
                        "Voy a transferir su consulta a uno de nuestros agentes especializados que podrá ayudarle mejor."
                    )
                    response["source"] = "transfer"
                    self._simulate_transfer(question)
            else:
                # Sin LLM, proceder a transferencia
                if self._is_small_talk(question):
                    response["answer"] = self._small_talk_reply(question)
                    response["source"] = "small_talk"
                else:
                    response["transfer_to_agent"] = True
                    response["transfer_reason"] = "No se encontró información relevante en la base de conocimientos"
                    response["answer"] = (
                        "Lo siento, no tengo información específica sobre esa pregunta en mi base de datos. "
                        "Voy a transferir su consulta a uno de nuestros agentes especializados que podrá ayudarle mejor."
                    )
                    response["source"] = "transfer"
                    self._simulate_transfer(question)

        return response

    def _simulate_transfer(self, question: str) -> None:
        """
        Simular transferencia a agente humano

        Args:
            question: Pregunta que activó la transferencia
        """
        print("\n" + "="*60)
        print("🔄 TRANSFERENCIA A AGENTE HUMANO")
        print("="*60)
        print(f"Pregunta: {question}")
        print("Estado: Conectando con agente disponible...")
        print("Tiempo estimado de espera: 2-3 minutos")
        print("="*60 + "\n")

    def chat(self) -> None:
        """Iniciar sesión de chat interactivo"""
        print("\n" + "="*60)
        print("💬 Chatbot Grupo Lazarus")
        print("="*60)
        print("Hola! Soy el asistente virtual de Grupo Lazarus.")
        print("Puedo responder preguntas sobre nuestros servicios, horarios,")
        print("ubicación, políticas y más.")
        print("\nEscribe 'salir' para terminar la conversación.")
        print("="*60 + "\n")

        while True:
            try:
                question = input("Tú: ").strip()

                if not question:
                    continue

                if question.lower() in ['salir', 'exit', 'quit', 'adios']:
                    print("\nChatbot: ¡Hasta luego! Que tenga un excelente día.")
                    break

                # Obtener respuesta
                response = self.answer(question)

                print(f"\nChatbot: {response['answer']}")
                print(f"(Fuente: {response['source']})\n")

                # Si se activó transferencia, romper el bucle
                if response['transfer_to_agent']:
                    print("La conversación será transferida a un agente humano.\n")
                    break

            except KeyboardInterrupt:
                print("\n\nChatbot: ¡Hasta luego!")
                break
            except Exception as e:
                print(f"\nError: {str(e)}\n")

    def _is_small_talk(self, question: str) -> bool:
        """Detectar si el mensaje es un saludo o conversación ligera"""
        normalized = question.lower().strip()
        small_talk_phrases = {
            "hola", "hola!", "hola.", "buenas", "buenas!", "buenas tardes",
            "buenas noches", "buenos días", "buenos dias", "hey", "que tal",
            "qué tal", "gracias", "muchas gracias", "ok", "vale", "entendido",
            "perfecto", "hola chatbot", "hola bot", "hola lazarus"
        }
        if normalized in small_talk_phrases:
            return True
        return len(normalized) <= 20 and any(
            normalized.startswith(prefix) for prefix in ["hola", "buen", "grac", "hey", "que tal", "qué tal"]
        )

    def _small_talk_reply(self, question: str) -> str:
        """Generar respuesta amigable para saludos"""
        base_reply = (
            "¡Hola! 😊 Estoy aquí para ayudarte con todo lo relacionado a Grupo Lazarus. "
            "¿En qué puedo asistirte hoy?"
        )
        if "grac" in question.lower():
            return "¡Con gusto! Si necesitas algo más sobre Grupo Lazarus, dime 😊"
        return base_reply


def main():
    """Función principal para ejecutar el chatbot"""
    # Cargar variables de entorno
    dotenv.load_dotenv()

    # Inicializar chatbot
    chatbot = LazarusChatbot()

    # Iniciar sesión de chat
    chatbot.chat()


if __name__ == "__main__":
    main()
