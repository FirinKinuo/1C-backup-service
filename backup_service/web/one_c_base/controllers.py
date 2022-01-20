from datetime import datetime

from flask import request, render_template, jsonify, Response, g

from backup_service.filesystem import search
from backup_service.database import one_c_bases, action_logs
from backup_service.web.one_c_base import models, log


def set_alias_base_name() -> tuple[models.OneCBaseModel, int]:
    """Установить Alias название базы 1С"""
    request_body = request.json
    response_status = 200
    one_c_base_list = one_c_bases.OneCBases.get_all(original_name=request_body.get('original_name'))

    if not one_c_base_list:
        one_c_base = one_c_bases.OneCBases.set_or_get(**request_body)
        response_status = 201  # Отправить статус 201, запись создана
    else:
        one_c_base = one_c_base_list[-1].update(request_body)  # Берем последнюю найденную запись, меняем поля и отдаем

    response = models.OneCBaseModel(
        original_name=one_c_base.original_name,
        alias_name=one_c_base.alias_name,
        share=one_c_base.share
    )

    log.info(f"User {g.user['username']} "
             f"{'update' if response_status == 200 else 'add'} "
             f"alias name {one_c_base.alias_name} for base {one_c_base.original_name}")

    action_logs.ActionLogs.set(
        ip=request.remote_addr,
        user=f"{g.user['surname']} {g.user['name']}",
        type=action_logs.TYPE_CHANGE,
        date=datetime.now(),
        message=f"Обновление алиаса базы {one_c_base.original_name} на {one_c_base.alias_name}"
    )

    return response, response_status


def response_get_one_c_bases() -> Response:
    """Получить список баз 1С"""
    return jsonify(
        [models.OneCBaseModel(**(one_c_bases.OneCBases.get_last(original_name=base_name) or one_c_bases.OneCBases(
            original_name=base_name, alias_name=base_name, share=True)).__dict__).__dict__ for base_name in
         search.search_base_backup_folders()])


def response_aliases_page() -> str:
    """Получить рендер страницы списка алиасов баз 1С"""
    return render_template(template_name_or_list='aliases.html')


def update_base_share_status() -> Response:
    """Обновить статус share у базы"""
    request_body = request.json
    one_c_base_list = one_c_bases.OneCBases.get_all(original_name=request_body.get('original_name'))
    response = Response(status=200)

    if one_c_base_list:
        one_c_base_list[-1].update({'share': request_body['share']})
    else:
        one_c_bases.OneCBases.set_or_get(**request_body)
        response.status = 201

    action_logs.ActionLogs.set(
        ip=request.remote_addr,
        user=f"{g.user['surname']} {g.user['name']}",
        type=action_logs.TYPE_CHANGE,
        date=datetime.now(),
        message=f"{'Включил' if request_body['share'] else 'Выключил'} отображение базы {request_body['original_name']}"
    )

    return response
