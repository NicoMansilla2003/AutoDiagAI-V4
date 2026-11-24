import shutil

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge.base_tecnica import (
    DOCUMENTOS,
    BASE_CONOCIMIENTO_VERSION
)


# =========================================================
# CONFIGURACIÓN
# =========================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
)


DIRECTORIO_CHROMA = (
    BASE_DIR
    / "chroma_db"
)


ARCHIVO_VERSION = (
    DIRECTORIO_CHROMA
    / "knowledge_version.txt"
)


MODELO_EMBEDDINGS = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


NOMBRE_COLECCION = (
    "autodiag_conocimiento"
)


CHUNK_SIZE = 500

CHUNK_OVERLAP = 100


# =========================================================
# VARIABLES INTERNAS
# =========================================================

_embeddings = None

_vectorstore = None


# =========================================================
# EMBEDDINGS
# =========================================================

def obtener_embeddings():
    """
    Carga el modelo de embeddings una sola vez.
    """

    global _embeddings


    if _embeddings is None:

        _embeddings = (
            HuggingFaceEmbeddings(

                model_name=(
                    MODELO_EMBEDDINGS
                ),

                model_kwargs={
                    "device": "cpu"
                },

                encode_kwargs={
                    "normalize_embeddings":
                        True
                }
            )
        )


    return _embeddings


# =========================================================
# CHUNKS
# =========================================================

def crear_chunks():
    """
    Divide los documentos de conocimiento
    en fragmentos para ChromaDB.
    """

    splitter = (
        RecursiveCharacterTextSplitter(

            chunk_size=(
                CHUNK_SIZE
            ),

            chunk_overlap=(
                CHUNK_OVERLAP
            ),

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
    )


    return splitter.split_documents(
        DOCUMENTOS
    )


# =========================================================
# VERSIÓN INDEXADA
# =========================================================

def obtener_version_indexada() -> str | None:
    """
    Lee la versión de conocimiento actualmente
    almacenada en ChromaDB.
    """

    if not ARCHIVO_VERSION.exists():

        return None


    try:

        return (
            ARCHIVO_VERSION
            .read_text(
                encoding="utf-8"
            )
            .strip()
        )

    except Exception:

        return None


# =========================================================
# GUARDAR VERSIÓN
# =========================================================

def guardar_version_indexada():
    """
    Guarda la versión actual de la base técnica.
    """

    DIRECTORIO_CHROMA.mkdir(
        parents=True,
        exist_ok=True
    )


    ARCHIVO_VERSION.write_text(
        BASE_CONOCIMIENTO_VERSION,
        encoding="utf-8"
    )


# =========================================================
# COMPROBAR RECONSTRUCCIÓN
# =========================================================

def necesita_reconstruccion() -> bool:
    """
    Determina si ChromaDB necesita reconstruirse.
    """

    archivo_db = (
        DIRECTORIO_CHROMA
        / "chroma.sqlite3"
    )


    # No existe todavía
    if not archivo_db.exists():

        return True


    version_indexada = (
        obtener_version_indexada()
    )


    # Base creada antes del sistema de versiones
    if version_indexada is None:

        return True


    # Cambió la versión
    if (
        version_indexada
        != BASE_CONOCIMIENTO_VERSION
    ):

        return True


    return False


# =========================================================
# ELIMINAR BASE ANTERIOR
# =========================================================

def eliminar_vectorstore_anterior():
    """
    Elimina físicamente la base Chroma anterior.
    """

    global _vectorstore


    _vectorstore = None


    if DIRECTORIO_CHROMA.exists():

        shutil.rmtree(
            DIRECTORIO_CHROMA
        )


# =========================================================
# CREAR VECTORSTORE
# =========================================================

def crear_vectorstore():
    """
    Construye ChromaDB desde cero utilizando
    la base de conocimiento actual.
    """

    global _vectorstore


    DIRECTORIO_CHROMA.mkdir(
        parents=True,
        exist_ok=True
    )


    embeddings = (
        obtener_embeddings()
    )


    chunks = (
        crear_chunks()
    )


    _vectorstore = (
        Chroma.from_documents(

            documents=chunks,

            embedding=embeddings,

            collection_name=(
                NOMBRE_COLECCION
            ),

            persist_directory=str(
                DIRECTORIO_CHROMA
            )
        )
    )


    guardar_version_indexada()


    return _vectorstore


# =========================================================
# OBTENER VECTORSTORE
# =========================================================

def obtener_vectorstore():
    """
    Recupera ChromaDB.

    Si detecta que la base de conocimiento cambió,
    reconstruye automáticamente el índice.
    """

    global _vectorstore


    if _vectorstore is not None:

        return _vectorstore


    if necesita_reconstruccion():

        eliminar_vectorstore_anterior()

        return crear_vectorstore()


    embeddings = (
        obtener_embeddings()
    )


    _vectorstore = Chroma(

        collection_name=(
            NOMBRE_COLECCION
        ),

        embedding_function=(
            embeddings
        ),

        persist_directory=str(
            DIRECTORIO_CHROMA
        )
    )


    return _vectorstore


# =========================================================
# RECONSTRUCCIÓN MANUAL
# =========================================================

def reconstruir_vectorstore():
    """
    Permite reconstruir manualmente ChromaDB
    cuando sea necesario.
    """

    eliminar_vectorstore_anterior()

    return crear_vectorstore()


# =========================================================
# INFORMACIÓN DE LA BASE
# =========================================================

def obtener_info_base() -> dict:
    """
    Devuelve información básica sobre
    la base de conocimiento.
    """

    chunks = crear_chunks()


    return {

        "version":
            BASE_CONOCIMIENTO_VERSION,

        "documentos":
            len(DOCUMENTOS),

        "fragmentos":
            len(chunks),

        "modelo_embeddings":
            MODELO_EMBEDDINGS,

        "coleccion":
            NOMBRE_COLECCION
    }


# =========================================================
# BÚSQUEDA ESTRUCTURADA
# =========================================================

def buscar_documentos_vectoriales(
    consulta: str,
    cantidad: int = 3
) -> list[dict]:
    """
    Busca documentos utilizando similitud semántica.

    Se utiliza directamente desde Streamlit.
    """

    consulta = (
        consulta
        .strip()
    )


    if not consulta:

        return []


    cantidad = max(
        1,
        min(
            cantidad,
            5
        )
    )


    vectorstore = (
        obtener_vectorstore()
    )


    documentos = (
        vectorstore
        .similarity_search(
            consulta,
            k=cantidad
        )
    )


    resultados = []


    for documento in documentos:

        metadata = (
            documento.metadata
        )


        resultados.append(
            {

                "contenido":
                    documento
                    .page_content
                    .strip(),

                "categoria":
                    metadata.get(
                        "categoria",
                        "Sin categoría"
                    ),

                "subcategoria":
                    metadata.get(
                        "subcategoria",
                        "General"
                    ),

                "fuente":
                    metadata.get(
                        "fuente",
                        "No disponible"
                    ),

                "version":
                    metadata.get(
                        "version",
                        BASE_CONOCIMIENTO_VERSION
                    )
            }
        )


    return resultados


# =========================================================
# BÚSQUEDA PARA CREWAI
# =========================================================

def buscar_conocimiento_vectorial(
    consulta: str,
    cantidad: int = 2
) -> str:
    """
    Recupera documentos y los transforma en texto
    para el agente investigador.
    """

    resultados = (
        buscar_documentos_vectoriales(

            consulta=consulta,

            cantidad=cantidad
        )
    )


    if not resultados:

        return (
            "No se encontró información técnica "
            "relacionada con la consulta."
        )


    bloques = []


    for numero, resultado in enumerate(
        resultados,
        start=1
    ):

        bloque = (
            f"Resultado técnico {numero}\n"
            f"Categoría: {resultado['categoria']}\n"
            f"Subcategoría: {resultado['subcategoria']}\n"
            f"Fuente: {resultado['fuente']}\n"
            f"Contenido:\n"
            f"{resultado['contenido']}"
        )


        bloques.append(
            bloque
        )


    return "\n\n---\n\n".join(
        bloques
    )