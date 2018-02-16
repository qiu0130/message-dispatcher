# _*_ coding: utf-8 _*_
from collections import namedtuple

from config import config
from handler.sms import Sms, SmsCallback
from handler.mail import Mail, MailCallback
from handler.throughout import Throughout, ThroughoutCallback
from base import MessageDispatchChannel


class MessageDispatcher(object):

    handlers = {
        "throughout": Throughout,  # app透传消息
        "mail": Mail,
        "sms": Sms                 # 手机短信
    }
    callbacks = {
        "throughout": ThroughoutCallback(),
        "mail": MailCallback(),
        "sms": SmsCallback()
    }

    def __init__(self):
        self.code = None
        self.name = None
        self.channel = None

    def extract_message(self, code=None, is_dict=False):
        target_message = config(fp="./message.yaml", is_dict=is_dict)
        if code is None:
            code = self.code

        return target_message.get(code)

    @classmethod
    def initialize(cls, code):
        inst = cls()
        current_message = inst.extract_message(code=code, is_dict=True)

        inst.code = code
        inst.name = current_message.get("name")
        channel = current_message.get("type")
        inst.channel = list()

        for channel_type, payload_dict in channel.items():
            channel_class = inst.handlers.get(channel_type)
            if channel_class is None:
                return inst
            target = payload_dict.pop("target")
            if target:
                target = getattr(inst.callbacks.get(channel_type), target.strip("{{ ").strip(" }}"))

            inst.channel.append(
                channel_class(name=inst.name,
                              target=target,
                              **payload_dict
                              )
            )

        if inst.channel.__len__() == 1:
            inst.channel = inst.channel.pop(0)
        elif inst.channel.__len__() == 0:
            inst.channel = None
        return inst

    def dispatch(self, **kwargs):
        if isinstance(self.channel, MessageDispatchChannel):
            self.channel.dispatch(**kwargs)
        elif isinstance(self.channel, list):
            for channel in self.channel:
                if isinstance(channel, MessageDispatchChannel):
                    channel.dispatch(**kwargs)
                else:
                    raise TypeError("Channel must be MessageDispatchChannel")
        else:
            raise TypeError("Channel must be MessageDispatchChannel")

    def __repr__(self, type_name=None):
        if type_name is None:
            type_name = self.__class__.__name__

        repr_obj = namedtuple(
            typename=type_name,
            field_names=[
                "code",
                "name",
                "channel"
            ]
        )
        if isinstance(self.channel, list):
            channel_repr = [channel.__repr__() for channel in self.channel]
        elif isinstance(self.channel, MessageDispatchChannel):
            channel_repr = self.channel.__repr__()
        else:
            raise TypeError("Channel must be MessageDispatchChannel")

        return repr_obj(
            code=self.code,
            name=self.name,
            channel=channel_repr
        ).__repr__()

if __name__ == "__main__":
    message = MessageDispatcher.initialize(code="A")
    print(message.dispatch())
