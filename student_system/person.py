"""Person: abstract base class in the class diagram."""

from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id: str, name: str, email: str) -> None:
        if not person_id.strip():
            raise ValueError("person_id cannot be empty")
        if not name.strip():
            raise ValueError("name cannot be empty")
        if "@" not in email:
            raise ValueError("email is not valid")

        self._person_id = person_id
        self._name = name
        self._email = email

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @abstractmethod
    def get_role(self) -> str:
        """Return the role of this person."""
