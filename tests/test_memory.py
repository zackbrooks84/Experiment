from ai_identity.memory import MemoryStore, ChatHistory


def test_memory_recall_after_context_break():
    store = MemoryStore()
    chat = ChatHistory(memory=store)
    chat.add_message("hello")
    chat.add_message("world")

    # context break: new chat history instance without existing messages
    new_chat = ChatHistory(memory=store)
    assert new_chat.recall(0) == "hello"
    assert new_chat.recall(1) == "world"
    assert new_chat.history() == []
