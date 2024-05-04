from dataclasses import dataclass


@dataclass
class EmailMessage:
    body: str
    text: str
    sender: str
