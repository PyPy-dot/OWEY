import win32crypt
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


def encrypt_value(value: str) -> bytes:
    if not isinstance(value, str):
        raise TypeError('value must be str')
    byte_value = value.encode('utf-8')
    return win32crypt.CryptProtectData(byte_value, None, None, None, None, 0)


def decrypt_value(value: bytes) -> str:
    if not isinstance(value, bytes):
        raise TypeError('value must be bytes')
    byte_value = win32crypt.CryptUnprotectData(value, None, None, None, 0)[1]
    return byte_value.decode('utf-8')


class Token(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.BinaryField()
    service = models.CharField(max_length=30)
    expires = models.DateTimeField(blank=True, null=True)

    class TokenExpiredError(Exception):
        """Ошибка возникает при использовании просроченного токена."""
        pass

    class TokenInvalidError(Exception):
        """Ошибка возникает при использовании невалидного токена."""
        pass

    @classmethod
    def save_token(cls, token: str, service: str) -> None:
        date = datetime.fromtimestamp(int(token.split(':')[1]), timezone.get_fixed_timezone(timedelta(hours=3)))
        expires = date + timedelta(days=365)
        cls.objects.update_or_create(service=service, defaults={'value': encrypt_value(token), 'expires': expires})

    @classmethod
    def read_token(cls, service: str) -> dict:
        token = cls.objects.get(service=service)
        return {
            'value': decrypt_value(token.value),
            'expires': token.expires.astimezone(timezone.get_fixed_timezone(timedelta(hours=3)))
        }

    @classmethod
    async def aread_token(cls, service: str) -> dict:
        token = await cls.objects.aget(service=service)
        return {
            'value': decrypt_value(token.value),
            'expires': token.expires.astimezone(timezone.get_fixed_timezone(timedelta(hours=3)))
        }

    @classmethod
    async def asave_token(cls, token: str, service: str) -> None:
        date = datetime.fromtimestamp(int(token.split(':')[1]), timezone.get_fixed_timezone(timedelta(hours=3)))
        expires = date + timedelta(days=365)
        await cls.objects.aupdate_or_create(service=service, defaults={
            'value': encrypt_value(token),
            'expires': expires
        })

    def __str__(self):
        return f'{self.service}: {decrypt_value(self.value)}'
