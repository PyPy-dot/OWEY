from dataclasses import dataclass, field
from abc import ABC

from apps.services.utils import Client, AsyncClient


@dataclass
class TaskSearchItem:
    autoru_client_id: str = None  # ID Частника Авто.ру
    autoru_dealer_id: str = None  # ID Дилера Авто.ру/СМЕ
    b2b_short_ticket_id: str = None  # ID тикета в ПИ
    car_number: str = None  # Номер машины
    chat_type: str = None  # chat_type
    city: str = None  # Город
    clid: str = None  # CLID парка
    contract_number: str = None  # contract_number
    corp_client_id: str = None  # ID корпоративного клиента
    country: str = 'rus'  # country
    custom_themes: str = None  # custom_themes
    destination_email: str = None  # destination_email
    device_model: str = None  # Устройство
    driver_license: str = None  # Номер ВУ
    driver_license_pd_id: str = None  # Personal id ВУ
    driver_name: str = None  # ФИО водителя
    driver_uuid: str = None  # UUID водителя
    eater_passport_uid: str = None  # eater_passport_uid
    email_from: str = None  # email_from
    external_id: str = None  # external_id
    fintech_service: str = None  # fintech_service
    fuel_order_id: str = None  # Заправки Заказ
    lavka_wms_cluster: str = None  # Город Лавки
    lavka_wms_title: str = None  # Адрес Лавки
    lines: list = field(default_factory=list)  # Виды
    login: str = None  # Саппорт
    login_id: str = None  # Telegram login id
    merch_site: str = None  # merch_site
    order_id: str = None  # Заказ
    park_db_id: str = None  # DBID парка
    park_name: str = None  # Название парка
    partner_details_partnerInternalName: str = None  # Внутреннее имя партнера
    partner_id: str = None  # Айди Партнера
    phone: str = None  # phone
    product_id: str = None  # product_id
    realty_room_id: str = None  # ID чат-комнаты (Недвижимость)
    restapp_company: str = None  # Юридическое название ресторана
    restapp_inn: str = None  # ИНН ресторана
    restapp_order_id: str = None  # Номер заказа ресторана
    restapp_place_id: str = None  # RestApp Place ID
    restapp_rest: str = None  # Название ресторана
    scooters_vehicle_number: str = None  # scooters_vehicle_number
    short_order_id: str = None  # Короткий ID заказа
    status: str = None  # Статус
    tags: list = field(default_factory=list)  # Теги
    tags_search_method: str = 'and'
    taximeter_version: str = None  # Версия Яндекс.Про
    telegram_user_id: str = None  # telegram_user_id
    text: str = None  # Текст
    ticket_subject: str = None  # Тема обращения
    unique_driver_id: str = None  # unique_driver_id
    user_email: str = None  # Почта клиента
    user_id: str = None  # User ID
    user_phone: str = None  # Телефон
    user_phone_pd_id: str = None  # Personal id телефона
    user_uid: str = None  # Yandex User ID
    created: str = None  # Дата {%Y-%m-%d}
    created_from: str = None  # Дата с {%Y-%m-%d %H:%M}
    created_to: str = None  # Дата до {%Y-%m-%d %H:%M}
    limit: int = 100  # Лимит
    offset: int = 0  # Шаг

    def keys(self) -> list:
        return list(self.__dict__)

    def values(self) -> list:
        return list(self.__dict__.values())

    def items(self) -> list:
        return list(self.__dict__.items())


class BaseChatterbox(ABC):
    service: str = 'chatterbox'
    search_params = TaskSearchItem()

    @staticmethod
    def get_url(name: str) -> str:
        return {
            "get_chat": "https://supchat.taxi.yandex-team.ru/chatterbox-api/v1/tasks/",
            "get_available_fields": "https://supchat.taxi.yandex-team.ru/chatterbox-api/v1/tasks/search/available_fields/",
            "get_user_status": 'https://supchat.taxi.yandex-team.ru/chatterbox-api/v1/user/status/',
            "post_available_lines": "https://supchat.taxi.yandex-team.ru/chatterbox-api/v1/lines/available/",
            "post_tasks_search": "https://supchat.taxi.yandex-team.ru/chatterbox-api/v1/tasks/search/"
        }[name]

    @staticmethod
    def _parse_chatterbox(resp: dict) -> dict:
        return {
            'id': resp.get('id'),
            'chat_type': resp.get('chat_type'),
            'chats': resp.get('chats'),
            'comment_is_read_only': resp.get('comment_is_read_only'),
            'contacts': resp.get('contacts'),
            'created': resp.get('created'),
            'external_id': resp.get('external_id'),
            'omnichat_id': resp.get('omnichat_id'),
            'customers': resp.get('customers'),
            'operators': resp.get('operators'),
            'recipients': resp.get('recipients'),
            'line': resp.get('line'),
            'status': resp.get('status'),
            'state': resp.get('state'),
            'resolution': resp.get('resolution'),
            'ivr_settings': resp.get('ivr_settings'),
            'sip_settings': resp.get('sip_settings'),
            'support_uid': resp.get('support_uid'),
            'meta_info': {
                'order_id': resp['meta_info'].get('order_id'),
                'active_shift_id': resp['meta_info'].get('active_shift_id'),
                'active_shift_org_id': resp['meta_info'].get('active_shift_org_id'),
                'active_shift_site_address': resp['meta_info'].get('active_shift_site_address'),
                'active_shift_site_id': resp['meta_info'].get('active_shift_site_id'),
                "scenario_title": resp['meta_info'].get('scenario_title'),
                "screen_attach": resp['meta_info'].get('screen_attach'),
                "last_assignee_uid": resp['meta_info'].get('last_assignee_uid'),
                "park_id": resp['meta_info'].get('park_id'),
                "chat_in_omnichat": resp['meta_info'].get('chat_in_omnichat'),
                "block_status": resp['meta_info'].get('block_status'),
                "chatterbox_button": resp['meta_info'].get('chatterbox_button'),
                'request_assignment_time': resp['meta_info'].get('request_assignment_time'),
                "finished_shifts_count": resp['meta_info'].get('finished_shifts_count'),
                "chatterbox_archiving_deadline_time": resp['meta_info'].get('chatterbox_archiving_deadline_time'),
                "autoreply_count_forward": resp['meta_info'].get('autoreply_count_forward'),
                "user_id": resp['meta_info'].get('user_id'),
                'custom_themes': resp['meta_info'].get('custom_themes'),
                "custom_manual_themes": resp['meta_info'].get('custom_manual_themes'),
                "deprecated_task_type": resp['meta_info'].get('deprecated_task_type'),
                "source": resp['meta_info'].get('source'),
                "last_support_action": resp['meta_info'].get('last_support_action'),
                "supportai_waiting_triggered_by_chatterbot": resp['meta_info'].get(
                    'supportai_waiting_triggered_by_chatterbot'),
                "fintech_manual_theme": resp['meta_info'].get('fintech_manual_theme'),
                "use_autoreply_count": resp['meta_info'].get('use_autoreply_count'),
                "ml_predicted_line": resp['meta_info'].get('ml_predicted_line'),
                "have_medcard_payout": resp['meta_info'].get('have_medcard_payout'),
                "number_of_reopens": resp['meta_info'].get('number_of_reopens'),
                "messenger_chat_id": resp['meta_info'].get('messenger_chat_id'),
                "user_uid": resp['meta_info'].get('user_uid'),
                "is_new_chatterbot_integration": resp['meta_info'].get('is_new_chatterbot_integration'),
                "person_id": resp['meta_info'].get('person_id'),
                "user_locale": resp['meta_info'].get('user_locale'),
                "supportai_projects": resp['meta_info'].get('supportai_projects'),
                "supportai_keep_ticket_on_robot": resp['meta_info'].get('supportai_keep_ticket_on_robot'),
                "last_user_message_id": resp['meta_info'].get('last_user_message_id'),
                "preset_name": resp['meta_info'].get('preset_name'),
                "ml_request_id": resp['meta_info'].get('ml_request_id'),
                "chatterbox_archiving_stq_task_id": resp['meta_info'].get('chatterbox_archiving_stq_task_id'),
                "recently_used_macro_ids": resp['meta_info'].get('recently_used_macro_ids'),
                "autoreply_count_comment": resp['meta_info'].get('autoreply_count_comment'),
                "sorry_payout_count": resp['meta_info'].get('sorry_payout_count'),
                "db_id": resp['meta_info'].get('db_id'),
                "messenger_bot_id": resp['meta_info'].get('messenger_bot_id'),
                "check_autoreply_count": resp['meta_info'].get('check_autoreply_count'),
                "worker_category": resp['meta_info'].get('worker_category'),
                "batch_id": resp['meta_info'].get('batch_id'),
                "status_before_assign": resp['meta_info'].get('status_before_assign'),
                'x5_flg': resp['meta_info'].get('x5_flg'),
                'user_refund_count': resp['meta_info'].get('user_refund_count'),
                'user_platform': resp['meta_info'].get('user_platform'),
                'user_phone_pd_id': resp['meta_info'].get('user_phone_pd_id'),
                'user_phone': resp['meta_info'].get('user_phone'),
                'user_messages_count': resp['meta_info'].get('user_messages_count'),
                'task_language': resp['meta_info'].get('task_language'),
                'storing_in_omnichat': resp['meta_info'].get('storing_in_omnichat'),
                'site_id': resp['meta_info'].get('site_id'),
                'request_id': resp['meta_info'].get('request_id'),
                'phone_type': resp['meta_info'].get('phone_type'),
                'message_text': resp['meta_info'].get('message_text'),
                'country': resp['meta_info'].get('country'),
                'calls': resp['meta_info'].get('calls'),
                'call_guid': resp['meta_info'].get('call_guid'),
                'ask_csat': resp['meta_info'].get('ask_csat'),
                'antifraud_rules': resp['meta_info'].get('antifraud_rules'),
            },
            'ticket_postponement': resp.get('ticket_postponement'),
            'meta_to_show': resp.get('meta_to_show'),
            'history': resp.get('history'),
            'hidden_comments': resp.get('hidden_comments'),
            'chat_messages': {
                'messages': resp['chat_messages'].get('messages'),
                'total': resp['chat_messages'].get('total'),
            },
            'tags': resp.get('tags'),
            'orders_links': resp.get('orders_links'),
            'support_alias': resp.get('support_alias'),
            'type': resp.get('type'),
            'updated': resp.get('updated'),
        }

    @staticmethod
    def _pars_user_status(resp: dict) -> dict:
        return {
            'assigned_lines': resp.get('assigned_lines'),
            'available_modes': resp.get('available_modes'),
            'can_choose_except_assigned_lines': resp.get('can_choose_except_assigned_lines'),
            'can_choose_from_assigned_lines': resp.get('can_choose_from_assigned_lines'),
            'current_status': resp.get('current_status'),
            'dashboard_next_request_timeout': resp.get('dashboard_next_request_timeout'),
            'default_work_status': resp.get('default_work_status'),
            'incoming_calls_allowed': resp.get('incoming_calls_allowed'),
            'lines': resp.get('lines'),
            'next_request_timeout': resp.get('next_request_timeout'),
            'status_list': resp.get('status_list'),
        }


class ChatterboxClient(BaseChatterbox, Client):
    def get_chat(self, ticket_id: str) -> dict:
        resp = dict(self.request(f'{self.get_url('get_chat')}{ticket_id}', 'GET'))
        return self._parse_chatterbox(resp)

    def get_available_fields(self):
        return dict(self.request(self.get_url('get_available_fields'), 'GET'))

    def get_user_status(self) -> dict:
        resp = dict(self.request(self.get_url('get_user_status'), 'GET'))
        return self._pars_user_status(resp)

    def post_available_lines(self):
        return dict(self.request(self.get_url('post_available_lines'), 'POST'))

    def post_tasks_search(self, json: dict) -> dict:
        return dict(self.request(self.get_url('post_tasks_search'), 'POST', json=json))


class AsyncChatterboxClient(BaseChatterbox, AsyncClient):
    async def get_chat(self, ticket_id: str) -> dict:
        resp = dict(await self.request(f'{self.get_url('get_chat')}{ticket_id}', 'GET'))
        return self._parse_chatterbox(resp)

    async def get_available_fields(self):
        return dict(await self.request(self.get_url('get_available_fields'), 'GET'))

    async def get_user_status(self) -> dict:
        resp = dict(await self.request(self.get_url('get_user_status'), 'GET'))
        return self._pars_user_status(resp)

    async def post_available_lines(self):
        return dict(await self.request(self.get_url('post_available_lines'), 'POST'))

    async def post_tasks_search(self, json: dict) -> dict:
        return dict(await self.request(self.get_url('post_tasks_search'), 'POST', json=json))
