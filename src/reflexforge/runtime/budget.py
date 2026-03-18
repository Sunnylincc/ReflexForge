from reflexforge.compat import BaseModel


class RuntimeBudget(BaseModel):
    max_candidates: int
    spent_candidates: int = 0

    def consume(self) -> bool:
        if self.spent_candidates >= self.max_candidates:
            return False
        self.spent_candidates += 1
        return True
