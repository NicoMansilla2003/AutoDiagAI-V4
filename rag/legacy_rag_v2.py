from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools import tool


# ==========================================
# 1. BASE DE CONOCIMIENTO
# ==========================================

documentos = [
    Document(
        page_content="""
        Sistema de frenos:

        Una vibración durante el frenado puede estar relacionada con
        desgaste de componentes, deformación de discos o problemas
        en otros elementos del sistema de frenos.

        Entre los elementos que pueden inspeccionarse se encuentran
        las pastillas, los discos, el líquido de frenos y el sistema
        hidráulico.

        Si existen síntomas que puedan comprometer la capacidad de
        frenado, el vehículo debe ser evaluado por un profesional.
        """,
        metadata={
            "categoria": "frenos",
            "fuente": "base_tecnica_autodiag"
        }
    ),

    Document(
        page_content="""
        Batería:

        Una batería deteriorada o descargada puede producir dificultad
        para arrancar, luces débiles y diferentes fallas eléctricas.

        Se recomienda revisar el estado de la batería, sus terminales,
        conexiones y el sistema de carga del vehículo.

        Una batería descargada no necesariamente significa que la
        batería esté defectuosa, ya que también puede existir un
        problema en el sistema de carga.
        """,
        metadata={
            "categoria": "bateria",
            "fuente": "base_tecnica_autodiag"
        }
    ),

    Document(
        page_content="""
        Motor:

        Los tirones, pérdida de potencia, ralentí inestable o dificultad
        para arrancar pueden estar relacionados con diferentes sistemas.

        Entre las posibles áreas de revisión se encuentran las bujías,
        el sistema de inyección y el sistema de encendido.

        Si la falla persiste, puede ser necesario realizar un diagnóstico
        electrónico para identificar la causa.
        """,
        metadata={
            "categoria": "motor",
            "fuente": "base_tecnica_autodiag"
        }
    ),

    Document(
        page_content="""
        Mantenimiento preventivo:

        El mantenimiento preventivo permite detectar problemas antes de
        que se conviertan en fallas mayores.

        Las revisiones deben realizarse de acuerdo con las indicaciones
        del fabricante y considerando el uso del vehículo.

        Las recomendaciones entregadas por AutoDiag AI son orientativas
        y no sustituyen el mantenimiento realizado por un profesional.
        """,
        metadata={
            "categoria": "mantenimiento",
            "fuente": "base_tecnica_autodiag"
        }
    )
]


# ==========================================
# 2. TEXT CHUNKING
# ==========================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documentos)


# ==========================================
# 3. EMBEDDINGS
# ==========================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# ==========================================
# 4. BASE VECTORIAL CHROMA
# ==========================================

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="autodiag_conocimiento"
)


# ==========================================
# 5. HERRAMIENTA RAG
# ==========================================

@tool
def buscar_conocimiento_tecnico(consulta: str) -> str:
    """
    Busca información técnica relevante en la base de conocimiento
    mediante búsqueda semántica.

    Utilizar cuando el usuario solicite información técnica,
    mantenimiento, posibles causas o recomendaciones que puedan
    encontrarse en la documentación disponible.
    """

    documentos_relevantes = vectorstore.similarity_search(
        consulta,
        k=2
    )

    if not documentos_relevantes:
        return (
            "No se encontró información relevante en la base "
            "de conocimiento."
        )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos_relevantes
    )

    return (
        "Información técnica recuperada:\n\n"
        + contexto
    )