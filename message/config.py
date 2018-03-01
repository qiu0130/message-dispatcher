# _*_ coding: utf-8 _*_

from types import SimpleNamespace

import yaml
import simplejson as json


def config(fp, is_dict=False):

    with open(fp, encoding="utf-8") as file_handler:
        content = yaml.safe_load(file_handler)
        if is_dict:
            res = json.loads(
                json.dumps(content))
        else:
            res = json.loads(
                json.dumps(content),
                object_hook=lambda d: SimpleNamespace(**d))
    return res
