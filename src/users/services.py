import uuid

from .tasks import send_activation_email

# from .constants import USER_ACTIVATION_UUID_NAMESPACE


def create_activation_key(email: str) -> uuid.UUID:
    return uuid.uuid3(namespace=uuid.uuid4(), name=email)


def create_activation_link(activation_key: uuid.UUID) -> str:
    return f"{activation_key}"


def send_user_activation_email(email: str) -> None:
    """Send activation email using SMTP."""

    activation_key: uuid.UUID = create_activation_key(email)
    activation_link = create_activation_link(activation_key)

    send_activation_email.delay(recipient=email, activation_link=activation_link) # noqa
