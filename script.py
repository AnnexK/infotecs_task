from fastapi import FastAPI, Path, Query
from fastapi.responses import JSONResponse
from storage.schemas import GeonameEntry, GeonameEntryDiff, HTTPError
from storage.nodb import Storage
from util.translit import bgn_pcgn as transliterate
from util.timezone import tzdiff

import uvicorn


app = FastAPI()


filename = 'RU.txt'
storage: Storage = Storage(filename)


@app.get('/cities/', response_model=list[GeonameEntry])
async def get_city_page(
    page: int = Query(..., title='Номер страницы', gt=0),
    entries_per_page: int = Query(..., title='Количество городов на страницу', gt=0),
):
    entries = storage.get_offset_limit((page-1) * entries_per_page, entries_per_page)
    return entries


@app.get('/cities/{geonameid}', response_model=GeonameEntry,
    responses={404: {'model': HTTPError}})
async def get_city_info(
    geonameid: int = Path(..., title='Идентификатор города', gt=0),
):
    entry = storage.get_by_id(geonameid)
    if entry is None:
        return JSONResponse(status_code=404, content={'detail': f'Город с идентификатором {geonameid} не найден'})
    else:
        return entry


@app.get('/diff/', response_model=GeonameEntryDiff,
    responses = {404: {'model': HTTPError}})
async def get_city_diff(
    name1: str = Query(..., title='Название первого города'),
    name2: str = Query(..., title='Название второго города'),
):
    def key_foo(entry: GeonameEntry) -> int:
        return entry.population
    
    entries1 = sorted(storage.get_by_alias(name1) + storage.get_by_name(transliterate(name1)), key=key_foo)
    if not entries1:
        return JSONResponse(status_code=404, content={'detail': f'Город с именем name1={name1} не найден'})

    entries2 = sorted(storage.get_by_alias(name2) + storage.get_by_name(transliterate(name2)), key=key_foo)
    if not entries2:
        return JSONResponse(status_code=404, content={'detail': f'Город с именем name2={name2} не найден'})

    object1 = entries1[-1]
    object2 = entries2[-1]

    timediff = tzdiff(object1.timezone, object2.timezone)

    dct = {
       'object1': object1,
       'object2': object2,
       'same_timezone': timediff == 0.0,
       'more_north_id': object1.geonameid if object1.latitude > object2.latitude else object2.geonameid,
       'timezone_diff': timediff
    }
    return GeonameEntryDiff( **dct )

if __name__ == "__main__":
    uvicorn.run('script:app', host="localhost", port=8000)
