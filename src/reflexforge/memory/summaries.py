from reflexforge.memory.retrieval import LessonMemory


def summarize_lessons(memory: LessonMemory) -> str:
    top = memory.top(3)
    if not top:
        return "No lessons yet."
    return " | ".join(f"{l.key}:{l.summary}" for l in top)
