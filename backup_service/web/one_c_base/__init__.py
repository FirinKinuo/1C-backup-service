from pathlib import Path

from flask import Blueprint

blueprint = Blueprint('one_c_base', __name__,
                      template_folder=str(Path(__path__[0], 'templates')),
                      static_folder=str(Path(__path__[0], 'static')))
