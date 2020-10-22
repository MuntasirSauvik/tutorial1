from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .. import models


@view_config(route_name='chatroom_list', renderer='../templates/chats/chatroomList.jinja2')
def chatroom_list(request):
    res = request.dbsession.query(models.Chatroom).all()
    return dict(res=res)


@view_config(route_name='chatroom_add', renderer='../templates/chats/chatroomAdd.jinja2')
def chatroom_add(request):
    message = ''
    roomDescription = ''
    door = False
    errors = []

    if 'form.submitted' in request.params:
        roomDescription = request.params['roomDescription']
        if request.params['door'] == "False":
            door = False
        elif request.params['door'] == "True":
            door = True

        # Validation
        if len(roomDescription.strip()) == 0:
            errors.append('Room Description cannot be blank')
        if len(roomDescription.strip()) > 64:
            errors.append('Please Enter a shorter Room Description')

        if not len(errors):
            # Add object to database
            new_room = models.Chatroom()
            new_room.roomDescription = roomDescription
            new_room.door = door
            request.dbsession.add(new_room)
            try:
                request.dbsession.flush()
                return HTTPFound(location=request.route_url('editor_page'))
            except IntegrityError:
                errors.append('Username already exists')

        message = 'Try Again'

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('chatroom_add'),
        )