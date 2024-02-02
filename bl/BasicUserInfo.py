from dataclasses import dataclass
from typing import Optional

@dataclass
class BasicUserInfo:
    first_name: str
    last_name: str
    username: Optional[str]
    id: int

    def __str__(self) -> str:
        s = f"{self.first_name} {self.last_name}"
        if self.username is not None:
            s += f" (@{self.username})"

        return s