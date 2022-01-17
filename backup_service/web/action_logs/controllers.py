from logging import getLogger

from flask import render_template, Response, request, jsonify

from backup_service.database import action_logs
from backup_service.web.action_logs import models

log = getLogger("Backup.Controller")


def response_action_logs_page() -> str:
    """
    Получить рендер страницы с бэкапами
    Returns:
        str: Строка срендренной страницы
    """

    return render_template('action_logs.html')


def response_action_logs_pagination() -> Response:
    """Получить список логов"""
    logs_pagination = action_logs.ActionLogs.get_pool_with_offset(
        offset=(request.query_params.page - 1) * request.query_params.per_page,
        pool=request.query_params.per_page
    )

    return jsonify([models.ActionLogsModel(
        id=log_data.id,
        ip=log_data.ip,
        user=log_data.user,
        type=log_data.type,
        date=log_data.date,
        message=log_data.message
    ).__dict__ for log_data in logs_pagination])
