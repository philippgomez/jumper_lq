import os
import json
import webapp2
import model
import httplib2

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


class FBConnectHandler(RestHandler) :
    def post(self) :
        r = json.loads(self.request.body)
        access_token = r['access)token']
        app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
        app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']

        # get token
        url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
          app_id, app_secret, access_token)
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        token = result.split(',')[0].split(':')[1].replace('"', '')

        # get user information
        url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email,cover' % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)
        user_id = data['id']
        name = data['name']
        email = data['email']

        # get user cover photo url
        url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
        h = httplib2.Http()
        result = h.request(url, 'GET')[1]
        data = json.loads(result)
        cover = data['data']['url']
        
        user = User.GetUser(user_id)
        if not user:
            User.AddUser(user_id, name, cover, email)

        r = UserAsDict(user)
        self.SendJson(r)


app = webapp2.WSGIApplication([
    ('/rest/user', UserHandler),
    ('/rest/group', GroupHandler),
    ('/rest/fbconnect', FBConnectHandler),
], debug=True)
