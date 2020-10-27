from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.security import (
    remember,
    forget,
    )

from .. import models


@view_config(route_name='chatroom', renderer='../templates/messages/chatroom.jinja2')
def chatroom(request):
    room = request.dbsession.query(models.Chatroom).get(request.matchdict["roomId"])
    messages = request.dbsession.query(models.Message) \
        .filter_by(room_id=room.id) \
        .order_by(models.Message.dateTime) \
        .all()
    next_url = request.params.get('next')
    if not next_url:
        next_url = request.route_url('chatroom', roomId=room.id)
    message = request.params.get('message', '')
    message = ''
    username = ''
    errors = []

    if not room.door:
        request.session.flash('Cannot enter chatroom {}, it is closed'.format(room.id))
        next_url = request.route_url('chatrooms')
        return HTTPFound(location=next_url)

    key = 'my_test_value'
    request.redis.set(key, 1, ex=100)
    print(request.redis.keys(pattern="my*"))

    if 'form.submitted' in request.params:
        message_text = request.params['message']

        # Validation
        if len(message_text.strip()) == 0:
            errors.append('Please enter a message in the box then click send.')
        else:
            new_message = models.Message()
            new_message.message_text = message_text
            new_message.creator = request.user
            new_message.room = room
            request.dbsession.add(new_message)
            request.dbsession.flush()
            messages.append(new_message)

    message = '\n'.join(errors)

    return dict(res1=room, res2=messages, next_url=next_url)


@view_config(route_name='message_remove', renderer='../templates/messages/messageRemove.jinja2')
def message_remove(request):
    message = ''
    username = ''
    errors = []

    if 'form.submitted' in request.params:
        message_id = request.params['message_id']
        password1 = request.params['password1']

        # Validation
        if len(message_id.strip()) == 0 and len(password1) == 0:
            errors.append('Nothing entered')
        elif len(password1) != 0 and not request.user.check_password(password1):
            errors.append('You entered a wrong Password')
        else:
            try:
                user_message = request.dbsession.query(models.Message.message_text).filter_by(id=message_id).one()
                print(user_message)
                message1 = request.dbsession.query(models.Message).filter_by(id=message_id).one()
                request.dbsession.delete(message1)
            except NoResultFound:
                errors.append('Message_id does not exist')

        messages = '\n'.join(errors)

    return dict(
        message=message,
        errors=errors,
        url=request.route_url('message_remove'),
        username=username,
    )
