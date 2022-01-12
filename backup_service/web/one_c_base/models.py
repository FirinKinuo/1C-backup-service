from pydantic import BaseModel, constr


class OneCBaseNames(BaseModel):
    """Модель названий баз 1С"""
    original_name: constr(max_length=32)
    alias_name: constr(max_length=32)


class OneCBaseModel(OneCBaseNames):
    """Модель данных базы 1С"""
    share: bool
