from logging import getLogger
from flask import Blueprint

blueprint = Blueprint('backups', __name__)

log = getLogger("Backup.Controller")
