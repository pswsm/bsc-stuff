'''Checks if url is live and returns the protocol to which it responded'''
import requests

def url_is_live(url: str) -> tuple[bool, str]:
    '''Check if the url is live.
       Returns a tuple, consisting of a bool indicating if the url is live,
       and a string with the protocol used (either http or https)'''
    resp: int = 0
    try:
        try:
            resp = requests.get(f'https://{url}', timeout=3).status_code
            if resp == 200:
                return True, 'https://'
        except:
            pass
    except:
        try:
            resp = requests.get(f'http://{url}', timeout=3).status_code
            if resp == 200:
                return True, 'http://'
        except:
            pass
    return False, ''


if __name__ == "__main__":
    liveness, protocol = url_is_live('pswsm.cat')
    print(f"'pswsm.cat' is live: {liveness}\nProtocol used: {protocol}")
