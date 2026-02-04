from apps.services.utils import Client, AsyncClient
from abc import ABC
from dataclasses import dataclass, field


class WikiClient(Client):
    def get_search_result(
            self,
            text: str,
            version: int = 2,
            lang: str | None = None,
            scope: str | None = None,
            ehs: int | None = None,
            per_page: int | None = None,
            layers: str = 'all'
    ) -> dict:
        params = {'text': text, 'version': version, 'layers': layers}
        if lang is not None:
            params['lang'] = lang
        if scope is not None:
            params['scope'] = scope
        if ehs is not None:
            params['feature.enable_highlight_suggest'] = ehs
        if per_page is not None:
            params['all.per_page'] = per_page
        return dict(self.request('', 'GET', params=params))['all']['result']
