# -*- coding: UTF-8 -*-

import re


def _rec_update_dict(base_dict, overlay_dict):
    for k, v in overlay_dict.iteritems():
        if isinstance(v, dict):
            old_v = base_dict.get(k)
            if isinstance(old_v, dict):
                _rec_update_dict(old_v, v)
            else:
                base_dict[k] = {}
                _rec_update_dict(base_dict[k], v)
        elif isinstance(v, list):
            if k in base_dict:
                base_dict[k].extend(v)
            else:
                base_dict[k] = v
        else:
            base_dict[k].append(v)


def extract_number_and_context_from_extension(extension, default_context='default'):
    if re.search('@', extension):
        exten = extension.split('@')
        number = exten[0]
        context = exten[1]
        ret = (number, context)
    else:
        ret = (extension, default_context)
    return ret
