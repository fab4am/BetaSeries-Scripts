# -*- coding: utf-8 -*-

import web, os
render = web.template.render(os.path.join(os.path.dirname(__file__), 'templates/'))

urls = (
    '/', 'index'
)

class index(object):
    def GET(self):
        name = 'Test'
        return render.index(name)

app = web.application(urls, globals())

if __name__ == '__main__':
    app.run()