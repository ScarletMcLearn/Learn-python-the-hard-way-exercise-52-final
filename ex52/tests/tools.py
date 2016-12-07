from nose.tools import *
import re

def assert_response(resp,contains=None,matches = None,headers = None,status="200"):
    assert status in resp.status,"Expected response %r not in %r"%(status,resp.status)

    #if status =="200":
        #assert resp.data,"Response data is empty"

    if contains:
        assert contains in resp.data,"Response does not contain %r"%contains

    if matches:
        reg = re.compile(matches)
        assert reg.matches(resp.data),"Response does not match %r"%matches

    if headers:
        assert_equal(resp.headers, headers)


# header contains session variable address. sent as cookie
def get_session_id(resp):
    cookies_str = resp.headers['Set-Cookie']
    if cookies_str:
        for kv in cookies_str.split(';'):
            if 'webpy_session_id=' in kv:
                return kv

