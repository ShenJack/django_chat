import json
import logging

from channels import Group
from channels.auth import channel_session_user, channel_and_http_session_user_from_http
from channels.sessions import channel_session, http_session, channel_and_http_session
from django.utils import timezone

from chat_core.models import Room

log = logging.getLogger(__name__)


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    print("connected")
    try:
        prefix, label = message['path'].strip('/').split('/')
        if prefix != 'room':
            log.debug('invalid ws path=%s', message['path'])
            return
        room = Room.objects.get(label=label)
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    except Room.DoesNotExist:
        log.debug('ws room does not exist label=%s', label)
        return

    log.debug('chat connect room=%s client=%s:%s',
              room.label, message['client'][0], message['client'][1])

    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('chat-', channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room.label


@channel_and_http_session_user_from_http
def ws_receive(message):
    room = Room.objects.get(label=message.channel_session['room'])
    room.updateTime = timezone.now()
    room.save()
    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return



    if data:
        log.debug('chat message room=%s handle=%s message=%s',
                  room.label, data['handle'], data['message'])
        m = room.messages.create(**data)
        # m.handle = message.http_session['username']

        # See above for the note about Group
        Group('chat-', channel_layer=message.channel_layer).send({'text': json.dumps(m.as_dict())})


@channel_session
def ws_disconnect(message):
    try:
        label = message.channel_session['room']
        room = Room.objects.get(label=label)
        Group('chat-', channel_layer=message.channel_layer).discard(message.reply_channel)
    except (KeyError, Room.DoesNotExist):
        pass
