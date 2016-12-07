from nose.tools import *
from bin.app import app
from tests.tools import assert_response,get_session_id
import base64
import pickle



# Sorry, the tests are a mess due to constant updating and refactoring

# Globvars
##########################################
cookie = None
##########################################



# Defining function to Check each room
#######################################################################
def checkstuff(action,contains):
    global cookie
    resp = app.request("/game",method = "POST",headers = {'Cookie':cookie},data = {'action':action})
    assert_response(resp,status = "303")
    cookie = get_session_id(resp)
    # GET
    resp = app.request("/game",headers = {'Cookie':cookie},method = "GET")
    assert_response(resp,status = "200",contains = contains)
    cookie = get_session_id(resp)
######################################################################




# Checks the log in page
def test_index():
    global cookie
    resp = app.request('/',method = "GET")
    assert_response(resp,status = '200',contains = "Please provide log in information")
    cookie = get_session_id(resp)

    resp = app.request('/',method = "POST",headers = {'Cookie':cookie},data = {'username':'user5','password':'password1'})
    assert_response(resp,contains = "User does not exist")
    resp = app.request('/',method = "POST",headers = {'Cookie':cookie},data = {'username':'user2','password':'password1'})
    assert_response(resp,contains = "Wrong password")
    resp = app.request('/',method = "POST",headers = {'Cookie':cookie},data = {'username':'user1','password':'password1'})
    assert_response(resp,status = '303')
    cookie = get_session_id(resp)

    pass
######################################################################

# testing map chooser
######################################################################
def test_map_chooser():
    global cookie
    resp = app.request("/load",method = "GET",headers = {'Cookie':cookie} )
    assert_response(resp,contains = "List of available games are:",status = "200")
    cookie = get_session_id(resp)
    resp = app.request("/load",method = "POST", data = {'mapname':"Gothonweb"},headers = {'Cookie':cookie})
    assert_response(resp,status = "303")
    cookie = get_session_id(resp)
######################################################################


######################################################################
def test_game():
    global cookie

    # check empty session
    resp = app.request("/game")
    assert_response(resp,contains ="Error!",status = "200")

    # check initial get
    resp = app.request("/game",headers = {'Cookie':cookie})
    assert_response(resp,contains = "Central Corridor",status = "200")
    cookie = get_session_id(resp)


    # Using the method we built to check rooms
    checkstuff("tell a joke","Laser Weapon Armory")
    x = base64.b64decode(open("sessions/{}".format(cookie[17::]),'r').read())
    x = pickle.loads(x)
    # ^ This gets the rand value of laser_weapon_armory from session variable using cookie
    # Then decodes and unpickles using base64 and pickle
    checkstuff("45","Laser Weapon Armory")
    # ^Checking with a mistake to see if it returns the same room
    checkstuff(x['rand'],"The Bridge")
    # ^ Checking with the rand value which should be the solution and return the bridge
    checkstuff("slowly place the bomb","Escape Pod")
    checkstuff(x['rand'],"The End")
    del cookie

    ## Initializing another cookie because writing cookie2 = cookie will return the same cookie since address
    resp = app.request('/',method = "POST",data = {'username':'user1','password':'password1'})
    cookie = get_session_id(resp)
    resp = app.request("/load",headers = {'Cookie':cookie},method = "POST", data = {'mapname':"Gothonweb"})
    assert_response(resp,status = "303")
    cookie2 = get_session_id(resp)


    # Checking Screwup input
    resp2 = app.request("/game",headers = {'Cookie':cookie2}, method = "POST", data = {'action':'dgsdg'})
    assert_response(resp2,status = "303")
    cookie2 = get_session_id(resp2)

    resp2 = app.request("/game",headers = {'Cookie':cookie2},method = "GET")
    assert_response(resp2,status = "200",contains = "Death")
    del cookie2
######################################################################

























