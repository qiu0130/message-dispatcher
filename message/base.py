#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import logging
from collections import namedtuple

logger = logging.getLogger("Message")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

pattern = re.compile("{{ \w+ }}", re.I)


class MessageDispatchChannel(object):

    type = None

    def __init__(self, name, target, **payload_dict):
        self.name = name
        self.target = target
        self.payload = MessagePayload.initialize(
            name=name,
            **payload_dict
        )

    def dispatch(self, **kwargs):
        raise NotImplementedError

    def __repr__(self, type_name=None):
        if type_name is None:
            type_name = self.__class__.__name__
        repr_obj = namedtuple(
            typename=type_name,
            field_names=[
                "name",
                "target",
                "payload"
            ]
        )
        return repr_obj(
            name=self.name,
            target=self.target,
            payload=self.payload.__repr__()
        ).__repr__()


class MessagePayload(object):

    def __init__(self):
        self.name = None
        self.payload_field = set()

    @classmethod
    def initialize(cls, name, **payload_dict):
        inst = cls()
        inst.name = name
        inst.payload_field = set()
        for payload_name, payload_value in payload_dict.items():
            if hasattr(inst, payload_name):
                logging.warning(
                    (
                        "Payload <{}> has been existed on Message <{}>"
                        .format(payload_name, inst.name)
                    )
                )
            setattr(inst, payload_name, payload_value)
            inst.payload_field.add(payload_name)

        return inst

    def __repr__(self, type_name=None):
        if type_name is None:
            type_name = self.__class__.__name__

        repr_obj = namedtuple(
            typename=type_name,
            field_names=[
                payload_name for payload_name in self.payload_field
            ]
        )
        return repr_obj(
            **{
                payload_name: getattr(self, payload_name) for payload_name in self.payload_field
            }
        ).__repr__()

