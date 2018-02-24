from google.appengine.ext import ndb

class User(ndb.Model):
    id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    cover = ndb.StringProperty()
    email = ndb.StringProperty()
    groups = ndb.KeyProperty(repeated=True)
    token = ndb.StringProperty()

def AddUser(user_id, first_name, cover, email, token):
    user = User(id=user_id, first_name=first_name, cover=cover, email=email, token=token)
    user.put()
    return user

def GetUser(user_id):
    user = User.query(User.id == user_id).get()
    return user

def UpdateUser(user_id, first_name, cover, email, token):
    user = User.query(User.id == user_id).get()
    if user :
        user.first_name = first_name
        user.cover = cover
        user.email = email
        user.token = token
        user.put()
    else :
        user = AddUser(user_id, first_name, cover, email, token)

    return user

def GetAllUsers() :
    users = User.query().fetch()
    return users


class Group(ndb.Model):
    id = ndb.StringProperty()
    user_id = ndb.StringProperty()
    name = ndb.StringProperty()
    is_notify_sent = ndb.BooleanProperty()
    paging_next = ndb.StringProperty()

def AddGroup(group_id, user_id, name, is_notify_sent=True, paging_next=""):
    group = Group.query(ndb.AND(Group.id == group_id, Group.user_id == user_id)).get()
    if group == None :
        group = Group(id=group_id, user_id=user_id, name=name, is_notify_sent=is_notify_sent, paging_next=paging_next)
        group.put()

        user = User.query(User.id == user_id).get()
        if user != None :
            user.groups.append(group.key)
            user.put()

    return group

def GetGroups(user_id):
    user = User.query(User.id == user_id).get()
    groups = []

    if user != None :
        groups = [group_key.get() for group_key in user.groups]

    return groups

def GetGroup(group_id, user_id) :
    group = Group.query(ndb.AND(Group.id == group_id, Group.user_id == user_id)).get()
    return group

def UpdateGroup(group_id, user_id, name):
    group = Group.query(ndb.AND(Group.id == group_id, Group.user_id == user_id)).get()
    if group == None :
        # Add only new groups
        group = AddGroup(group_id, user_id, name)
    
    return group

def UpdateGroups(user_id, groups) :
    user = User.query(User.id == user_id).get()
    if user != None :
        for group_key in user.groups :
            ndb_group = group_key.get()
            is_found = False
            for group in groups :
                if ndb_group.id == group['id'] :
                    is_found = True
                    break

            if not is_found :
                user.groups.remove(group_key)
                group_key.delete()

        user.put()
