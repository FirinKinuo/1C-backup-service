from flask import render_template

from backup_service.web.backups import blueprint


@blueprint.route('/')
def view_backups() -> str:
    """
    View странцы списка бекапов

    Returns:
        str: Отрендеринная страница backups
    """
    return render_template(
        'backup_table.html',
        base_numbers=[250, 251, 252, 253]
    )
