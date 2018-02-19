import sys

sys.path.insert(0, 'lib')

import falcon
import falcon_jsonify

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import ndb

NUM_OF_LINKS_PER_PAGE = 10

class Link(ndb.Model):
    owner = ndb.UserProperty()
    title = ndb.StringProperty()
    url = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)

    def serialize(self):
        return {
            'title': self.title,
            'url': self.url,
            'created_at': self.created_at
         }

class HomeFeedSource(object):
    def on_get(self, req, resp):
        links = Link.query().order(-Link.created_at)\
            .fetch(NUM_OF_LINKS_PER_PAGE)
        resp.status = falcon.HTTP_200
        resp.json = [link.serialize() for link in links]

class LinkCreateSource(object):
    def on_post(self, req, resp):
        link = Link(title=req.get_json('title'), url=req.get_json('url'))
        link.put()
        resp.json ={'key': str(link.key.urlsafe())}

app = falcon.API(middleware=[
    falcon_jsonify.Middleware(help_messages=True),
])

app.add_route('/', HomeFeedSource())
app.add_route('/create/', LinkCreateSource())

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()

