import win32crypt
import asyncio
import http.cookiejar as cj
from http.cookies import SimpleCookie
from aiohttp.cookiejar import CookieJar
from aiohttp.abc import AbstractCookieJar
from urllib.parse import urlparse
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
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


class Cookie(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=0)
    name = models.TextField(blank=True, null=True)
    value = models.BinaryField()
    path = models.TextField(blank=True, null=True)
    path_specified = models.BooleanField(default=False)
    expires = models.IntegerField(blank=True, null=True)
    domain = models.TextField(blank=True, null=True)
    domain_specified = models.BooleanField(default=False)
    domain_initial_dot = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    secure = models.BooleanField(default=False)

    @classmethod
    def save_cookie(cls, cookies: cj.CookieJar, url: str) -> None:
        for cookie in cookies:
            data = {
                'version': cookie.version,
                'name': cookie.name,
                'value': encrypt_value(cookie.value),
                'domain': cookie.domain if cookie.domain else urlparse(url).hostname,
                'path': cookie.path,
                'expires': cookie.expires,
                'domain_specified': cookie.domain_specified,
                'domain_initial_dot': cookie.domain_initial_dot,
                'path_specified': cookie.path_specified,
                'secure': cookie.secure,
                'comment': cookie.comment,
            }
            cls.objects.update_or_create(name=cookie.name, domain=cookie.domain, path=cookie.path, defaults=data)

    @classmethod
    def read_cookie(cls) -> cj.CookieJar:
        cookies = cls.objects.all()
        cd = cj.CookieJar()
        if cookies:
            for cookie in cookies:
                cd.set_cookie(cj.Cookie(
                    version=cookie.version,
                    name=cookie.name,
                    value=decrypt_value(cookie.value),
                    domain=cookie.domain,
                    path=cookie.path,
                    expires=cookie.expires,
                    port=None,
                    port_specified=False,
                    domain_specified=bool(cookie.domain),
                    domain_initial_dot=cookie.domain.startswith('.') if cookie.domain else False,
                    path_specified=bool(cookie.path),
                    secure=cookie.secure,
                    discard=True,
                    comment=cookie.comment,
                    comment_url=None,
                    rest={}
                ))
        return cd

    @classmethod
    async def aread_cookie(cls) -> CookieJar:
        cookies = await asyncio.to_thread(lambda: list(cls.objects.all()))
        cd = CookieJar()
        if cookies:
            for cookie in cookies:
                simple_cookie = SimpleCookie()
                simple_cookie[cookie.name] = await asyncio.to_thread(decrypt_value, cookie.value)
                simple_cookie[cookie.name]['expires'] = None
                if cookie.expires:
                    simple_cookie[cookie.name]['expires'] = datetime.strftime(
                        datetime.fromtimestamp(cookie.expires, settings.TIME_ZONE), '%a, %d %b %Y %H:%M:%S GMT')
                simple_cookie[cookie.name]['domain'] = cookie.domain
                simple_cookie[cookie.name]['path'] = cookie.path
                simple_cookie[cookie.name]['secure'] = cookie.secure
                simple_cookie[cookie.name]['version'] = cookie.version
                simple_cookie[cookie.name]['secure'] = cookie.secure
                simple_cookie[cookie.name]['comment'] = cookie.comment
                cd.update_cookies(simple_cookie)
        return cd

    @classmethod
    async def asave_cookie(cls, cookies: AbstractCookieJar, url: str) -> None:
        for cookie in cookies:
            items = cookie.__dict__
            info = dict(cookie.items())

            value = await asyncio.to_thread(encrypt_value, items['_value'])

            secure = False
            if isinstance(info['secure'], bool):
                secure = info['secure']
            elif isinstance(info['secure'], str):
                secure = info['secure'].lower() == 'true'

            expires = None
            if info['expires']:
                try:
                    expires = datetime.timestamp(datetime.strptime(info['expires'], '%a, %d %b %Y %H:%M:%S GMT'))
                except ValueError:
                    expires = None

            data = {
                'version': info['version'] if info['version'] else 0,
                'name': items['_key'],
                'value': value,
                'domain': info['domain'] if info['domain'] else urlparse(url).hostname,
                'path': info['path'] if info['path'] else '/',
                'expires': expires,
                'domain_specified': bool(info['domain']),
                'domain_initial_dot': info['domain'].startswith('.') if info['domain'] else False,
                'path_specified': bool(info['path']),
                'secure': secure,
                'comment': info['comment'],
            }
            await cls.objects.aupdate_or_create(name=data['name'], domain=data['domain'], path=data['path'],
                                                defaults=data)

    def __str__(self):
        return f'{self.name}: {decrypt_value(self.value)}'


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
