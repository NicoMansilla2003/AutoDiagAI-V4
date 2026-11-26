# 🚗 AutoDiag AI V4

AutoDiag AI V4 es un asistente experimental de diagnóstico automotriz desarrollado en Python que combina una arquitectura multiagente, recuperación de conocimiento mediante RAG y reglas deterministas de seguridad.

El sistema recibe los síntomas descritos por el usuario, consulta una base técnica automotriz y coordina diferentes agentes especializados para generar una evaluación estructurada con posibles causas, nivel de riesgo, recomendaciones y consideraciones de seguridad.

> **AutoDiag AI no reemplaza un diagnóstico mecánico profesional.**  
> La información entregada por el sistema es orientativa y debe utilizarse como apoyo inicial.

---

## ✨ Características principales

- 🤖 Arquitectura multiagente utilizando **CrewAI**
- 🧠 Modelo de lenguaje ejecutado mediante **Groq**
- 📚 Sistema **RAG** con conocimiento técnico automotriz
- 🔎 Embeddings mediante **Hugging Face**
- 🗃️ Base vectorial persistente con **ChromaDB**
- 🖥️ Interfaz web desarrollada con **Streamlit**
- 💾 Historial de diagnósticos mediante **SQLite**
- 📧 Envío de informes mediante **Gmail API + OAuth 2.0**
- 🔧 Módulo de mantenimiento preventivo
- 📖 Consulta directa de conocimiento técnico
- 🔒 Filtro de dominio automotriz
- 🛡️ Reglas deterministas para situaciones potencialmente críticas
- 📋 Resultados estructurados y validados con **Pydantic**
- 🇪🇸 Interfaz orientada al español

---

# 🧠 Arquitectura

AutoDiag AI V4 combina reglas deterministas, recuperación de información y agentes de inteligencia artificial.

```text
Usuario
   │
   ▼
┌─────────────────────────────┐
│ Guardrail de dominio        │
│                             │
│ Verifica que la consulta    │
│ pertenezca al ámbito        │
│ automotriz                  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Safety Guard                │
│                             │
│ Detecta señales críticas    │
│ mediante reglas locales     │
└──────────────┬──────────────┘
               │
               ▼
┌───────────────────────────────────────────────────────┐
│                    CrewAI                             │
│                                                       │
│  🔧 Especialista mecánico                            │
│  📚 Investigador técnico                             │
│  🛡️ Revisor de seguridad                            │
│  🧠 Sintetizador diagnóstico                         │
└──────────────┬────────────────────────────────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Resultado JSON estructurado │
│ + validación Pydantic       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│ Safety Guard final          │
│                             │
│ Impide reducir determinadas │
│ alertas críticas            │
└──────────────┬──────────────┘
               │
               ▼
        Diagnóstico final
```

---

# 🤖 Agentes de inteligencia artificial

AutoDiag AI utiliza cuatro agentes especializados.

## 🔧 Especialista mecánico

Analiza los síntomas descritos por el usuario y consulta la base estructurada de diagnóstico.

Puede utilizar información relacionada con:

- frenos;
- motor;
- batería;
- sistema eléctrico;
- refrigeración;
- transmisión;
- embrague;
- suspensión;
- dirección;
- neumáticos;
- escape;
- turbo;
- sensores;
- climatización.

---

## 📚 Investigador técnico

Consulta la base de conocimiento mediante RAG.

Su función es recuperar documentación relacionada con los síntomas para proporcionar evidencia técnica adicional al diagnóstico.

---

## 🛡️ Revisor de seguridad

Evalúa el diagnóstico desde el punto de vista de seguridad.

Determina aspectos como:

- riesgo potencial;
- posibilidad de continuar conduciendo;
- necesidad de una revisión profesional.

---

## 🧠 Sintetizador diagnóstico

Recibe la información obtenida por los agentes anteriores y genera el resultado final estructurado.

La respuesta debe cumplir un esquema definido mediante Pydantic.

---

# 📋 Estructura del diagnóstico

El resultado final contiene campos similares a los siguientes:

```json
{
  "evaluacion_general": "...",
  "sistema_relacionado": "...",
  "nivel_riesgo": "medio",
  "causas_posibles": [
    "..."
  ],
  "evidencia_tecnica": "...",
  "fuente_tecnica": "...",
  "evaluacion_seguridad": "...",
  "seguridad_conduccion": "precaucion",
  "requiere_revision_profesional": true,
  "recomendaciones": [
    "..."
  ],
  "advertencia": "..."
}
```

Los niveles de riesgo admitidos son:

```text
bajo
medio
alto
```

La seguridad de conducción utiliza:

```text
seguro
precaucion
no_recomendado
```

---

# 📚 Sistema RAG

AutoDiag AI incluye una base de conocimiento automotriz que puede consultarse semánticamente.

El sistema utiliza:

```text
Documentos técnicos
       ↓
RecursiveCharacterTextSplitter
       ↓
HuggingFace Embeddings
       ↓
ChromaDB
       ↓
Similarity Search
       ↓
Fragmentos relevantes
```

## Modelo de embeddings

```text
sentence-transformers/all-MiniLM-L6-v2
```

## Configuración de fragmentación

```text
chunk_size = 500
chunk_overlap = 100
```

La base vectorial se almacena localmente en:

```text
rag/chroma_db/
```

Esta carpeta se genera automáticamente y no debe versionarse en Git.

---

# 🔄 Versionado del conocimiento

La base técnica dispone de un sistema de versionado.

Ejemplo:

```python
BASE_CONOCIMIENTO_VERSION = "2.0.0"
```

Cuando cambia esta versión, AutoDiag puede detectar que la base vectorial existente pertenece a una versión anterior y reconstruir automáticamente ChromaDB.

Esto permite modificar la documentación técnica sin tener que eliminar manualmente la base vectorial.

---

# 🔒 Guardrail de dominio

AutoDiag AI está diseñado exclusivamente para consultas relacionadas con vehículos.

Antes de iniciar los agentes, el sistema analiza localmente la consulta.

Consultas válidas:

```text
El volante vibra cuando voy a 100 km/h.

El motor pierde potencia al acelerar.

La batería se descarga durante la noche.

Siento un golpe cuando paso por baches.
```

Consultas fuera del dominio:

```text
¿Cómo preparo una pizza?

¿Quién ganó el mundial?

Ayúdame con un ejercicio de matemáticas.
```

Las consultas fuera del ámbito automotriz se rechazan antes de iniciar los agentes, evitando llamadas innecesarias al modelo de lenguaje.

---

# 🛡️ Safety Guard

AutoDiag AI posee una segunda capa de protección independiente del modelo de inteligencia artificial.

El sistema busca determinadas descripciones potencialmente críticas, por ejemplo:

- pérdida importante de capacidad de frenado;
- pedal de freno que se va al fondo;
- presión de aceite crítica;
- sobrecalentamiento severo;
- pérdida del control de dirección;
- fuga de combustible;
- humo o gases dentro del habitáculo;
- problemas críticos de rueda o neumático.

Cuando se detecta una condición crítica, el sistema puede establecer como mínimo:

```text
Nivel de riesgo: ALTO
Conducción: NO RECOMENDADO
Revisión profesional: SÍ
```

Estas reglas se aplican mediante código local y no dependen únicamente de la decisión del LLM.

---

# 🔧 Mantenimiento

AutoDiag dispone de un módulo independiente de mantenimiento preventivo.

Incluye categorías como:

- sistema de frenos;
- batería;
- sistema eléctrico;
- motor;
- refrigeración;
- transmisión;
- suspensión;
- dirección;
- neumáticos;
- escape;
- turbo;
- electrónica;
- climatización.

Las recomendaciones son generales.

Los intervalos específicos deben consultarse siempre en la documentación oficial del fabricante correspondiente al vehículo.

---

# 📖 Conocimiento técnico

La aplicación permite consultar directamente la base RAG sin ejecutar los cuatro agentes.

Ejemplo:

```text
¿Qué puede provocar tirones y pérdida de potencia?
```

El sistema recupera documentos relacionados desde ChromaDB.

Esta función:

- utiliza embeddings semánticos;
- no ejecuta CrewAI;
- no consume llamadas de Groq;
- muestra la categoría y fuente del documento;
- no interpreta la similitud vectorial como porcentaje de certeza.

---

# 💾 Historial de diagnósticos

Los informes pueden guardarse localmente mediante SQLite.

La base se genera en:

```text
data/autodiag_history.db
```

Se almacenan datos como:

- fecha;
- marca;
- modelo;
- año;
- motor;
- kilometraje;
- consulta;
- sistema relacionado;
- nivel de riesgo;
- resultado completo en JSON.

La base SQLite generada no debe subirse al repositorio.

---

# 📧 Informes mediante Gmail

AutoDiag AI puede enviar el diagnóstico generado mediante Gmail API.

La autenticación utiliza OAuth 2.0.

El proyecto requiere:

```text
secrets/gmail_credentials.json
```

Después de autorizar la aplicación se genera:

```text
secrets/gmail_token.json
```

Ambos archivos contienen información privada y están excluidos del repositorio mediante `.gitignore`.

El destinatario permitido se configura mediante:

```env
AUTODIAG_EMAIL=correo@ejemplo.com
```

Antes de enviar el informe, la interfaz solicita confirmación.

---

# 🖥️ Interfaz

La interfaz está desarrollada utilizando Streamlit.

Los módulos principales son:

```text
🚗 Nuevo diagnóstico
🕘 Historial de diagnósticos
🔧 Mantenimiento
📚 Conocimiento técnico
⚙️ Configuración
```

El diseño utiliza una estética oscura inspirada en instrumentación automotriz.

---

# 📁 Estructura del proyecto

```text
AutoDiagAI-V3/
│
├── app.py
├── agents.py
├── tasks.py
├── crew.py
├── models.py
├── llm_config.py
│
├── services/
│   ├── __init__.py
│   ├── domain_guard.py
│   ├── safety_guard.py
│   ├── history.py
│   └── email_service.py
│
├── tools/
│   ├── __init__.py
│   ├── diagnosis.py
│   ├── maintenance.py
│   └── knowledge_search.py
│
├── rag/
│   ├── __init__.py
│   ├── vectorstore.py
│   ├── legacy_rag_v2.py
│   └── chroma_db/
│
├── knowledge/
│   ├── __init__.py
│   └── base_tecnica.py
│
├── ui/
│   ├── __init__.py
│   └── styles.py
│
├── data/
│   └── autodiag_history.db
│
├── secrets/
│   ├── gmail_credentials.json
│   └── gmail_token.json
│
├── tests/
│
├── .env
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

> Las carpetas `chroma_db`, `data` y `secrets` contienen archivos generados o privados y no deben versionarse.

---

# ⚙️ Requisitos

- Python 3.12
- `uv`
- Cuenta de Groq con API Key
- Credenciales OAuth de Google únicamente si se desea utilizar Gmail

La versión utilizada durante el desarrollo es:

```text
Python 3.12
```

---

# 📦 Instalación

Clona el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
```

Entra al proyecto:

```bash
cd AutoDiagAI-V3
```

Instala las dependencias utilizando `uv`:

```bash
uv sync
```

---

# 🔑 Variables de entorno

Crea un archivo:

```text
.env
```

Ejemplo:

```env
GROQ_API_KEY=tu_api_key_de_groq
AUTODIAG_EMAIL=tu_correo@gmail.com
```

Nunca subas este archivo a GitHub.

---

# 📧 Configuración opcional de Gmail

Para utilizar el envío de informes:

1. Crea un proyecto en Google Cloud.
2. Habilita Gmail API.
3. Configura una aplicación OAuth para escritorio.
4. Descarga las credenciales.
5. Guarda el archivo como:

```text
secrets/gmail_credentials.json
```

En la primera autenticación se abrirá el navegador para autorizar el acceso.

AutoDiag utiliza únicamente el permiso:

```text
https://www.googleapis.com/auth/gmail.send
```

Después se generará automáticamente:

```text
secrets/gmail_token.json
```

---

# ▶️ Ejecutar AutoDiag AI

Desde la raíz del proyecto:

```bash
uv run streamlit run app.py
```

Streamlit iniciará la aplicación web local.

---

# 🧪 Ejemplo de diagnóstico

Entrada:

```text
Cuando freno siento una vibración fuerte y el volante tiembla.
```

Flujo aproximado:

```text
Consulta
   ↓
Validación de dominio
   ↓
Safety Guard
   ↓
Especialista mecánico
   ├── Base estructurada
   └── Mantenimiento
   ↓
Investigador técnico
   └── RAG / ChromaDB
   ↓
Revisor de seguridad
   ↓
Sintetizador
   ↓
Validación Pydantic
   ↓
Safety Guard final
   ↓
Informe
```

El sistema podría identificar el sistema de frenos como área relacionada y entregar posibles elementos a inspeccionar, manteniendo siempre el resultado como una orientación inicial.

---

# 🧰 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Interfaz web |
| CrewAI | Orquestación multiagente |
| Groq | Inferencia del modelo |
| GPT-OSS 120B | Modelo de lenguaje |
| LangChain | Componentes RAG |
| Hugging Face | Embeddings |
| ChromaDB | Base vectorial |
| Pydantic | Validación estructurada |
| SQLite | Historial local |
| Gmail API | Envío de informes |
| OAuth 2.0 | Autenticación con Google |
| uv | Gestión de proyecto y dependencias |

---

# 🔐 Archivos que no deben versionarse

El `.gitignore` debe proteger al menos:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/

.env

.vscode/
.idea/

.streamlit/secrets.toml

chroma_db/
.chroma/
rag/chroma_db/

data/*.db
data/*.sqlite
data/*.sqlite3

secrets/

gmail_credentials.json
gmail_token.json
```

Nunca deben publicarse:

- claves de Groq;
- tokens OAuth;
- credenciales de Google;
- archivos `.env`;
- bases SQLite con información de uso;
- tokens de Gmail.

---

# ⚠️ Limitaciones

AutoDiag AI se encuentra en desarrollo y posee limitaciones importantes.

El sistema:

- no inspecciona físicamente el vehículo;
- no realiza mediciones mecánicas reales;
- no reemplaza un scanner profesional;
- no reemplaza un técnico automotriz;
- puede interpretar incorrectamente síntomas ambiguos;
- depende de la calidad de la información proporcionada;
- utiliza una base técnica limitada;
- puede producir respuestas incorrectas generadas por IA;
- no dispone necesariamente de información específica para cada fabricante y motorización.

Las posibles causas deben interpretarse como hipótesis de orientación inicial.

---

# 🛡️ Aviso de seguridad

Si un vehículo presenta una condición que pueda comprometer:

- frenos;
- dirección;
- neumáticos;
- combustible;
- lubricación;
- temperatura del motor;
- visibilidad;
- estabilidad;
- seguridad de los ocupantes;

debe priorizarse la seguridad y solicitar una evaluación profesional.

No debe utilizarse AutoDiag AI como única fuente para determinar que un vehículo es seguro para circular.

---

# 🗺️ Roadmap

Posibles mejoras futuras:

- ampliar la base técnica RAG;
- incorporar documentación específica por fabricante;
- integrar códigos OBD-II;
- mejorar búsqueda y filtros del historial;
- exportar informes a PDF;
- gestionar perfiles de vehículos;
- incorporar mantenimiento por kilometraje;
- ampliar cobertura de síntomas;
- mejorar evaluación de contexto;
- incorporar fuentes técnicas externas verificadas;
- añadir soporte opcional para talleres;
- desarrollar pruebas automatizadas;
- mejorar observabilidad y registro de agentes.

---

# 📌 Estado del proyecto

AutoDiag AI V4 actualmente incluye:

```text
✅ Arquitectura multiagente
✅ Diagnóstico estructurado
✅ RAG con ChromaDB
✅ Embeddings locales
✅ Historial SQLite
✅ Gmail OAuth
✅ Informes por correo
✅ Mantenimiento
✅ Consulta de conocimiento
✅ Guardrail de dominio
✅ Safety Guard
✅ Interfaz Streamlit en español
```

---

# 👨‍💻 Desarrollo

Proyecto desarrollado como una aplicación educativa y experimental para explorar:

- inteligencia artificial aplicada al ámbito automotriz;
- sistemas multiagente;
- RAG;
- bases vectoriales;
- modelos de lenguaje;
- validación estructurada;
- desarrollo de interfaces con Streamlit.

---

## AutoDiag AI V4

**Diagnóstico asistido por inteligencia artificial, recuperación de conocimiento y reglas deterministas de seguridad.**

🚗 🔧 🧠

---

## Autenticación V4

V4 agrega cuentas públicas con correo y contraseña, hash Argon2id, cierre de sesión,
sesiones revocables con vencimiento, limitación de intentos y roles `user`/`admin`.
El registro público siempre crea el rol `user`.

### Gestión de cuentas

Al iniciar sesión como administrador aparece **Gestión de usuarios** en el menú.
La vista muestra nombre, correo, rol, estado, fecha de creación y cantidad de
diagnósticos. El administrador puede activar o desactivar cuentas; al desactivarlas
se revocan todas sus sesiones activas. La vista no permite promover usuarios a
administrador ni desactivar al último administrador activo. La autorización se
comprueba también en el servicio, no solo en la interfaz.

### Primer administrador

Después de instalar las dependencias, crea el primer administrador desde una terminal
local. La contraseña se solicita de forma oculta y no debe pasarse como argumento:

```powershell
uv run python -m services.auth_service bootstrap-admin --email admin@ejemplo.cl
```

El comando solo permite crear un administrador activo inicial. No publiques la salida
de la terminal ni copies credenciales al repositorio.

### Historial existente

La migración agrega una columna de propietario nullable sin borrar diagnósticos. Los
registros anteriores quedan sin propietario y solo son visibles para un administrador.
Los nuevos informes se asocian a la cuenta autenticada; el servicio verifica la sesión
en cada guardado, listado y apertura.

### Despliegue y límites

Esta aplicación combina Streamlit y SQLite y **no se presenta como segura para un
servicio público multiusuario de producción**. Antes de exponerla, hace falta HTTPS
terminado en un proxy confiable, protección de cookies y cabeceras, secretos en un
gestor de secretos del despliegue, monitoreo, copias de seguridad y un procedimiento
de recuperación. SQLite requiere un único proceso/escritor y almacenamiento persistente;
para varias instancias o alto tráfico se debe migrar a una base de datos servidor y
revisar el modelo de sesión. No uses `.env`, tokens, secretos ni bases con datos personales
en commits o imágenes de despliegue.

### Refuerzos incorporados para la evaluación

- CrewAI limita las iteraciones (`max_iter=5`, y `3` en síntesis), acota cada agente
  a 120 segundos y registra cuando se alcanza el techo de iteraciones.
- El inicio de sesión ya limita intentos fallidos. Además, los diagnósticos se limitan
  por cuenta (5 por minuto por defecto) y a 4000 caracteres por consulta. Se pueden
  ajustar con `AUTODIAG_REQUESTS_PER_MINUTE` y `AUTODIAG_MAX_INPUT_CHARS`.
- Las entradas del usuario se escapan y se enmarcan como datos no confiables en cada
  tarea. Esto reduce la confusión de instrucciones, pero no garantiza eliminar toda
  inyección de prompt.
- Las llamadas al modelo tienen timeout de 60 segundos, un reintento máximo y topes
  de salida. Los eventos de inicio, error y duración se registran como JSON con
  `trace_id`; no se deben registrar prompts, contraseñas ni tokens.
- El proyecto usa CrewAI para la orquestación y LangChain para RAG; no depende de
  LangGraph. No hay una conversación reanudable que requiera checkpointing en este
  flujo de diagnóstico de una sola ejecución. Si luego se adopta LangGraph, se debe
  diseñar persistencia aislada por usuario antes de habilitarla.

### Contenedor y HTTPS para una demostración

El `Dockerfile` fija Python 3.12, instala desde `uv.lock`, ejecuta como usuario no root
y consulta el endpoint de salud de Streamlit. `compose.yaml` añade Caddy, que sirve
HTTPS automático al dominio indicado y añade HSTS, CSP y otras cabeceras. Antes de
arrancarlo en AWS, se requiere un dominio con DNS apuntando a la IP pública, reglas
de entrada TCP 80/443 en el grupo de seguridad y una instancia activa. Streamlit solo
queda accesible dentro de la red privada de Docker.

En el equipo o instancia, crea `.env` copiando `.env.example`, reemplaza la clave
Groq por una real y define `AUTODIAG_DOMAIN`. No guardes `.env` en Git. Luego ejecuta:

```powershell
docker compose up -d --build
docker compose ps
```

Comprueba `https://tu-dominio/` y `docker compose logs app proxy`. Si cambias la CSP y
la interfaz deja de cargar, inspecciona la consola del navegador y ajusta la política
con pruebas; no elimines HTTPS ni HSTS como solución. Caddy necesita salida a Internet
para obtener y renovar el certificado. El volumen de Chroma, SQLite y caché del modelo
persiste entre reinicios; respáldalo y protégelo como dato privado. En AWS Academy,
detén o elimina los recursos facturables cuando termine la práctica.

Este Compose es una base reproducible para una demostración de curso, no una garantía
de seguridad de producción. La CSP es una política inicial y requiere validación con
la interfaz Streamlit. La URL pública, DNS, reglas de red y certificado no se pueden
confirmar desde el repositorio: deben comprobarse en el entorno AWS activo.
