from xivo_lettuce.remote_py_cmd import remote_exec, remote_exec_with_result
from xivo_lettuce.manager_dao import voicemail_manager_dao


def delete_voicemail_with_id(voicemail_id):
    remote_exec(_delete_voicemail_with_id, voicemail_id=voicemail_id)


def _delete_voicemail_with_id(channel, voicemail_id):
    from xivo_dao.data_handler.voicemail import services
    from xivo_dao.data_handler.exception import ElementNotExistsError

    try:
        voicemail = services.get(voicemail_id)
        services.delete(voicemail)
    except ElementNotExistsError:
        pass


def find_voicemail_id_with_number(number, context='default'):
    return remote_exec_with_result(_find_voicemail_id_with_number, number=number, context=context)


def _find_voicemail_id_with_number(channel, number, context):
    from xivo_dao.data_handler.voicemail import services
    from xivo_dao.data_handler.exception import ElementNotExistsError

    try:
        voicemail = services.get_by_number_context(number, context)
        channel.send(voicemail.id)
    except ElementNotExistsError:
        channel.send(None)


def add_or_replace_voicemail(parameters):
    _delete_voicemail(parameters)
    voicemail_manager_dao.create_voicemail(parameters)


def _delete_voicemail(parameters):
    if 'number' in parameters:
        number = parameters['number']
        context = parameters.get('context', 'default')
        voicemail_id = find_voicemail_id_with_number(number, context)
        if voicemail_id:
            delete_voicemail_with_id(voicemail_id)
