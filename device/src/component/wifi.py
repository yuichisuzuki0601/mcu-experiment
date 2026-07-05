from network import WLAN, STA_IF, STAT_IDLE, STAT_GOT_IP, AP_IF
from utime import sleep

import asyncio

from lib import aiohttp
from util import timestamp

class Wifi:
    CONNECT_MAX_WAIT_S = 10 #[s]
    REQUEST_TIMEOUT_S  =  3 #[s]
    UA                 = 'mcu'

    def __init__(self, ssid: str, password: str):
        self.ssid = ssid
        self.password = password
        print(f'wifi setting: ssid = {ssid}, password = {password}')

    def connect(self):
        self.wlan = WLAN(STA_IF)
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)

        max_wait_s = Wifi.CONNECT_MAX_WAIT_S
        while max_wait_s > 0:
            if self.wlan.status() < STAT_IDLE or self.wlan.status() >= STAT_GOT_IP:
                break
            max_wait_s -= 1
            print('waiting for wifi connection...')
            sleep(1)

        if self.wlan.status() == STAT_GOT_IP:
            status = self.wlan.ifconfig()
            print(f'wifi connected: ip = {status[0]}')
            timestamp.sync_time()
        else:
            raise Exception('ERR: wifi connection failed.')

        return self

    def is_connected(self):
        return self.wlan.isconnected()

    def launch_as_access_point(self):
        wlan = WLAN(AP_IF)
        wlan.config(essid = self.ssid, password = self.password)
        wlan.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '192.168.4.1'))  
        wlan.active(True)
        print('\nIP Address: {}\nNet Mask: {}\nGateway: {}\nDNS: {}\n'.format(*wlan.ifconfig()))

    def _request(self, method: str, url: str, req_headers: dict, req_body: dict, on_success, on_error):
        print(f'{method} {url} {timestamp.get_jst_datetime()}')
        headers = req_headers.copy() if req_headers else {}
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('User-Agent', Wifi.UA)
        async def task():
            try:
                # TODO 200じゃなかった時にon_errorに飛ばしてステータスも渡したい。
                async with aiohttp.ClientSession() as session:
                    func = getattr(session, method.lower())
                    kwargs = {'headers': headers}
                    if req_body is not None:
                        kwargs['json'] = req_body
                    ctx = func(url, **kwargs)
                    try:
                        response = await asyncio.wait_for(ctx.__aenter__(), timeout = Wifi.REQUEST_TIMEOUT_S)
                        print(response.status)
                    except asyncio.TimeoutError:
                        raise Exception(f'ERR: Connection timed out after {Wifi.REQUEST_TIMEOUT_S}s')
                    try:
                        res_status = response.status
                        res_headers = response.headers
                        res_body = await response.text()
                        on_success(res_status, res_headers, res_body)
                    finally:
                        await ctx.__aexit__(None, None, None)
            except Exception as e:
                on_error(e)
        asyncio.create_task(task())

    def _noop(_): pass

    def get(self, url: str, on_success, req_headers: dict = None, on_error = _noop):
        self._request('GET', url, req_headers, None, on_success, on_error)

    def post(self, url: str, on_success, req_headers: dict = None, req_body: dict = None, on_error = _noop):
        self._request('POST', url, req_headers, req_body, on_success, on_error)

    def put(self, url: str, on_success, req_headers: dict = None, req_body: dict = None, on_error = _noop):
        self._request('PUT', url, req_headers, req_body, on_success, on_error)

    def delete(self, url: str, on_success, req_headers: dict = None, on_error = _noop):
        self._request('DELETE', url, req_headers, None, on_success, on_error)
