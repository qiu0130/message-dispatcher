# _*_ coding: utf-8 _*_
from base import MessageDispatchChannel, pattern


class ThroughoutCallback(object):
    @staticmethod
    def username():
        return "xxx"

    @property
    def phone(self):
        return "xxx"


class Throughout(MessageDispatchChannel):
    type = "throughout"

    def send_message_to_app(self, **kwargs):
        """
        发送APP透穿消息
        :param kwargs: type->dict
        :return: None
        """
        pass

    def dispatch(self, **kwargs):
        result = dict()
        for payload_name in self.payload.payload_field:
            payload = getattr(self.payload, payload_name)

            matched_pattern = pattern.findall(payload)
            for m in matched_pattern:
                callback = getattr(ThroughoutCallback, m.strip("{{ ").strip(" }}"))
                callback_result = callback(**kwargs)
                payload = payload.replace(m, callback_result)
            result[payload_name] = payload
        self.send_message_to_app(**result)