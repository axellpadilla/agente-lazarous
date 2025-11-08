"""
Ejemplo de uso del Chatbot Lazarus
Demuestra varias características incluyendo RAG y transferencia de agente
"""

from chatbot import LazarusChatbot
from dotenv import load_dotenv
import os


def example_basic_usage():
    """Ejemplo 1: Uso básico del chatbot"""
    print("\n" + "="*60)
    print("EJEMPLO 1: Uso Básico del Chatbot")
    print("="*60 + "\n")

    # Crear instancia del chatbot
    chatbot = LazarusChatbot()

    # Preguntas de prueba
    test_questions = [
        "¿Cuál es el horario de atención?",
        "¿Dónde están ubicadas las oficinas?",
        "¿Qué servicios ofrecen?",
    ]

    for question in test_questions:
        print(f"Pregunta: {question}")
        response = chatbot.answer(question)
        print(f"Respuesta: {response['answer']}")
        print(f"Fuente: {response['source']}")
        print("-" * 60 + "\n")


def example_transfer_scenario():
    """Ejemplo 2: Escenario que activa transferencia a agente"""
    print("\n" + "="*60)
    print("EJEMPLO 2: Escenario de Transferencia a Agente")
    print("="*60 + "\n")

    chatbot = LazarusChatbot()

    # Pregunta no en base de conocimiento
    unknown_question = "¿Puedo personalizar el color del producto?"

    print(f"Pregunta: {unknown_question}")
    response = chatbot.answer(unknown_question)
    print(f"Respuesta: {response['answer']}")
    print(f"Transferir a agente: {response['transfer_to_agent']}")
    if response['transfer_to_agent']:
        print(f"Razón: {response['transfer_reason']}")
    print("-" * 60 + "\n")


def example_custom_model():
    """Ejemplo 3: Uso con modelo personalizado"""
    print("\n" + "="*60)
    print("EJEMPLO 3: Uso con Modelo Personalizado")
    print("="*60 + "\n")

    api_key = os.getenv("OPENROUTER_API_KEY")

    if api_key and api_key != "your_api_key_here":
        # Use GPT-4 for better responses
        chatbot = LazarusChatbot(
            api_key=api_key,
            model="openai/gpt-4"
        )

        question = "¿Tienen garantía?"
        print(f"Pregunta: {question}")
        response = chatbot.answer(question)
        print(f"Respuesta: {response['answer']}")
        print(f"Fuente: {response['source']}")
    else:
        print("⚠ API key no configurada. Configure OPENROUTER_API_KEY en .env")

    print("-" * 60 + "\n")


def example_knowledge_base_inspection():
    """Ejemplo 4: Inspección de la base de conocimientos"""
    print("\n" + "="*60)
    print("EJEMPLO 4: Inspección de la Base de Conocimientos")
    print("="*60 + "\n")

    from rag_knowledge_base import FAQKnowledgeBase

    kb = FAQKnowledgeBase()

    print(f"Total de FAQs cargadas: {len(kb.get_all_faqs())}")
    print("\nCategorías disponibles:")
    categories = set(faq['categoria'] for faq in kb.get_all_faqs())
    for cat in sorted(categories):
        count = len(kb.get_faqs_by_category(cat))
        print(f"  - {cat}: {count} preguntas")

    print("\nEjemplo de FAQ:")
    if kb.get_all_faqs():
        faq = kb.get_all_faqs()[0]
        print(f"  Pregunta: {faq['pregunta']}")
        print(f"  Respuesta: {faq['respuesta'][:100]}...")
        print(f"  Categoría: {faq['categoria']}")

    print("-" * 60 + "\n")


def main():
    """Ejecutar todos los ejemplos"""
    # Cargar variables de entorno
    load_dotenv()

    print("\n")
    print("*" * 60)
    print("  EJEMPLOS DE USO - Chatbot Grupo Lazarus")
    print("*" * 60)

    # Ejecutar ejemplos
    example_knowledge_base_inspection()
    example_basic_usage()
    example_transfer_scenario()
    example_custom_model()

    print("\n" + "="*60)
    print("Para iniciar el chatbot interactivo, ejecute:")
    print("  python chatbot.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
