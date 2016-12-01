import pecan
from pecan import conf
from pecan import expose, redirect
from webob.exc import status_map

from pecan_model2.model import Session, MetaData
from pecan_model2.model.user import User


class RootController(object):
    @expose(generic=True, template='json')
    def index(self):
        query = Session.query(User)
        users = query.all()
        names = [user.name for user in users]
        return {"users": users}

    @expose('json')
    @index.when(method='POST')
    def index_post(self):
        username = pecan.request.POST.get('username')
        password = pecan.request.POST.get('password')
        email = pecan.request.POST.get('email')

        user = User()
        user.name = username
        user.password = password
        if email:
            user.email = email
        Session.add(user)
        return {"message": "OKKKKK"}

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
