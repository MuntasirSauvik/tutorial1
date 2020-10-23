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


@view_config(route_name='chatroom_remove', renderer='../templates/chats/chatroomRemove.jinja2')
def chatroom_remove(request):
    message = ''
    errors = []

    if 'form.submitted' in request.params:
        roomId = request.params['roomId']
        password1 = request.params['password1']

        # Validation
        if len(roomId.strip()) == 0 and len(password1) == 0:
            errors.append('Nothing entered')
        elif len(password1) != 0 and not request.user.check_password(password1):
            errors.append('You entered a wrong Password')
        else:
            try:
                room = request.dbsession.query(models.Chatroom.id).filter_by(id=roomId).one()
                print(room)
                room1 = request.dbsession.query(models.Chatroom).filter_by(id=roomId).one()
                request.dbsession.delete(room1)
            except NoResultFound:
                errors.append('Chatroom does not exist')

        messages = '\n'.join(errors)

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('chatroom_remove'),
    )
