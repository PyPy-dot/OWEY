import json
from aiohttp import ClientSession
from requests import Session
from typing import Optional, Any
from urllib.parse import urlparse

from apps.services.models import Token
from django.utils import timezone


class AuthenticationError(Exception):
    """
    Raised when authentication with the server fails.
    """
    pass


class CSRFResponseError(Exception):
    """
    Raised when the request to obtain the CSRF token fails or returns an invalid response.
    """
    pass


class RequestError(Exception):
    """
    Raised when an API request fails due to an unexpected response or error status.
    """
    pass


class BaseClient:
    """
    Base class for clients.
    """
    service: str | None = None
    search_params: Any | None = None

    def __init__(self) -> None:
        """
        Initializes the BaseClient.
        Sets default user agent, initializes session and data dictionaries,
        and defines URLs for authentication.
        """
        self.user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                           '136.0.0.0 YaBrowser/25.6.0.0 Safari/537.36')
        self._session = None
        self.data = {
            'login': 'LOGIN',
            'passwd': 'PASSWORD'
        }
        self.urls = {
            'csrf-token': {
                'chatterbox': ('https://supchat.taxi.yandex-team.ru/chatterbox-api/me/', 'POST'),
                'bc_admin': ('https://admin-external.smena.yandex-team.ru/api/admin/me', 'GET'),
            },
            'passport': {
                'auth': ('https://passport.yandex-team.ru/auth', 'POST'),
                'update': ('https://passport.yandex-team.ru/auth/update', 'GET')
            },
            'hosts': {
                'chatterbox': ''
            }
        }

    def _parse_search_params(self) -> str:
        params = self.search_params.__dict__
        string_params = '&'.join([
            f'{key}={value}' if not isinstance(value, list) else '&'.join(map(
                lambda it: f'{key}={it}', value
            )) for key, value in params if value is not None
        ])
        return string_params

    def _set_search_params(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.search_params.__setattr__(key, value)

    @staticmethod
    def get_url(name: str) -> str:
        with open('apps/services/network/hosts.json', 'r') as file:
            url = dict(json.load(file)).get(name)
        return url


# ------------------- Client's logic --------------------------- #

class AsyncClient(BaseClient):
    """
    Asynchronous client for making requests.
    """

    async def __aenter__(self):
        """
        Asynchronous context manager entry point.
        Authenticates the client before entering the context.
        """
        await self.auth()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Asynchronous context manager exit point.
        Closes the session after exiting the context.
        """
        await self.close()

    async def request(self, url: str, method: str, **kwargs) -> Optional[dict]:
        """
        Makes an asynchronous GET and POST request to the specified URL

        Args:
            url: The URL to make the request to
            method: The HTTP method to use

        Returns:
            A dictionary containing the JSON response from the server

        Raises:
            RuntimeError: If the session is not initialized.
        """
        if self._session is None:
            raise RuntimeError('Session is not initialized. Call auth() first.')
        async with self._session.request(method, url, **kwargs) as resp:
            if resp.status == 200:
                meta = await resp.json()
                return meta
            else:
                print(resp.status, resp.reason, self.service)
                raise RequestError

    async def auth(self) -> None:
        """
        Authenticates the client with the server.
        """
        if not self.is_active:
            url, method = self.urls['passport']['auth']
            headers = {'User-Agent': self.user_agent, 'Host': 'passport.yandex-team.ru'}
            self._session = ClientSession(headers=headers)
            async with self._session.request(method, url, data=self.data) as resp:
                if resp.status == 200:
                    print('Auth:', resp.status)
                else:
                    print('Auth failed', resp.status)
            self._session.headers.pop('Host', None)
            self._session.headers['X-Csrf-Token'] = await self._take_csrf_token()
        else:
            raise RuntimeError('Session already initialized')

    async def _take_csrf_token(self) -> str:
        """
        Retrieves the CSRF token from the server

        Returns:
            The CSRF token.
        """
        try:
            token = await Token.aread_token(self.service)
            if timezone.now() < token['expires']:
                return token['value']
            else:
                raise Token.TokenExpiredError
        except (Token.DoesNotExist, Token.TokenExpiredError):
            url, method = self.urls['csrf-token'][self.service]
            self._session.headers['Host'] = urlparse(url).hostname
            async with self._session.request(method, url) as resp:
                if resp.status == 200:
                    resp_token = await resp.json()
                    print('Request to csrf-token success', self.service)
                    await Token.asave_token(resp_token.get('csrf_token'), self.service)
                    return resp_token.get('csrf_token')
                else:
                    raise CSRFResponseError(f'CSRF token from service {self.service} not valid')

    async def close(self) -> None:
        """
        Closes the session.
        """
        if self._session:
            await self._session.close()

    @property
    def closed(self) -> bool | None:
        """
        Checks if the session is closed

        Returns:
            True if the session is closed, False otherwise.
        """
        if self._session:
            return self._session.closed

    @property
    def is_active(self) -> bool:
        """
        Checks if the session is active

        Returns:
            True if the session is active, False otherwise.
        """
        return self._session is not None and not self._session.closed


class Client(BaseClient):
    """
    Synchronous client for making requests.
    """

    def __init__(self):
        super().__init__()
        self._closed = False

    def __enter__(self):
        """
        Context manager entry point.
        Authenticates the client before entering the context.
        """
        self.auth()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        Closes the session after exiting the context.
        """
        self.close()

    def request(self, url: str, method: str, **kwargs) -> Optional[dict]:
        """
        Makes a synchronous GET request to the specified URL

        Args:
            url: The URL to make the request to
            method: The HTTP method to use

        Returns:
            A dictionary containing the JSON response from the server

        Raises:
            RuntimeError: If the session is not initialized.
            RequestError: If the request fails.
        """
        if self._session is None:
            raise RuntimeError('Session is not initialized. Call auth() first.')
        resp = self._session.request(method, url, **kwargs)
        if resp.status_code == 200:
            meta = resp.json()
            return meta
        else:
            raise RequestError

    def auth(self) -> None:
        """
        Authenticates the client with the server.

        Raises:
            RuntimeError: If the session is already initialized.
            AuthenticationError: If the authentication fails.
        """
        if not self.is_active:
            url, method = self.urls['passport']['auth']
            self._session = Session()
            self._session.headers.update({'User-Agent': self.user_agent, 'Host': urlparse(url).hostname})
            resp = self._session.request(method, url, data=self.data)
            if resp.status_code == 200:
                print('Auth:', resp.status_code)
            else:
                raise AuthenticationError
            self._session.headers.pop('Host', None)
            self._session.headers['X-Csrf-Token'] = self._take_csrf_token()
        else:
            raise RuntimeError('Session already initialized')

    def _take_csrf_token(self) -> str:
        """
        Retrieves the CSRF token from the server

        Returns:
            The CSRF token.

        Raises:
            CSRFResponseError: If the request to csrf-token generator fails.
            Token.TokenExpiredError: If the token is expired.
        """
        try:
            token = Token.read_token(self.service)
            if timezone.now() < token['expires']:
                return token['value']
            else:
                raise Token.TokenExpiredError
        except (Token.DoesNotExist, Token.TokenExpiredError):
            url, method = self.urls['csrf-token'][self.service]
            self._session.headers['Host'] = urlparse(url).hostname
            resp = self._session.request(method, url)
            if resp.status_code == 200:
                resp_token = resp.json().get('csrf_token')
                Token.save_token(resp_token, self.service)
                print('Request to csrf-token success', self.service)
                return resp_token
            else:
                raise CSRFResponseError(f'Request to CSRF token from service {self.service} fails')

    def close(self):
        """
        Closes the session.
        """
        if self._session:
            self._session.close()
            self._closed = True

    @property
    def closed(self) -> bool:
        return self._closed

    @property
    def is_active(self) -> bool:
        return self._session is not None and not self.closed
