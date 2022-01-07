from json import dumps as json_dumps
from flask import Response, request
from backup_service.database import one_c_bases


def set_alias_base_name() -> Response:
    """Установить Alias название базы 1С"""
    request_body = request.json
    response = Response(status=200, content_type='application/json')
    one_c_base_list = one_c_bases.OneCBases.get_all(original_name=request_body.get('original_name'))

    if not one_c_base_list:
        one_c_base = one_c_bases.OneCBases.set_or_get(**request_body)
        response.status = 201  # Отправить статус 201, запись создана
    else:
        one_c_base = one_c_base_list[-1].update(request_body)  # Берем последнюю найденную запись, меняем поля и отдаем

    response.data = json_dumps({
        'original_name': one_c_base.original_name,
        'alias_name': one_c_base.alias_name,
        'share': one_c_base.share
    })

    return response
