from google.appengine.ext import ndb

class User(ndb.Model):
    id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    cover = ndb.StringProperty()
    email = ndb.StringProperty()
    groups = ndb.KeyProperty(repeated=True)

def AddUser(user_id, first_name, cover, email):
    user = User(id=user_id, first_name=first_name, cover=cover, email=email)
    user.put()
    return user

def GetUser(user_id):
    user = User.query(User.id == user_id).get()
    return user


class Group(ndb.Model):
    id = ndb.StringProperty()
    name = ndb.StringProperty()
    icon = ndb.StringProperty()
    is_notify_sent = ndb.BooleanProperty()

def AddGroup(group_id, user_id, name, icon, is_notify_sent=True):

    group = Group(id=group_id, user_id=user_id, name=name, icon=icon, is_notify_sent=is_notify_sent)
    group.put()

    user = User.query(User.id == user_id).get()
    if user:
        user.groups.append(group.key)

    return group

def GetGroups(user_id):
    user = User.query(User.id == user_id).get()
    groups = []

    for group_key in user.groups:
        group = group_key.get()
        groups.append(group)

    return groups

