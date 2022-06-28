'''Checks if url is live and returns the liveness,the protocol and the
   response code (statuscode) to which it responded'''
import requests


def url_is_live(url: str) -> tuple[bool, str, int]:
    '''Checks if the url is live.
       Returns a tuple, consisting of a bool indicating if the url is live,
       and a string with the protocol used (either http or https)'''
    try:
        try:
            resp = requests.get(f'https://{url}', timeout=3)
            if resp.status_code == 200:
                return True, 'https://', resp.status_code
            raise requests.exceptions.RequestException
        except requests.exceptions.RequestException as exc:
            raise requests.exceptions.RequestException from exc
    except requests.exceptions.RequestException as exc:
        try:
            resp = requests.get(f'http://{url}', timeout=3)
            if resp.status_code == 200:
                return True, 'http://', resp.status_code
            raise requests.exceptions.RequestException from exc
        except requests.exceptions.RequestException:
            pass
    return False, '', 404


if __name__ == "__main__":
    is_live, protocol, response = url_is_live('abcde.cat')
    print(
        f"'pswsm.cat' is live: {is_live}\nProtocol used: {protocol}\nStatus code: {response}")
    is_live, protocol, response = url_is_live('1898ramonroqueta.cat')
    print(
        f"'fhjfdks.cat' is live: {is_live}\nProtocol used: {protocol}\nStatus code: {response}")
