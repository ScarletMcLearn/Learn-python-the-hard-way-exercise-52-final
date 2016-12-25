import web
import map

web.config.debug = True
urls = (
        '/','Login',
        '/load','Index',
        '/game','GameEngine',
        )
###################################################
game_list = {"Gothonweb":map,"Errorgame":None}
app = web.application(urls,globals())
allowed = {'user1':'password1','user2':'password2'}
###################################################


#little hack so that debug mode works with sessions
if web.config.get('_session') is None:
    store = web.session.DiskStore('sessions')
    # rand as a session variable is only used for tests
    session = web.session.Session(app,store,initializer = {'room':None,
        'rand':None,
        'logged_in':False,
        })
    web.config._session = session

else:
    session = web.config._session

render = web.template.render('templates/',base = "layout")

###################################################
class Login(object):
    def GET(self):
        return render.log_in()

    def POST(self):
        username = web.input().username
        password = web.input().password

        if username in allowed.keys():
            if allowed[username] == password:
                session.logged_in = True
                web.seeother('/load')
            else:
                return "Wrong password"
        else:
            return "User does not exist"



###################################################

###################################################
class Index(object):
    def GET(self):
        if session.logged_in:
            return render.roomchooser(game_list = game_list)
        else:
            return "You must log in first"
    def POST(self):
        map = web.input().mapname.capitalize()
        # this is use to setup the session with starting values
        if session.logged_in:
            if map in game_list:
                # Reload module to reset room.count and rands inside map module
                game_list[map] = reload(game_list[map])
                # Rand for testing
                session.rand = game_list[map].RAND1
                session.rand2 = game_list[map].RAND2
                session.room = game_list[map].START
                web.seeother("/game")
            else:
                return render.you_died()
        else:
            return "Logged in somehow got deleted"
###################################################

######################################################
class GameEngine(object):
    def GET(self):
        if session.room:
            if session.room.name == "The End" or session.room.name == "Death":
                session.kill()
            return render.show_room(room=session.room)
        else:
            # returns this if your input is not found
            return render.you_died()
##
    def POST(self):
        form = web.input(action = None)

        # There is a bug here, can you fix it? (bug fixed. Bug was how end room had an action box too.)
        # Fixed bug in show_room.html
        if session.room  and form.action:
            session.room = session.room.go(form.action)

        web.seeother("/game")
########################################################



if __name__ == "__main__":
    app.run()


