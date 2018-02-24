import os
import json
import webapp2
import model
import httplib
from google.appengine.api import mail

def UserAsDict(user):
    groups = [group_key.get().id for group_key in user.groups]
    return {'user_id': str(user.id), 'cover' : user.cover, 'first_name': user.first_name, 'email': user.email, 'groups' : groups}

def GroupAsDict(group):
    return {'group_id': str(group.id), 'name' : group.name, 'is_notify_sent' : group.is_notify_sent, 'paging_next' : group.paging_next}


class RestHandler(webapp2.RequestHandler):

    def dispatch(self):
        super(RestHandler, self).dispatch()

    def SendJson(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(r))

    def Send(self, r):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(r)

class UserHandler(RestHandler):

    def post(self):
        r = json.loads(self.request.body)
        user_id = r['user_id']
        r = { } 
        if user_id != None :
            user = model.GetUser(user_id)
            if user != None :
                r = UserAsDict(user)

        self.SendJson(r)


class GroupHandler(RestHandler):

    def post(self):
        r = json.loads(self.request.body)
        user_id = r['user_id']

        user = model.GetUser(user_id)
        
        conn = httplib.HTTPSConnection("graph.facebook.com")
        url = '/v2.12/%s/groups?access_token=%s' % (user_id, user.token)
        conn.request("GET", url)
        result = conn.getresponse().read()
        data = json.loads(result)
        
        groups = model.GetGroups(user_id)
        if len(groups) == 0 :
            for group in data['data'] :
               model.AddGroup(group['id'], user_id, group['name'])
        else :
            model.UpdateGroups(user_id, data['data'])
            for group in data['data'] :
               model.UpdateGroup(group['id'], user_id, group['name'])

        groups = model.GetGroups(user_id)
        r = [GroupAsDict(group) for group in groups]

        self.SendJson(r)


class FBConnectHandler(RestHandler) :

    def post(self) :
        r = json.loads(self.request.body)
        access_token = r['access_token']
        app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
        app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']

        # get token
        conn = httplib.HTTPSConnection("graph.facebook.com")
        url = '/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
          app_id, app_secret, access_token)
        conn.request("GET", url)
        result = conn.getresponse().read()
        token = result.split(',')[0].split(':')[1].replace('"', '')

        # get user information
        url = '/v2.12/me?access_token=%s&fields=first_name,id,email,cover' % token
        conn.request("GET", url)
        result = conn.getresponse().read()
        data = json.loads(result)
        user_id = data['id']
        name = data['first_name']
        email = data['email']

        # get user cover photo url
        url = '/v2.12/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
        conn.request("GET", url)
        result = conn.getresponse().read()
        data = json.loads(result)
        cover = data['data']['url']
        
        user = model.GetUser(user_id)
        if not user:
            user = model.AddUser(user_id, name, cover, email, token)
        else :
            user = model.UpdateUser(user_id, name, cover, email, token)

        r = UserAsDict(user)
        self.SendJson(r)


class WebhookHandler(RestHandler) :
    def post(self):
        self.SendJson({ })

    def get(self) :
        r = ""
        challenge = self.request.get("hub.challenge")
        verify_token = self.request.get("hub.verify_token")
        if verify_token == "JumperLQ" :
              r = challenge

        self.Send(r)

class GroupPollHandler(RestHandler) :
    def get(self):
        r = { }
        users = model.GetAllUsers()
        for user in users :
            r[user.first_name] = { }
            for group_key in user.groups :
                group = group_key.get()
                r[user.first_name][group.name] = { }
                if group.is_notify_sent == True :
                    notification = get_group_feed(group, user)
                    r[user.first_name][group.name]['notification'] = notification
                    if len(notification) > 0 :
                        send_notification(user, group, json.dumps(notification))

        return self.SendJson(r)

def get_group_feed(group, user) :
    #r = {}
    r = []

    conn = httplib.HTTPSConnection("graph.facebook.com")
    if group.paging_next != None and group.paging_next != "" :
        url = group.paging_next
    else :
        url = '/%s/feed?access_token=%s' % (group.id, user.token)
    
    #r['url'] = url
    conn.request("GET", url)
    res = conn.getresponse()
    if res != None :
        result = res.read()
        data = json.loads(result)
        #r['data'] = data['data']
        r = data['data']

        if len(data['data']) > 0 and data.has_key('paging') :
            if data['paging'].has_key('next') :
                paging_next = data['paging']['next']
                group.paging_next = paging_next[len("https://graph.facebook.com"):-1]
                group.put()

    return r

def send_notification(user, group, notification) :
    mail.send_mail(sender='mkchaz@gmail.com',
                   to=user.first_name + ' <' + user.email + '>',
                   subject='Notification: New item(s) in ' + group.name + ' feed',
                   body=notification)

app = webapp2.WSGIApplication([
    ('/rest/user', UserHandler),
    ('/rest/group', GroupHandler),
    ('/rest/fbconnect', FBConnectHandler),
    ('/webhook', WebhookHandler),
    ('/tasks/grouppoll', GroupPollHandler)
], debug=True)
