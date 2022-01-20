from pydantic import BaseModel, constr


class OneCBaseModel(BaseModel):
    """Модель данных базы 1С"""
    original_name: constr(max_length=32)
    alias_name: constr(max_length=32)
    share: bool
