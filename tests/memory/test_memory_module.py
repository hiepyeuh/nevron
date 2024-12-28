# from unittest.mock import AsyncMock, MagicMock, patch
# import pytest
# from loguru import logger
# from openai import AsyncOpenAI

# from src.core.defs import MemoryBackendType
# from src.memory.memory_module import MemoryModule, get_memory_module
# from src.memory.backends.qdrant import QdrantBackend
# from src.memory.backends.chroma import ChromaBackend


# @pytest.fixture
# def mock_logger(monkeypatch):
#     """Mock logger for testing."""
#     mock_debug = MagicMock()
#     mock_error = MagicMock()
#     monkeypatch.setattr(logger, "debug", mock_debug)
#     monkeypatch.setattr(logger, "error", mock_error)
#     return mock_debug, mock_error


# @pytest.fixture
# def mock_openai_client():
#     """Create a mock OpenAI client."""
#     return AsyncMock(spec=AsyncOpenAI)


# @pytest.fixture
# def mock_embedding_generator():
#     """Create a mock EmbeddingGenerator."""
#     with patch("src.memory.memory_module.EmbeddingGenerator") as mock:
#         generator = mock.return_value
#         generator.get_embedding = AsyncMock(return_value=[[0.1, 0.2, 0.3]])
#         yield generator


# @pytest.fixture
# def mock_qdrant_backend():
#     """Create a mock Qdrant backend."""
#     with patch("src.memory.memory_module.QdrantBackend") as mock:
#         backend = mock.return_value
#         backend.store = AsyncMock()
#         backend.search = AsyncMock(return_value=[
#             {"event": "test event", "action": "test action", "outcome": "test outcome"}
#         ])
#         yield backend


# @pytest.fixture
# def mock_chroma_backend():
#     """Create a mock Chroma backend."""
#     with patch("src.memory.memory_module.ChromaBackend") as mock:
#         backend = mock.return_value
#         backend.store = AsyncMock()
#         backend.search = AsyncMock(return_value=[
#             {"event": "test event", "action": "test action", "outcome": "test outcome"}
#         ])
#         yield backend


# @pytest.mark.parametrize("backend_type,backend_class", [
#     (MemoryBackendType.QDRANT, QdrantBackend),
#     (MemoryBackendType.CHROMA, ChromaBackend),
# ])
# def test_memory_module_init(mock_openai_client, backend_type, backend_class):
#     """Test MemoryModule initialization with different backends."""
#     # arrange/act:
#     with patch(f"src.memory.memory_module.{backend_class.__name__}") as mock_backend:
#         module = MemoryModule(
#             openai_client=mock_openai_client,
#             backend_type=backend_type,
#             collection_name="test_collection",
#             host="localhost",
#             port=6333,
#             vector_size=1536,
#             persist_directory="./persist"
#         )

#         # assert:
#         assert isinstance(module.backend, mock_backend.return_value.__class__)
#         if backend_type == MemoryBackendType.QDRANT:
#             mock_backend.assert_called_once_with(
#                 collection_name="test_collection",
#                 host="localhost",
#                 port=6333,
#                 vector_size=1536
#             )
#         else:
#             mock_backend.assert_called_once_with(
#                 collection_name="test_collection",
#                 persist_directory="./persist"
#             )


# def test_memory_module_init_invalid_backend():
#     """Test MemoryModule initialization with invalid backend type."""
#     with pytest.raises(ValueError, match="Unsupported backend type: invalid"):
#         MemoryModule(backend_type="invalid")


# @pytest.mark.asyncio
# @pytest.mark.parametrize("backend_fixture", ["mock_qdrant_backend", "mock_chroma_backend"])
# async def test_memory_storage(mock_embedding_generator, request, backend_fixture):
#     """Test memory storage functionality with different backends."""
#     # arrange:
#     backend = request.getfixturevalue(backend_fixture)
#     module = MemoryModule(backend_type="qdrant")  # Type doesn't matter as backend is mocked

#     # act:
#     await module.store(
#         event="test event",
#         action="test action",
#         outcome="test outcome",
#         metadata={"key": "value"}
#     )

#     # assert:
#     mock_embedding_generator.get_embedding.assert_called_once_with(
#         "test event test action test outcome"
#     )
#     backend.store.assert_called_once_with(
#         event="test event",
#         action="test action",
#         outcome="test outcome",
#         embedding=[0.1, 0.2, 0.3],
#         metadata={"key": "value"}
#     )


# @pytest.mark.asyncio
# @pytest.mark.parametrize("backend_fixture", ["mock_qdrant_backend", "mock_chroma_backend"])
# async def test_memory_search(mock_embedding_generator, request, backend_fixture):
#     """Test memory search functionality with different backends."""
#     # arrange:
#     backend = request.getfixturevalue(backend_fixture)
#     module = MemoryModule(backend_type="qdrant")  # Type doesn't matter as backend is mocked

#     # act:
#     results = await module.search("test query", top_k=3)

#     # assert:
#     mock_embedding_generator.get_embedding.assert_called_once_with("test query")
#     backend.search.assert_called_once_with(
#         query_vector=[0.1, 0.2, 0.3],
#         top_k=3
#     )
#     assert len(results) == 1
#     assert results[0]["event"] == "test event"
#     assert results[0]["action"] == "test action"
#     assert results[0]["outcome"] == "test outcome"


# @pytest.mark.parametrize("backend_type", [
#     MemoryBackendType.QDRANT,
#     MemoryBackendType.CHROMA
# ])
# def test_get_memory_module(mock_openai_client, backend_type):
#     """Test get_memory_module factory function."""
#     # arrange/act:
#     with patch(f"src.memory.memory_module.MemoryModule") as mock_module:
#         module = get_memory_module(
#             openai_client=mock_openai_client,
#             backend_type=backend_type
#         )

#         # assert:
#         mock_module.assert_called_once_with(
#             openai_client=mock_openai_client,
#             backend_type=backend_type
#         )
#         assert module == mock_module.return_value
