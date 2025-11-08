"""
Módulo de Base de Conocimiento RAG (RAG para Generación Aumentada por Recuperación)
Maneja la carga y búsqueda de datos de FAQ desde archivo CSV
"""

import pandas as pd
from typing import List, Dict, Optional
import os


class FAQKnowledgeBase:
    """Gestiona la base de conocimiento de FAQ desde archivo CSV"""

    # Puntuación común en español para eliminar de las palabras
    PUNCTUATION = '¿?.,;:'

    def __init__(self, excel_file: str = "data_limpia/faq_limpio.csv"):
        """
        Inicializar la base de conocimiento

        Args:
            excel_file: Ruta al archivo CSV que contiene los datos de FAQ
        """
        self.excel_file = excel_file
        self.faqs: List[Dict[str, str]] = []
        self.load_data()

    def load_data(self) -> None:
        """Cargar datos de FAQ desde archivo CSV"""
        if not os.path.exists(self.excel_file):
            raise FileNotFoundError(
                f"Archivo CSV no encontrado: {self.excel_file}")

        try:
            df = pd.read_csv(self.excel_file)

            # Convertir DataFrame a lista de diccionarios
            for _, row in df.iterrows():
                self.faqs.append({
                    'pregunta': str(row['pregunta']),
                    'respuesta': str(row['respuesta']),
                    'categoria': str(row.get('categoria', 'General'))
                })

            print(f"✓ Cargadas {len(self.faqs)} FAQs desde {self.excel_file}")
        except Exception as e:
            raise Exception(f"Error al cargar archivo CSV: {str(e)}")

    def search(self, query: str, threshold: float = 0.2) -> Optional[Dict[str, str]]:
        """
        Búsqueda mejorada basada en palabras clave en la base de datos de FAQ

        Args:
            query: Pregunta del usuario
            threshold: Umbral mínimo de similitud

        Returns:
            Mejor FAQ coincidente o None si no se encuentra ninguna
        """
        query_lower = query.lower()
        best_match = None
        best_score = 0

        # Eliminar palabras vacías comunes y puntuación
        stopwords = {'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 'del', 'al',
                     'es', 'un', 'una', 'con', 'por', 'para', 'su', 'sus', 'que', '¿', '?',
                     'están', 'estan', 'como', 'cual', 'cuales'}

        # Mapeos de palabras para mejor coincidencia
        word_mappings = {
            'donde': 'ubicad',
            'ubicacion': 'ubicad',
            'oficina': 'ubicad',
            'direccion': 'ubicad',
        }

        # Limpiar consulta
        query_words = [w.strip(self.PUNCTUATION) for w in query_lower.split()
                       if w.strip(self.PUNCTUATION) not in stopwords]
        # Aplicar mapeos
        query_words = [word_mappings.get(w, w) for w in query_words]

        for faq in self.faqs:
            pregunta_lower = faq['pregunta'].lower()
            respuesta_lower = faq['respuesta'].lower()
            categoria_lower = faq['categoria'].lower()

            # Limpiar pregunta de FAQ
            pregunta_words = [w.strip(self.PUNCTUATION) for w in pregunta_lower.split()
                              if w.strip(self.PUNCTUATION) not in stopwords]

            score = 0

            # Verificar coincidencias de subcadenas (más flexible)
            for query_word in query_words:
                # Verificar en pregunta
                for pregunta_word in pregunta_words:
                    if query_word in pregunta_word or pregunta_word in query_word:
                        score += 0.4
                    if query_word == pregunta_word:
                        score += 0.2

                # Verificar en categoría
                if query_word in categoria_lower:
                    score += 0.3

                # Verificar en respuesta (menos peso)
                if query_word in respuesta_lower:
                    score += 0.1

            # Normalizar puntuación
            if len(query_words) > 0:
                score = score / len(query_words)

                # Bonificación por coincidencia exacta de frase
                if query_lower in pregunta_lower or query_lower in respuesta_lower:
                    score += 0.5

                if score > best_score and score > threshold:
                    best_score = score
                    best_match = faq

        return best_match

    def get_all_faqs(self) -> List[Dict[str, str]]:
        """Devolver todas las FAQ"""
        return self.faqs

    def get_faqs_by_category(self, category: str) -> List[Dict[str, str]]:
        """Obtener FAQ filtradas por categoría"""
        return [faq for faq in self.faqs if faq['categoria'].lower() == category.lower()]
