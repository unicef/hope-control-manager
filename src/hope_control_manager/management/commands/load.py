import logging
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pandas as pd
import requests
from django.core.management import BaseCommand

from hope_control_manager.models import Area, AreaType

if TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)

GEONAMES_COLUMNS = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature_class",
    "feature_code",
    "country_code",
    "cc2",
    "admin1_code",
    "admin2_code",
    "admin3_code",
    "admin4_code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification_date",
]


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def add_arguments(self, parser: "ArgumentParser") -> None:
        pass

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: C901
        from hope_control_manager.models import Country

        Country.objects.load()
        downloads_path = Path("~DATA")
        downloads_path.mkdir(parents=True, exist_ok=True)

        self.stdout.write(self.style.NOTICE("Processing "), ending="")
        for country in Country.objects.filter().order_by("name"):
            base_url = "https://download.geonames.org/export/dump/"
            zip_filename = f"{country.iso_code2.upper()}.zip"
            txt_filename = f"{country.iso_code2.upper()}.txt"
            url = f"{base_url}{zip_filename}"
            local_zip_path = downloads_path / zip_filename
            if local_zip_path.exists():
                self.stdout.write(self.style.SUCCESS(country.iso_code2), ending=", ")
            else:
                self.stdout.write(self.style.WARNING(country.iso_code2), ending=", ")
                with requests.get(url, stream=True, timeout=60) as response:
                    response.raise_for_status()
                    with open(local_zip_path, "wb") as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

            with zipfile.ZipFile(local_zip_path, "r") as zf, zf.open(txt_filename) as txt_file:
                df = pd.read_csv(
                    txt_file,
                    sep="\t",  # This is a Tab-Separated-Value (TSV) file
                    header=None,  # The file has no header row
                    names=GEONAMES_COLUMNS,  # We provide the column names
                    encoding="utf-8",
                    usecols=[
                        "name",
                        "feature_code",
                        "admin1_code",
                        "admin2_code",
                        "admin3_code",
                        "admin4_code",
                        "geonameid",
                        "asciiname",
                    ],
                )
                at1, __ = AreaType.objects.get_or_create(
                    country=country, name="Admin Level 1", parent=None, area_level=1
                )
                at2, __ = AreaType.objects.get_or_create(
                    country=country, name="Admin Level 2", parent=at1, area_level=2
                )
                at3, __ = AreaType.objects.get_or_create(
                    country=country, name="Admin Level 3", parent=at2, area_level=3
                )
                at4, __ = AreaType.objects.get_or_create(
                    country=country, name="Admin Level 4", parent=at3, area_level=4
                )
                adm1 = df[df["feature_code"] == "ADM1"]
                for __, entry1 in adm1.iterrows():
                    a1, __ = Area.objects.get_or_create(
                        geonameid=entry1["geonameid"],
                        defaults={
                            "area_type": at1,
                            "p_code": str(entry1["admin1_code"]),
                            "name": entry1["asciiname"],
                        },
                    )
                    adm2 = df[(df["feature_code"] == "ADM2") & (df["admin1_code"] == entry1["admin1_code"])]
                    for __, entry2 in adm2.iterrows():
                        a2, __ = Area.objects.get_or_create(
                            geonameid=entry2["geonameid"],
                            defaults={
                                "area_type": at2,
                                "parent": a1,
                                "p_code": entry2["admin2_code"],
                                "name": entry2["asciiname"],
                            },
                        )
                        adm3 = df[
                            (df["feature_code"] == "ADM3")
                            & (df["admin1_code"] == entry2["admin1_code"])
                            & (df["admin2_code"] == entry2["admin2_code"])
                        ]
                        for __, entry3 in adm3.iterrows():
                            a3, __ = Area.objects.get_or_create(
                                geonameid=entry3["geonameid"],
                                defaults={
                                    "area_type": at3,
                                    "parent": a2,
                                    "p_code": entry3["admin3_code"],
                                    "name": entry3["asciiname"],
                                },
                            )
                            adm4 = df[
                                (df["feature_code"] == "ADM4")
                                & (df["admin1_code"] == entry3["admin1_code"])
                                & (df["admin2_code"] == entry3["admin2_code"])
                                & (df["admin3_code"] == entry3["admin3_code"])
                            ]
                            for __, entry4 in adm4.iterrows():
                                Area.objects.get_or_create(
                                    geonameid=entry4["geonameid"],
                                    defaults={
                                        "area_type": at4,
                                        "parent": a3,
                                        "p_code": entry4["admin4_code"],
                                        "name": entry4["asciiname"],
                                    },
                                )

            Area.objects.rebuild()
