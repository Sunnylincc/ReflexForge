from dataclasses import dataclass


@dataclass
class SandboxReport:
    stage: str
    isolated: bool = True
