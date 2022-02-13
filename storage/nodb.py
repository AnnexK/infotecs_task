from typing_extensions import Self
from typing import Optional
from .schemas import GeonameEntry
import csv


class Storage:
    def _decode_row(self, row:list[str]) -> GeonameEntry:
        return GeonameEntry(
            geonameid=int(row[0]),
            name=row[1],
            asciiname = row[2],
            alternate_names = [] if row[3] == '' else row[3].split(','),
            latitude = float(row[4]),
            longitude = float(row[5]),
            feature_class = row[6],
            feature_code = row[7],
            country_code = row[8],
            cc2 = [] if row[9] == '' else row[9].split(','),
            admin1 = row[10],
            admin2 = row[11],
            admin3 = row[12],
            admin4 = row[13],
            population = int(row[14]),
            elevation = None if row[15] == '' else int(row[15]),
            dem = int(row[16]),
            timezone = row[17],
            modification_date = row[18]
        )
    
    def __init__(self, filename: str):
        with open(filename, 'r', encoding='utf8') as fp:
            reader = csv.reader(fp, delimiter='\t')
            self.entries = [ self._decode_row(r) for r in reader ]
            self.id_dict = { r.geonameid: r for r in self.entries }
    
    def __call__(self) -> Self:
        return self

    def get_by_id(self, id: int) -> Optional[GeonameEntry]:
        return self.id_dict.get(id, None)

    def get_offset_limit(self, offset: int, limit: int) -> list[GeonameEntry]:
        return self.entries[offset:offset+limit]

    def get_by_alias(self, alias: str) -> list[GeonameEntry]:
        def alias_filter(entry: GeonameEntry) -> bool:
            return any( alias.casefold() == alt.casefold() for alt in entry.alternate_names )
        return list(filter(alias_filter, self.entries))

    def get_by_name(self, name: str) -> list[GeonameEntry]:
        def name_filter(entry: GeonameEntry) -> bool:
            return name.casefold() == entry.name.casefold()

        return list(filter(name_filter, self.entries))