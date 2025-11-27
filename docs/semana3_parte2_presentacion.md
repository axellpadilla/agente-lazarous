🛠️ **Temática Clave — Dependencias, Git y ML Ops**

- **lanchain + VS Code:** Diagnóstico de fallas de instalación y alternativas con entornos administrados por UV.
- **Buenas prácticas Git:** Control de ramas, colaboración en GitHub y estructura de proyectos con carpeta `source`.
- **Pilares ML Ops:** Rastreo de modelos, despliegue/monitoreo y manejo eficiente de datos.
- **Optimización de almacenamiento:** Uso de bases de datos y formatos especializados para grandes volúmenes.

## ✅ Conclusiones y Tareas Inmediatas

- **luis.castillo:** Enviar el enlace de la reunión a todos los participantes, incluido Melvin.
- **luis.sabillon:** Hablar con Carolina para confirmar su asistencia o revisión de la grabación.
- **Axell:** Compartir el repo actualizado con estructura sugerida (carpeta `source`, etc.) y documentación sobre bases de datos locales como DuckDB.
- **Todos los participantes:**
  - Probar la instalación de lanchain usando UV y reportar resultados.
  - Aplicar la estructura recomendada de directorios en sus proyectos.
  - Guardar y monitorear cambios de estado relevantes (quiebres de inventario) en la base de datos.
  - Hacer pull del repositorio MLOps actualizado para evitar conflictos.
- **luis.sabillon y luis.castillo:** Experimentar con Google antigravity y documentar ideas útiles.

## 🧠 Contenido Principal de la Sesión

### Problemas de Instalación de Librerías
Axell y Luis revisaron los fallos de instalación de la librería lanchain en Visual Studio Code, identificando que otras dependencias sí funcionan y que la causa probable es el entorno. Se recomendó usar UV para aislar dependencias sin activar entornos manualmente, lo que facilita reproducir ambientes en cada proyecto.

### Gestión de Dependencias con UV
Se explicó el flujo de trabajo con UV: definición en `pyproject.toml`, instalación automática en la carpeta del proyecto y ejecución sin `activate`. Luis Castillo aprovechó para preguntar sobre ramas en GitHub, y Axell repasó commits atómicos, revert y colaboración segura cuando varias personas editan el mismo repositorio.

### Mejores Prácticas Git y ML Ops
Axell insistió en estructurar el código (carpeta `source`, módulos claros) cuando se integra IA para evitar monolitos difíciles de mantener. También repasó los pilares de ML Ops: rastreo/versionamiento de modelos, despliegue y routing, y monitoreo con métricas que permitan detectar drift de datos.

### Almacenamiento y Manejo de Datos
Ante preguntas sobre grandes volúmenes, Axell recomendó registrar cambios de estado en lugar de snapshots diarios y usar formatos columnar como Parquet o bases especializadas (DuckDB, SQLite, etc.). Destacó que esto reduce costos, mejora tiempos de consulta y simplifica el monitoreo continuo del pipeline.
