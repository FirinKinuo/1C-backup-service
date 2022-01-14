from logging import getLogger

from flask import Blueprint

blueprint = Blueprint('one_c_base', __name__)
log = getLogger("1C.Base.Controllers")
