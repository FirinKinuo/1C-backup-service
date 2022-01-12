from flask import request, render_template, jsonify, Response

from backup_service.filesystem import search
from backup_service.database import one_c_bases
from backup_service.web.one_c_base import models


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

    return response, response_status


def response_get_one_c_bases_name_list() -> Response:
    """Получить список имен баз 1С"""
    return jsonify([models.OneCBaseNames(
        original_name=base_name,
        alias_name=(one_c_bases.OneCBases.get_last(original_name=base_name) or one_c_bases.OneCBases(
            original_name=base_name, alias_name=base_name)).alias_name
    ).__dict__ for base_name in search.search_base_backup_folders()])


def response_aliases_page() -> str:
    """Получить рендер страницы списка алиасов баз 1С"""
    return render_template(template_name_or_list='aliases.html')
