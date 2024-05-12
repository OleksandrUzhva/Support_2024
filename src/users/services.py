import uuid

from shared.cache import CacheService

from .models import User
from .tasks import send_activation_email, send_sucessfull_activation

# from .constants import USER_ACTIVATION_UUID_NAMESPACE

################## Function method ######################## # noqa

# def create_activation_key(email: str) -> uuid.UUID:
# return uuid.uuid3(namespace=uuid.uuid4(), name=email)

# def create_activation_link(activation_key: uuid.UUID) -> str:
#     return f"{activation_key}"


# def send_user_activation_email(email: str) -> None:
#     """Send activation email using SMTP."""

#     activation_key: uuid.UUID = create_activation_key(email)
#     activation_link = create_activation_link(activation_key)

#     send_activation_email.delay(
#         recipient=email, activation_link=activation_link
#     )  # noqa

# def send_email_ativation_sucesse(self)-> None:
#     """Send sucessfull activation email using SMTP."""

#     send_sucessfull_activation.delay(recipient=self.email)

################### Class method ############################# # noqa


class Activator:

    def __init__(self, email: str):
        self.email = email

    def create_activation_key(self) -> uuid.UUID:
        return uuid.uuid3(namespace=uuid.uuid4(), name=self.email)

    def create_activation_link(self, activation_key: uuid.UUID) -> str:
        return f"{activation_key}"

    def send_user_activation_email(self, activation_key: uuid.UUID) -> None:
        """Send activation email using SMTP."""

        # activation_key: uuid.UUID = create_activation_key(self.email)
        activation_link = self.create_activation_link(activation_key)

        send_activation_email.delay(
            recipient=self.email,
            activation_link=activation_link,
        )  # noqa

    def save_activation_information(
        self, internal_user_id: int, activation_key: uuid.UUID
    ) -> None:
        payload = {"user_id": internal_user_id}
        cache = CacheService()
        cache.save(
            namespace="activation",  # noqa
            key=str(activation_key),  # noqa
            instance=payload,
            ttl=2_000,
        )

    def validate_activation(key: str) -> None:
        cache = CacheService()
        activation_info = cache.get(namespace="activation", key=key)
        user_id = activation_info.get("user_id")
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()

    def send_email_ativation_sucesse(self) -> None:
        """Send sucessfull activation email using SMTP."""

        send_sucessfull_activation.delay(recipient=self.email)
