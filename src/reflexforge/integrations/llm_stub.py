class LLMStub:
    """Placeholder integration for future providers."""

    def generate(self, prompt: str) -> str:
        return f"stub:{hash(prompt) % 10000}"
