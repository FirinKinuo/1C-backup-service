from pydantic import BaseModel, constr


class AliasNameQuery(BaseModel):
    """Модель данных запроса на alias_name базы 1С"""
    original_name: constr(max_length=32)
    alias_name: constr(max_length=32)
    share: bool
