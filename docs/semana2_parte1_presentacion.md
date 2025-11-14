🧩 **Temática Clave — Generación de Features y Política de Datos para Sistemas de IA**

- **Feature Engineering aplicado al negocio:** Uso de variables derivadas (fechas, clima, días laborables, estacionalidad) para mejorar el poder predictivo de modelos de ventas e inventario.
- **Gobernanza y calidad de datos en IA:** Revisión del borrador de política general de sistemas de inteligencia artificial, con foco en integridad, consistencia, limpieza y trazabilidad de los datos.
- **Data leakage y buenas prácticas:** Discusión sobre riesgos al mezclar información de entrenamiento y validación, y la importancia de dividir los datos antes de aplicar transformaciones.
- **Gestión de inventario y reglas de negocio:** Análisis de devoluciones, notas de crédito, productos de baja rotación y definición de matrices de mínimos y máximos por tienda.
- **Entorno técnico y repositorio:** Configuración del nuevo repositorio en GitHub, uso de UV como gestor de paquetes y ejecución de notebooks de demostración para feature engineering.

## ✅ Conclusiones y Tareas Inmediatas

- **Política de calidad de datos:** Se revisó el borrador de política de sistemas de IA, incluyendo objetivos, alcance, roles y responsabilidades, así como criterios de calidad (precisión, exactitud, integridad, completitud, consistencia, coherencia).
- **Necesidad de política global:** Se acordó que la política de gobernanza de datos debe escalar a toda la empresa, no solo a sistemas de inteligencia artificial.
- **Reglas de negocio críticas:** Se identificó la urgencia de documentar formalmente criterios para tratamiento de valores negativos, meses sin información, devoluciones, rotación y definición de mínimos/máximos de inventario.
- **Feature engineering práctico:** Se reforzó el valor de variables derivadas de tiempo y contexto (ej. sábados, clima, working day) y de un pipeline correcto (split antes de transformar) para evitar data leakage.
- **Madurez técnica:** El equipo técnico avanzó en la configuración del nuevo repositorio, ejecución de notebooks de ejemplo y comprensión de las limitaciones de modelos locales (Llama) frente a servicios en la nube.

## 🧠 Contenido Principal de la Sesión

### Generación de Features y Riesgos de Engineering

- La agenda se centró en la generación de features, fundamentos y riesgos del feature engineering, junto con un ejemplo práctico de regresión lineal.
- Se discutió cómo variables como día de la semana, clima, estacionalidad y ciclos de demanda pueden mejorar la capacidad predictiva de los modelos.
- Se aclaró que problemas como la optimización de distribución de inventario pueden requerir formulaciones de optimización matemática, más allá de modelos de machine learning estándar.

### Política General de Sistemas de IA y Gestión de Datos

- Se revisó el borrador de la política de sistemas de IA, con énfasis en:
  - Objetivos y alcance.
  - Roles: comité de gobernanza, propietarios de sistemas, custodios de datos y usuarios.
  - Proceso para registrar sistemas de IA y evaluar su calidad de datos.
- Se presentó un sistema de gestión de calidad de datos con:
  - Evaluación y medición.
  - Limpieza y prevención.
  - Monitoreo continuo, evaluación de riesgos y plan de mantenimiento/mejora.
  - Aprobación del sistema y mejora continua.
- Se remarcó la necesidad de una política de gobernanza de datos que cubra todos los procesos de la empresa, y no solo el chatbot o el modelo de predicción.

### Reglas de Negocio: Rotación, Devoluciones e Inventarios

- Se analizó el tratamiento de valores negativos y el manejo de facturas vs. notas de crédito para obtener indicadores de rotación más precisos.
- Se discutió el manejo de devoluciones de productos vencidos (reclamos con descuentos vs. devoluciones que afectan inventario).
- Se resaltó la importancia de:
  - Definir matrices de mínimos y máximos por tienda.
  - Documentar responsables y cadencias de revisión.
  - Establecer criterios claros para productos de baja rotación (cuándo se mantienen o se depuran del inventario).

### Conceptos de Machine Learning y Data Leakage

- Se repasaron conceptos básicos de ML y feature engineering:
  - Creación de variables a partir de fechas y contexto.
  - Evitar usar información del futuro o de validación en el entrenamiento.
- Se explicó el data leakage como el uso indebido de información de entrenamiento en la validación, y la necesidad de:
  - Separar datos en entrenamiento/prueba antes de aplicar transformaciones.
  - Ajustar transformadores (ej. escaladores) solo con datos de entrenamiento.

### Transformadores y Modelos Estadísticos

- Se aclaró el concepto de transformadores/transformadores estadísticos en pipelines clásicos (ej. cálculo de medias, escalamiento estándar) como componentes que ajustan variables durante el entrenamiento.
- Se mencionaron diferentes familias de modelos (árboles de decisión, modelos lineales, modelos basados en pesos) y cómo cada uno puede requerir transformaciones distintas.
- Se recomendó explorar plataformas con estudios públicos y código de competiciones para practicar preprocesamiento y modelado.

### Configuración Técnica del Repositorio

- Se explicó el procedimiento para:
  - Acceder al nuevo repositorio de trabajo.
  - Usar UV como gestor de paquetes.
  - Ejecutar aplicaciones y notebooks de ejemplo.
- Se abordaron problemas comunes con GitHub Codespaces y la gestión de repositorios antiguos.
- Se mostró la estructura modular del repositorio (núcleo/base y capa de interfaz visual), preparando el terreno para futuras modificaciones de código ligadas a variables y datasets.

### Procesamiento de Datos y Variables Derivadas

- Se practicó la extracción de variables a partir de fechas: día de la semana, working day, etc.
- Se discutió el uso de variables de clima u otras fuentes externas como "fichas" para enriquecer el modelo.
- Se demostró el uso de `pandas` y transformadores (ej. escaladores) para:
  - Crear nuevas columnas.
  - Aplicar escalamiento y otras transformaciones, respetando el split entrenamiento/prueba.

### Modelos Locales y Sistema de Asistencia al Cliente

- Se realizó una demostración de un sistema de asistencia al cliente usando un modelo Llama de 0.5B parámetros:
  - Se explicaron sus limitaciones de rendimiento y capacidad frente a modelos de proveedores como OpenAI.
  - Se sugirió hacer benchmarking de herramientas alternativas, evaluando costo/beneficio.
- Se revisó cómo interactuar con el chatbot y cómo los datos limpios y bien gobernados impactan directamente en la calidad de las respuestas.

## 🛠️ Herramientas Utilizadas y Recursos Comentados

| Herramienta / Recurso                        | Descripción                                                                                     | Enlace |
|---------------------------------------------|-------------------------------------------------------------------------------------------------|--------|
| `bike_sharing_demand.csv`                   | Dataset de ejemplo para análisis de demanda y generación de features de tiempo y clima.        | (archivo local en el entorno de trabajo) |
| Chatwoot                                    | Plataforma de atención al cliente y bandeja unificada para gestionar conversaciones.           | https://www.chatwoot.com/ |
| Repositorio agente Lazarus (actual)         | Repositorio principal del proyecto de chatbot y sesiones técnicas.                             | https://github.com/axellpadilla/agente-lazarus |
| Agentic Customer Support System             | Ejemplo de sistema de soporte al cliente usando agentes y modelos de lenguaje.                 | https://github.com/axellpadilla/agentic-customer-support-system |
| Demo Features & Leakage                     | Repositorio de demostración para feature engineering y ejemplos de data leakage.               | https://github.com/axellpadilla/demo-features-leakaje |
| Kaggle                                      | Plataforma con datasets públicos, competiciones y notebooks para practicar ML y feature engineering. | https://www.kaggle.com/ |
| Read.ai                                     | Herramienta para gestión de reuniones y grabaciones (incluyendo notas y transcripciones).      | https://www.read.ai/pp |

## 📌 Próximos Pasos

- **Equipo:** Presentar y finalizar el borrador de la política de calidad de datos.
- **Equipo:** Reestructurar la política de calidad de datos como una política global generalizadas para todos los procesos de la empresa, no solo para sistemas de IA.
- **Equipo:** Documentar formalmente los lineamientos sobre actualización de la memoria y criterios de contenido apto para la base de conocimientos.
- **Equipo:** Definir el método de indexación de información de productos.
- **Equipo:** Crear y mantener una tabla/matriz con puntos mínimos y máximos de inventario por tienda, incluyendo justificación, responsable y período de validez.
- **Equipo:** Definir y documentar reglas de tratamiento de valores negativos, meses sin información y otras reglas de negocio antes de programar el modelo de predicción de ventas.
- **Equipo:** Continuar depurando y documentando las reglas de cómputo de rotación y ventas que ya han venido trabajando.
- **Equipo técnico:** Practicar con el repositorio compartido en GitHub y ejecutar el notebook de demostración de feature engineering.

## 📎 Anexo — Matriz de inventario (ejemplo)

| id            | punto_minimo | maximo | seguridad | fecha_desde | fecha_hasta | responsable | notas                                                              |
|---------------|--------------|--------|-----------|-------------|-------------|-------------|--------------------------------------------------------------------|
| tienda-001    | 50           | 150    | 30        | 2025-11-01  | 2026-04-30  | equipo inventario | Cobertura pretemporada; seguridad mayor en productos frescos.     |
| tienda-002    | 20           | 80     | 15        | 2025-11-01  | 2026-01-15  | equipo inventario | Producto lento, seguridad baja para minimizar espacio de almacenaje. |
| tienda-003    | 100          | 220    | 25        | 2025-11-01  | 2026-03-31  | equipo tiendas     | Punto mínimo alto por alta demanda estacional; revisar cada semana. |

### Campos y ejemplos de uso

- `id`: Identificador único de la combinación tienda/producto o categoría. Ejemplo: `tienda-001` corresponde a la tienda principal en Ciudad X.
- `punto_minimo`: Cantidad mínima aceptada antes de disparar reabastecimiento. Se fija según lead time y demanda promedio.
- `maximo`: Límite superior que evita exceso de inventario y productos obsoletos.
- `seguridad`: Stock adicional reservado para cubrir variaciones inesperadas o demoras logísticas.
- `fecha_desde` / `fecha_hasta`: Vigencia del rango definido; permite cadencias diferentes por temporada.
- `responsable`: Equipo o persona encargada de validar y ajustar valores (ej. `equipo inventario`).
- `notas`: Contexto adicional, reglas especiales o vínculos a políticas (por ejemplo, mantener mayor seguridad para productos perecederos o incorporar devoluciones).

Estos campos permiten establecer una matriz operativa clara: al revisar inventario, se compara con `punto_minimo`/`maximo` vigente, se activa `seguridad` cuando la demanda supera el promedio y se documentan decisiones en `notas` para auditoría.
