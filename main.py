from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime
import models

class MainPage(webapp.RequestHandler):
    def get(self):
        time = datetime.datetime.now()
        user = users.get_current_user()
        if not user:
            navbar = ('<h1 align="center">Personalised Clock</h1><p  align="center"><image src="/images/customLogo.jpg" width="200" hspace="10"></p><p align="center"><a href="%s">Sign in or register</a> with <img src="/images/google.jpg" alt="Google"/> to customise your time zone.</p>'
                      % (users.create_login_url(self.request.path)))
            tz_form = ''
        else:
            userprefs = models.get_userprefs()
            navbar = ('<p  align="center">Welcome, %s! - <a href="%s">Sign out</a>.</p>'
                      % (user.nickname(), users.create_logout_url(self.request.path)))
            tz_form = '''
            <div align="center">
                <form action="/prefs" method="post">
                    <label for="tz_offset">
                        Timezone offset from UTC (can be negative):
                    </label>
                    <input name="tz_offset" id="tz_offset" type="text"
                        size="4" value="%d" />
                    <input type="submit" value="Set" />
                </form></div>
            ''' % userprefs.tz_offset
            time += datetime.timedelta(0, 0, 0, 0, 0, userprefs.tz_offset)
            
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('''
        <html>
            <head>
                <title>The Time Is...</title>
            </head>
            <body>
            
            <p align="center">%s</p>
                <font color="blue"><h1  align="center">The time is: %s</h1></font>
            <p  align="center">%s</p>
            <p align="center">Proudly brought to you by Jared Blyth</p><p align="center"><a href="http://jaredblyth.com" title="Visit website of the creator of this clock" target="_blank"><img border="none" src="http://jaredblyth.com/img/design/header/header-image.jpg" alt="Headshot"/></a></p><p align="center">Visit <a href="http://jaredblyth.com" title="Visit website of the creator of this clock" target="_blank">jaredblyth.com</a></p>
            </body>
        </html>
        ''' % (navbar, str(time), tz_form))

application = webapp.WSGIApplication([('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)
    
if __name__ == '__main__':
    main()
