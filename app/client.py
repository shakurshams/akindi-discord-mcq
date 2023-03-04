from requests import Request, Session


class Client:
    def __init__(self, method, url, headers, data={}):
        req = Request(method.upper(), url, headers=headers, data=data)

        self.session = Session()
        self.request = self.session.prepare_request(req)

    def make_request(self, stream=None, verify=True, proxies=None, cert=None):
        settings = self.session.merge_environment_settings(
            self.request.url, stream=stream, verify=verify, proxies=proxies, cert=cert
        )
        response = self.session.send(self.request, **settings)

        response.raise_for_status()

        return response.status_code, response.json() if response.text else None
