from apps.services.utils import Client, AsyncClient
from abc import ABC
from dataclasses import dataclass, field


@dataclass
class SiteSearchItem:
    organization_id: str = None
    group_id: list[str] = field(default_factory=list)
    site_id: str = None
    site_name: str = None
    operator_id: str = None
    city: str = None
    street: str = None
    internal_name: str = None
    internal_filial_name_mask: str = None
    internal_division_name_mask: str = None

    def keys(self) -> list:
        return list(self.__dict__)

    def values(self) -> list:
        return list(self.__dict__.values())

    def items(self) -> list:
        return list(self.__dict__.items())


class BaseBlueCollarsAdmin(ABC):
    service: str = 'bc_admin'

    @staticmethod
    def _parse_shift(resp: dict) -> dict:
        return {
            'shift_id': resp.get('id'),
            'batch_id': resp.get('batch_id'),
            'common_id': resp.get('common_id'),
            'external_id': resp.get('external_id'),
            'create_ts': resp.get('create_ts'),
            'start_time': resp.get('start_time'),
            'liked': resp.get('liked'),
            'blacklisted': resp.get('blacklisted'),
            'length': resp.get('length'),
            'rest_length': resp.get('rest_length'),
            'provider_id': resp.get('provider_id'),
            'attributes': resp.get('attributes'),
            'worker_requirements': resp.get('worker_requirements'),
            'history': resp.get('history'),
            'tags': resp.get('tags'),
            'site': {
                'id': resp['site'].get('id'),
                'name': resp['site'].get('name'),
                'internal_name': resp['site'].get('internal_name'),
                'address_id': resp['site'].get('address_id'),
                'city': resp['address'].get('city'),
                'country': resp['address'].get('country'),
                'street': resp['address'].get('street'),
            },
            'organization': {
                'id': resp['organization'].get('id'),
                'name': resp['organization'].get('name'),
                'fullname': resp['organization'].get('fullname'),
            },
            'payment': {
                'id': resp['payment'].get('id'),
                'name': resp['payment'].get('name'),
                'payment_type': resp['payment'].get('payment_type'),
                'currency': resp['payment'].get('currency'),
                'subsidy': resp.get('subsidy', 0),
                'payment_per_hour': resp['payment'].get('payment_per_hour', 0),
                'payment_per_hour_fee': resp['payment'].get('payment_per_hour_fee', 0),
                'payment_per_unit': resp['payment'].get('payment_per_unit', 0),
                'approximate_units_per_hour': resp['payment'].get('approximate_units_per_hour', 0),
                'auto_total_payment_fact_minutes': resp['payment'].get('auto_total_payment_fact_minutes', 0),
                'total_approximate': resp['payment'].get('total_approximate', 0),
                'guarantee': resp['payment'].get('guarantee', 0),
                'version_start_time': resp['payment'].get('version_start_time'),
            },
            'profession': {
                'id': resp['profession'].get('id'),
                'name': resp['profession'].get('name'),
                'is_training': resp['profession'].get('is_training'),
                'service': resp['profession'].get('service'),
                'version_start_time': resp['profession'].get('version_start_time'),
                'worker_registration_required': resp['profession'].get('worker_registration_required'),
                'work_description': resp['profession'].get('work_description'),
                'things_to_take': resp['profession'].get('things_to_take'),
                'gender_only': resp['profession'].get('gender_only'),
            },
            'address': resp.get('address'),
            'worker': resp.get('worker'),
            'contact_person': resp.get('contact_person'),
            'state': resp.get('state'),
            'real_start_time': resp.get('real_start_time'),
            'total_length_fact': resp.get('total_length_fact'),
            'total_payment_fact': resp.get('total_payment_fact'),
            'total_rest_length_fact': resp.get('total_rest_length_fact'),
            'total_units_fact': resp.get('total_units_fact'),
            'codes': resp.get('codes'),
        }

    @staticmethod
    def _parse_demand_outlet(resp: dict) -> dict:
        return {
            'site_id': resp['site'].get('site_id'),
            'address_id': resp['site'].get('address_id'),
            'street': resp['site'].get('street'),
            'city': resp['site'].get('city'),
            'country': resp['site'].get('country'),
            'create_ts': resp['site'].get('create_ts'),
            'organization_id': resp['site'].get('organization_id'),
            'parent_group_id': resp['site'].get('parent_group_id'),
            'site_name': resp['site'].get('site_name'),
            'internal_name': resp['site'].get('internal_name'),
        }

    @staticmethod
    def _parse_demand_organisation(resp: dict) -> dict:
        return {
            'id': resp.get('id'),
            'name': resp.get('name'),
            'brand_id': resp.get('brand_id'),
            'brand_name': resp.get('brand_name'),
            'fullname': resp.get('fullname'),
            'available_tags': resp.get('available_tags'),
        }

    @staticmethod
    def _parse_profession(resp: dict) -> dict:
        return {
            'id': resp.get('id'),
            'group_id': resp.get('group_id'),
            'organization_id': resp.get('organization_id'),
            'name': resp.get('name'),
            'description': resp.get('description'),
            'work_description': resp.get('work_description'),
            'service': resp.get('service'),
            'create_ts': resp.get('create_ts'),
            'update_ts': resp.get('update_ts'),
            'fns_receipt_service_code': resp.get('fns_receipt_service_code'),
            'version': resp.get('version'),
            'version_start_time': resp.get('version_start_time'),
            'training_required': resp.get('training_required'),
            'worker_registration_required': resp.get('worker_registration_required'),
            'is_training': resp.get('is_training'),
            'is_hidden': resp.get('is_hidden'),
            'requirements': resp.get('requirements'),
            'things_to_take': resp.get('things_to_take'),
        }

    @staticmethod
    def _parse_payment(resp: dict) -> dict:
        return {
            'payment_id': resp.get('payment_id'),
            'name': resp.get('name'),
            'description': resp.get('description'),
            'create_ts': resp.get('create_ts'),
            'version': resp.get('version'),
            'version_start_time': resp.get('version_start_time'),
            'contract_type': resp.get('contract_type'),
            'organization_id': resp.get('organization_id'),
            'payment_per_hour': resp.get('payment_per_hour'),
            'payment_per_unit': resp.get('payment_per_unit'),
            'total_approximate': resp.get('total_approximate'),
            'guarantee': resp.get('guarantee'),
            'approximate_units_per_hour': resp.get('approximate_units_per_hour'),
            'auto_total_payment_fact_minutes': resp.get('auto_total_payment_fact_minutes'),
            'is_hidden': resp.get('is_hidden'),
        }

    @staticmethod
    def _parse_supply(resp: dict) -> dict:
        return {
            'id': resp.get('id'),
            'first_name': resp.get('first_name'),
            'middle_name': resp.get('middle_name'),
            'last_name': resp.get('last_name'),
            'gender': resp.get('gender'),
            'status': resp.get('status'),
            'category': resp.get('category'),
            'smz_status': resp.get('smz_status'),
            'create_ts': resp.get('create_ts'),
            'person_id': resp.get('person_id'),
            'clid': resp.get('clid'),
            'inn_pd_id': resp.get('inn_pd_id'),
            'phone_pd_id': resp.get('phone_pd_id'),
            'dbid_uuid': resp.get('dbid_uuid'),
            'park_id': resp.get('park_id'),
            'park_name': resp.get('park_name'),
            'docs': resp.get('docs'),
            'documents': resp.get('documents'),
            'location': resp.get('location'),
            'requirements': resp.get('requirements'),
            'app_platform': resp.get('app_platform'),
            'app_version': resp.get('app_version'),

        }

    @staticmethod
    def _parse_promo(resp: dict) -> dict:
        return {}

    @staticmethod
    def _parse_review(resp: dict) -> dict:
        return {}

    @staticmethod
    def _parse_reward(resp: dict) -> dict:
        return {}


# ----------------------- BC Admin Client ----------------------- #
class BlueCollarsAdminClient(BaseBlueCollarsAdmin, Client):
    def get_shift(self, shift_id: str) -> dict:
        resp = dict(self.request(f'{self.get_url("get_shift")}{shift_id}', 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_shift(resp)

    def get_payments(self, payment_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_payments'), 'GET',
                                 params={'id': payment_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_payment(resp)

    def get_worker(self, user_id: str) -> dict:
        resp = dict(self.request(f'{self.get_url("get_worker")}{user_id}', 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_supply(resp)

    def get_brands_names(self) -> list:
        resp = self.request(self.get_url('get_brands_names'), 'GET',
                            params={'csrf_token': self._session.headers["X-Csrf-Token"]})
        return resp.get('brands')

    def get_professions(self, profession_id: str, version: int = 0) -> dict:
        resp = dict(self.request(self.get_url('get_professions'), 'GET',
                                 params={'profession_id': profession_id,
                                         'version': version,
                                         'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_profession(resp)

    def get_organizations(self, org_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_organizations'), 'GET',
                                 params={'id': org_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_demand_organisation(resp)

    def get_organization_managers(self, org_id: str) -> dict:
        return dict(self.request(self.get_url('get_organization_managers'), 'GET',
                                 params={
                                     'organization_id': org_id,
                                     'csrf_token': self._session.headers["X-Csrf-Token"]
                                 }))

    def get_sites(self, site_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_sites'), 'GET',
                                 params={'site_id': site_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_demand_outlet(resp)

    def get_promos(self, promo_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_promos'), 'GET',
                                 params={'promo_id': promo_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_promo(resp)

    def get_reviews(self, person_id: str, site_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_reviews'), 'GET',
                                 params={
                                     'person_id': person_id,
                                     'site_id': site_id,
                                     'csrf_token': self._session.headers["X-Csrf-Token"]
                                 }))
        return self._parse_review(resp)

    def get_review_by_id(self, review_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_review_by_id'), 'GET',
                                 params={'review_id': review_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_review(resp)

    def get_reward(self, reward_id: str) -> dict:
        resp = dict(self.request(self.get_url('get_reward'), 'GET',
                                 params={'reward_id': reward_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_reward(resp)

    def get_payments_versions(self, payment_id: str) -> list:
        resp = dict(self.request(self.get_url('get_payments_versions'), 'GET',
                                 params={'id': payment_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return resp.get('payments')

    def get_professions_versions(self, profession_id: str) -> list:
        resp = dict(self.request(self.get_url('get_professions_versions'), 'GET',
                                 params={'id': profession_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return resp.get('professions')

    def get_benefit_types(self) -> list:
        return list(self.request(self.get_url('get_benefit_types'), 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_user_blocks(self, user_id: str) -> list:
        return list(self.request(f'{self.get_url("get_user_blocks")}{user_id}', 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_eta_event_types(self) -> list:
        return list(self.request(self.get_url('get_eta_event_types'), 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_eta_triggers(self) -> list:
        return list(self.request(self.get_url('get_eta_triggers'), 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_promos_history(self, promo_id: str) -> list:
        return list(self.request(self.get_url('get_promos_history'), 'GET',
                                 params={'id': promo_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_rewards_info(self) -> dict:
        return dict(self.request(self.get_url('get_rewards_info'), 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_sites_temporary_blocks(self, site_id: str) -> list:
        return list(self.request(self.get_url('get_sites_temporary_blocks'), 'GET',
                                 params={'id': site_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def get_user_info(self) -> dict:
        return dict(self.request(self.get_url('get_user_info'), 'GET',
                                 params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    def post_invites_list(self, org_id: str) -> list:
        resp = dict(self.request(self.get_url('post_invites_list'), 'POST', json={'organization_id': org_id}))
        return resp.get('invites')

    def post_organizations_balance(self, org_ids: list = None) -> list:
        if org_ids is None:
            org_ids = []
        resp = dict(self.request(self.get_url('post_organizations_balance'), 'POST',
                                 json={'organization_ids': org_ids}))
        return resp.get('organizations')

    def post_organizations_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 25}
        resp = dict(self.request(self.get_url('post_organizations_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('organizations')

    def post_payment_mappings_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(self.request(self.get_url('post_payment_mappings_list'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('content')

    def post_payments_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        resp = dict(self.request(self.get_url('post_payments_list'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('payments')

    def post_profession_groups_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 100}
        resp = dict(self.request(self.get_url('post_profession_groups_list'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('profession_groups')

    def post_professions_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(self.request(self.get_url('post_professions_list'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('professions')

    def post_hide_shift_check(self, shift_id: str) -> str | None:
        resp = dict(self.request(self.get_url('post_hide_shift_check'), 'POST', json={'shift_id': shift_id}))
        return resp.get('hide_status')

    def post_sites_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        resp = dict(self.request(self.get_url('post_sites_list'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('sites')

    def post_sites_workers_last_shifts(self, site_id: str, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {"show_blacklisted": False, "show_liked": False, "show_not_rated": False}
        if pagination is None:
            pagination = {}
        resp = dict(self.request(self.get_url('post_sites_workers_last_shifts'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}, params={'site_id': site_id}))
        return resp.get('workers')

    def post_object_by_geo_id(self, geo_ids: list) -> dict:
        if geo_ids is None:
            geo_ids = []
        return dict(self.request(self.get_url('post_object_by_geo_id'), 'POST', json={'geo_ids': geo_ids}))

    def post_park_blocks_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(self.request(self.get_url('post_park_blocks_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('items')

    def post_promos_search(self, filters: dict = None, pagination: dict = None) -> dict:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "id", "order": "desc"}]}
        resp = dict(self.request(self.get_url('post_promos_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return {'count': resp.get('count'), 'promos': resp.get('promos', [])}

    def post_referrals_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "form_filling_ts", "order": "asc"}]}
        resp = dict(self.request(self.get_url('post_referrals_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('referrals')

    def post_reviews_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(self.request(self.get_url('post_reviews_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('items')

    def post_rewards_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(self.request(self.get_url('post_rewards_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('rewards')

    def post_worker_rewards_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "create_ts", "order": "asc"}]}
        resp = dict(self.request(self.get_url('post_worker_rewards_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('worker_rewards')

    def post_shift_payouts_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": []}
        resp = dict(self.request(self.get_url('post_shift_payouts_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('shift_payouts')

    def post_worker_activity_rating_history(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(self.request(self.get_url('post_worker_activity_rating_history'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('rating_history')

    def post_worker_docs_list(self, worker_id: str) -> list:
        resp = self.request(self.get_url('post_worker_docs_list'), 'POST', json={'worker_id': worker_id})
        return resp.get('documents')

    def post_worker_payments_search(self, filters: dict = None, pagination: dict = None) -> dict:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        return dict(self.request(self.get_url('post_worker_payments_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))

    def post_workers_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}], "page_size": 5}
        resp = dict(self.request(self.get_url('post_workers_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('workers')

    def post_shift_history_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [
                {"field": "shift_create_ts", "order": "asc"},
                {"field": "shift_id", "order": "asc"},
                {"field": "timestamp", "order": "asc"}
            ]}
        resp = dict(self.request(self.get_url('post_shift_history_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('shifts_history')

    def post_shift_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 10, "sort": [{"field": "start_time", "order": "desc"}]}
        resp = dict(self.request(self.get_url('post_shift_search'), 'POST',
                                 json={'filters': filters, 'pagination': pagination}))
        return resp.get('shifts')


class AsyncBlueCollarsAdminClient(BaseBlueCollarsAdmin, AsyncClient):
    async def get_shift(self, shift_id: str) -> dict:
        print(self._session.headers["X-Csrf-Token"])
        resp = dict(await self.request(f'{self.get_url("get_shift")}{shift_id}', 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_shift(resp)

    async def get_payments(self, payment_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_payments'), 'GET',
                                       params={'id': payment_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_payment(resp)

    async def get_worker(self, user_id: str) -> dict:
        resp = dict(await  self.request(f'{self.get_url("get_worker")}{user_id}', 'GET',
                                        params={'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_supply(resp)

    async def get_brands_names(self) -> list:
        resp = await self.request(self.get_url('get_brands_names'), 'GET',
                                  params={'csrf_token': self._session.headers["X-Csrf-Token"]})
        return resp.get('brands')

    async def get_professions(self, profession_id: str, version: int = 0) -> dict:
        resp = dict(await self.request(self.get_url('get_professions'), 'GET',
                                       params={'profession_id': profession_id,
                                               'version': version,
                                               'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_profession(resp)

    async def get_organizations(self, org_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_organizations'), 'GET',
                                       params={'id': org_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return self._parse_demand_organisation(resp)

    async def get_organization_managers(self, org_id: str) -> dict:
        return dict(await self.request(self.get_url('get_organization_managers'), 'GET',
                                       params={
                                           'organization_id': org_id,
                                           'csrf_token': self._session.headers["X-Csrf-Token"]
                                       }))

    async def get_sites(self, site_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_sites'), 'GET', params={
            'site_id': site_id, 'csrf_token': self._session.headers["X-Csrf-Token"]
        }))
        return self._parse_demand_outlet(resp)

    async def get_promos(self, promo_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_promos'), 'GET', params={
            'promo_id': promo_id, 'csrf_token': self._session.headers["X-Csrf-Token"]
        }))
        return self._parse_promo(resp)

    async def get_reviews(self, person_id: str, site_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_reviews'), 'GET',
                                       params={
                                           'person_id': person_id,
                                           'site_id': site_id,
                                           'csrf_token': self._session.headers["X-Csrf-Token"]
                                       }))
        return self._parse_review(resp)

    async def get_review_by_id(self, review_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_review_by_id'), 'GET', params={
            'review_id': review_id, 'csrf_token': self._session.headers["X-Csrf-Token"]
        }))
        return self._parse_review(resp)

    async def get_reward(self, reward_id: str) -> dict:
        resp = dict(await self.request(self.get_url('get_reward'), 'GET', params={
            'reward_id': reward_id, 'csrf_token': self._session.headers["X-Csrf-Token"]
        }))
        return self._parse_reward(resp)

    async def get_payments_versions(self, payment_id: str) -> list:
        resp = dict(await self.request(self.get_url('get_payments_versions'), 'GET',
                                       params={'id': payment_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))
        return resp.get('payments')

    async def get_professions_versions(self, profession_id: str) -> list:
        resp = dict(await self.request(self.get_url('get_professions_versions'), 'GET', params={
            'id': profession_id, 'csrf_token': self._session.headers["X-Csrf-Token"]
        }))
        return resp.get('professions')

    async def get_benefit_types(self) -> list:
        return list(await self.request(self.get_url('get_benefit_types'), 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_user_blocks(self, user_id: str) -> list:
        return list(await self.request(f'{self.get_url("get_user_blocks")}{user_id}', 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_eta_event_types(self) -> list:
        return list(await self.request(self.get_url('get_eta_event_types'), 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_eta_triggers(self) -> list:
        return list(await self.request(self.get_url('get_eta_triggers'), 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_promos_history(self, promo_id: str) -> list:
        return list(await self.request(self.get_url('get_promos_history'), 'GET',
                                       params={'id': promo_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_rewards_info(self) -> dict:
        return dict(await self.request(self.get_url('get_rewards_info'), 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_sites_temporary_blocks(self, site_id: str) -> list:
        return list(await self.request(self.get_url('get_sites_temporary_blocks'), 'GET',
                                       params={'id': site_id, 'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def get_user_info(self) -> dict:
        return dict(await self.request(self.get_url('get_user_info'), 'GET',
                                       params={'csrf_token': self._session.headers["X-Csrf-Token"]}))

    async def post_invites_list(self, org_id: str) -> list:
        resp = dict(await self.request(self.get_url('post_invites_list'), 'POST', json={'organization_id': org_id}))
        return resp.get('invites')

    async def post_organizations_balance(self, org_ids: list = None) -> list:
        if org_ids is None:
            org_ids = []
        resp = dict(await self.request(self.get_url('post_organizations_balance'), 'POST',
                                       json={'organization_ids': org_ids}))
        return resp.get('organizations')

    async def post_organizations_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 25}
        resp = dict(await self.request(self.get_url('post_organizations_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('organizations')

    async def post_payment_mappings_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(await self.request(self.get_url('post_payment_mappings_list'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('content')

    async def post_payments_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        resp = dict(await self.request(self.get_url('post_payments_list'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('payments')

    async def post_profession_groups_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 100}
        resp = dict(await self.request(self.get_url('post_profession_groups_list'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('profession_groups')

    async def post_professions_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(await self.request(self.get_url('post_professions_list'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('professions')

    async def post_hide_shift_check(self, shift_id: str) -> str | None:
        resp = dict(await self.request(self.get_url('post_hide_shift_check'), 'POST', json={'shift_id': shift_id}))
        return resp.get('hide_status')

    async def post_sites_list(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        resp = dict(await self.request(self.get_url('post_sites_list'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('sites')

    async def post_sites_workers_last_shifts(self, site_id: str, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {"show_blacklisted": False, "show_liked": False, "show_not_rated": False}
        if pagination is None:
            pagination = {}
        resp = dict(await self.request(self.get_url('post_sites_workers_last_shifts'), 'POST',
                                       json={'filters': filters, 'pagination': pagination},
                                       params={'site_id': site_id}))
        return resp.get('workers')

    async def post_object_by_geo_id(self, geo_ids: list) -> dict:
        if geo_ids is None:
            geo_ids = []
        return dict(await self.request(self.get_url('post_object_by_geo_id'), 'POST', json={'geo_ids': geo_ids}))

    async def post_park_blocks_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {}
        resp = dict(await self.request(self.get_url('post_park_blocks_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('items')

    async def post_promos_search(self, filters: dict = None, pagination: dict = None) -> dict:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "id", "order": "desc"}]}
        resp = dict(await self.request(self.get_url('post_promos_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return {'count': resp.get('count'), 'promos': resp.get('promos', [])}

    async def post_referrals_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "form_filling_ts", "order": "asc"}]}
        resp = dict(await self.request(self.get_url('post_referrals_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('referrals')

    async def post_reviews_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(await self.request(self.get_url('post_reviews_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('items')

    async def post_rewards_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(await self.request(self.get_url('post_rewards_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('rewards')

    async def post_worker_rewards_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "create_ts", "order": "asc"}]}
        resp = dict(await self.request(self.get_url('post_worker_rewards_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('worker_rewards')

    async def post_shift_payouts_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": []}
        resp = dict(await self.request(self.get_url('post_shift_payouts_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('shift_payouts')

    async def post_worker_activity_rating_history(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [{"field": "create_ts", "order": "desc"}]}
        resp = dict(await self.request(self.get_url('post_worker_activity_rating_history'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('rating_history')

    async def post_worker_docs_list(self, worker_id: str) -> list:
        resp = await self.request(self.get_url('post_worker_docs_list'), 'POST', json={'worker_id': worker_id})
        return resp.get('documents')

    async def post_worker_payments_search(self, filters: dict = None, pagination: dict = None) -> dict:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": []}
        return dict(await self.request(self.get_url('post_worker_payments_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))

    async def post_workers_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"sort": [{"field": "create_ts", "order": "desc"}], "page_size": 5}
        resp = dict(await self.request(self.get_url('post_workers_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('workers')

    async def post_shift_history_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 20, "sort": [
                {"field": "shift_create_ts", "order": "asc"},
                {"field": "shift_id", "order": "asc"},
                {"field": "timestamp", "order": "asc"}
            ]}
        resp = dict(await self.request(self.get_url('post_shift_history_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('shifts_history')

    async def post_shift_search(self, filters: dict = None, pagination: dict = None) -> list:
        if filters is None:
            filters = {}
        if pagination is None:
            pagination = {"page_size": 10, "sort": [{"field": "start_time", "order": "desc"}]}
        resp = dict(await self.request(self.get_url('post_shift_search'), 'POST',
                                       json={'filters': filters, 'pagination': pagination}))
        return resp.get('shifts')
