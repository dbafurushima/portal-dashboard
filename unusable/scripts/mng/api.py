import asyncio
import aiohttp
import ujson
from .helper.log import app_log
from .helper.formatting import format_text, format_dict2str
from .model import ApiConfig


class MNGApi:
    """API for main functions of the CLI tool
    """

    def __init__(self):
        self._api_conf = ApiConfig()
    
    def __assert_valid_repo(self):
        """Checks if config file is valid
        """
        self._api_conf.conf.validate()

    def init(self) -> dict:
        """initializes tool settings such as access credentials and basic information if one does not exist
        Returns:
            dict: [result and config file]
        """
        initialized = True
        if self._api_conf.conf.validate(throw=False):
            app_log.info("ferramenta já inicializada.")
        else:
            app_log.info("iniciando configurações da ferramenta...")
            initialized = self._api_conf.init()
            if initialized:
                app_log.info("ferramenta iniciada e pronto para uso.")
            else:
                app_log.error("falha ao iniciar ferramenta.")
        return {'initialized': initialized, 'conf': self._api_conf.conf}
    
    def configure(self)-> dict:
        """configure or update information in the API configuration file
        Returns:
            dict: [boolean result]
        """
        self.__assert_valid_repo()
        # configure a challenge
        configured = self._api_conf.configure()
        if configured:
            app_log.info("arquivo configurado com sucesso.")
        else:
            app_log.error("falha na configuração.")
        return {'configured': configured}
    
    async def post_json(self, suffix_url: str, data_json: dict) -> dict:
        """asynchronous post request with content type and json response
        Args:
            suffix_url (str): [path url for request]
            data_json (dict): [data json]
        Returns:
            dict: [data response]
        """
        url = 'http://%s:%s%s' % (self._api_conf.conf.ip, self._api_conf.conf.port, suffix_url)
        # url = f'http://{self._api_conf.conf.ip}:{self._api_conf.conf.port}{suffix_url}'
        headers = {'Authorization': 'Basic %s' % self._api_conf.conf.base64auth,
        'Content-Type': 'application/json'}

        app_log.debug('post in %s' % url)
        app_log.debug('headers requests %s' % headers)

        try:
            async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                response = await session.post(url, json=data_json, headers=headers)
            return await response.json()
        except (ConnectionRefusedError, aiohttp.client_exceptions.ClientConnectorError):
            print('[!] não foi possível se conectar com o servidor.')
        except asyncio.exceptions.TimeoutError:
            print('[!] timeout response.')
        except aiohttp.client_exceptions.ContentTypeError:
            print('[!] o corpo da requisição não está em JSON, algo pode está errado.')
        return {}

    async def put_json(self, suffix_url: str, data_json: dict) -> dict:
        """asynchronous put request with content type and json response
        Args:
            suffix_url (str): [path url for request]
            data_json (dict): [data json]
        Returns:
            dict: [data response]
        """
        url = 'http://%s:%s%s' % (self._api_conf.conf.ip, self._api_conf.conf.port, suffix_url)
        headers = {'Authorization': 'Basic %s' % self._api_conf.conf.base64auth,
        'Content-Type': 'application/json'}

        app_log.debug('post in %s' % url)
        app_log.debug('headers requests %s' % headers)

        try:
            async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
                response = await session.put(url, json=data_json, headers=headers)
            return await response.json()
        except (ConnectionRefusedError, aiohttp.client_exceptions.ClientConnectorError):
            print('[!] não foi possível se conectar com o servidor.')
        except asyncio.exceptions.TimeoutError:
            print('[!] timeout response.')
        except aiohttp.client_exceptions.ContentTypeError:
            print('[!] o corpo da requisição não está em JSON, algo pode está errado.')
        return {}

    async def get_json(self, suffix_url: str, params=None) -> dict:
        """get post request with json response
        Args:
            suffix_url (str): [path url]
            params (list, optional): [params for request]. Defaults to None:listorNone.
        Returns:
            dict: [data response]
        """
        url = 'http://%s:%s%s' % (self._api_conf.conf.ip, self._api_conf.conf.port, suffix_url)
        headers = {'Authorization': 'Basic %s' % self._api_conf.conf.base64auth,
        'Content-Type': 'application/json'}

        app_log.debug('post in %s' % url)

        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(url, params=params, headers=headers)
            return await response.json()
        except (ConnectionRefusedError, aiohttp.client_exceptions.ClientConnectorError):
            print('[!] não foi possível se conectar com o servidor')
        except asyncio.exceptions.TimeoutError:
            print('[!] timeout response.')
        except aiohttp.client_exceptions.ContentTypeError:
            print('[!] o corpo da requisição não está em JSON, algo pode está errado.')
        return {}
