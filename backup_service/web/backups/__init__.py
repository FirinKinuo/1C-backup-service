from pathlib import Path

from flask import Blueprint

blueprint = Blueprint('backups', __name__,
                      template_folder=str(Path(__path__[0], 'templates')),
                      static_folder=str(Path(__path__[0], 'static')))
