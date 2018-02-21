import os
import json
import webapp2
import model


def UserAsDict(user):
    return {'user_id': user.key.id(), 'cover' : user.cover, 'first_name': user.first_name, 'email': user.email, 'groups' : user.groups}

def GroupAsDict(group):
    return {'group_id': group.key.id(), 'name' : group.name, 'icon' : group.icon, 'is_sending_notify' : group.is_sending_notify}

class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))

class UserHandler(RestHandler):

    def get(self):
        users = model.AllUsers()
        r = [UserAsDict(user) for user in users]
        self.SendJson(r)

    def post(self):
        r = json.loads(self.request.body)
        user = model.AddUser(r['user_id'], r['first_name'], r['cover'], r['email'])
        r = UserAsDict(user)
        self.SendJson(r)

class GroupHandler(RestHandler):

    def get(self):
        groups = model.GetGroups()
        r = [UserAsDict(group) for group in groups]
        self.SendJson(r)

    def post(self):
        r = json.loads(self.request.body)
        group = model.AddGroup(r['group_id'], r['user_id'], r['name'], r['icon'])
        r = GroupAsDict(group)
        self.SendJson(r)


app = webapp2.WSGIApplication([
    ('/rest/user', UserHandler),
    ('/rest/group', GroupHandler),
], debug=True)
