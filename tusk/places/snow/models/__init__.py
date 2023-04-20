from pydantic import BaseModel



def to_lower_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_lower_camel
        allow_population_by_field_name = True
