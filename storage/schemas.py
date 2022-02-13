from typing import Optional
from pydantic import BaseModel, Field


class GeonameEntry(BaseModel):
    geonameid: int = Field(title='Идентификатор географического объекта')
    name: str = Field(title='Название географического объекта')
    alternate_names: list[str] = Field(title='Альтернативные названия объекта')
    asciiname: str = Field(title='Название, записанное символами ASCII')
    latitude: float = Field(title='Широта географического объекта')
    longitude: float = Field(title='Долгота географического объекта')
    feature_class: str = Field(title='Класс географического объекта')
    feature_code: str = Field(title='Код подкласса географического объекта')
    country_code: str = Field(title='Код страны географического объекта')
    cc2: list[str] = Field(title='Альтернативные коды страны географического объекта')
    admin1: str = Field(title='FIPS-код географического объекта')
    admin2: str = Field(title='Код второго уровня административно-территориального деления географического объекта')
    admin3: str = Field(title='Код третьего уровня административно-территориального деления географического объекта')
    admin4: str = Field(title='Код четвертого уровня административно-территориального деления географического объекта')
    population: int = Field(title='Население географического объекта')
    elevation: Optional[int] = Field(title='Уровень возвышения географического объекта')
    dem: int = Field(title='Средний уровень возвышения географического объекта')
    timezone: str = Field(title='Название часового пояса географического объекта')
    modification_date: str = Field(title='Дата последней модификации записи (в базе GeoNames) географического объекта')


class GeonameEntryDiff(BaseModel):
    object1: GeonameEntry = Field(title='Географический объект, соответствующий первому названию')
    object2: GeonameEntry = Field(title='Географический объект, соответствующий первому названию')
    more_north_id: int = Field(title='Идентификатор объекта, находящегося севернее')
    same_timezone: bool = Field(title='Находятся ли объекты в одной часовой зоне')
    timezone_diff: float = Field(title='Разница часовых зон объектов в часах')


class HTTPError(BaseModel):
    detail: str = Field(title='Описание ошибки')