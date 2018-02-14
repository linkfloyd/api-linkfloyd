from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

from google.appengine.ext import ndb
from google.appengine.ext import db
import cgi
app = FlaskAPI(__name__)
NUM_OF_LINKS_PER_PAGE = 20

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


@app.route("/", methods=['GET', 'POST'])
def links_list():
    links = Link.query().order(-Link.created_at).fetch(NUM_OF_LINKS_PER_PAGE)
    return [link.serialize() for link in links]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def link_detail(key):
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    if key not in notes:
        raise exceptions.NotFound()
    return note_repr(key)


@app.route("/create/", methods=['GET', 'POST'])
def link_create():
    if request.method == 'POST':
        link = Link(title=request.data.get('title'),
                    url=request.data.get('url'))
        link.put()
        return {'key': str(link.key.urlsafe())}
    return {}



if __name__ == "__main__":
    app.run(debug=True)
