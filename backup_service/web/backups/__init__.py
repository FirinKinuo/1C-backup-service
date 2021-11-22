from flask import Blueprint
from pathlib import Path

blueprint = Blueprint('backups', __name__,
                      template_folder=str(Path(__path__[0], 'templates')),
                      static_folder=str(Path(__path__[0], 'static')))
