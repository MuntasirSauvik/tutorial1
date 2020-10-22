from sqlalchemy.orm.exc import NoResultFound
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .. import models


@view_config(route_name='chatroom_list', renderer='../templates/chats/chatroomList.jinja2')
def chatroom_list(request):
    res = request.dbsession.query(models.Chatroom).all()
    return dict(res=res)
