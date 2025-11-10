import json
import sys
import zipfile
from pathlib import Path

import pandas as pd
import requests
from django.core.management.base import OutputWrapper
from django.core.management.color import Style, no_style

from hope_control_manager.models import Area, AreaType, Branch, Country, FinancialInstitution

GEONAMES_COLUMNS = [
    "admin1_code",
    "admin2_code",
    "admin3_code",
    "admin4_code",
    "alternatenames",
    "asciiname",
    "cc2",
    "country_code",
    "dem",
    "elevation",
    "feature_class",
    "feature_code",
    "geonameid",
    "latitude",
    "longitude",
    "modification_date",
    "name",
    "population",
    "timezone",
]


def load_areas(stdout: OutputWrapper | None = None, style: Style | None = None, only: list[str] | None = None) -> None:  # noqa: C901
    if not stdout:
        stdout = OutputWrapper(sys.stdout)
    if not style:
        style = no_style()

    downloads_path = Path("~DATA")
    downloads_path.mkdir(parents=True, exist_ok=True)

    stdout.write(style.NOTICE("Processing "), ending="")
    stdout.flush()
    qs = Country.objects.filter().order_by("iso_code2")
    if only:
        qs = qs.filter(iso_code2__in=only)

    for country in qs:
        base_url = "https://download.geonames.org/export/dump/"
        zip_filename = f"{country.iso_code2.upper()}.zip"
        txt_filename = f"{country.iso_code2.upper()}.txt"
        url = f"{base_url}{zip_filename}"
        local_zip_path = downloads_path / zip_filename
        if local_zip_path.exists():
            stdout.write(style.SUCCESS(country.iso_code2), ending=", ")
        else:
            stdout.write(style.WARNING(country.iso_code2), ending=", ")
            with requests.get(url, stream=True, timeout=60) as response:
                response.raise_for_status()
                with open(local_zip_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):  # noqa: FURB122
                        f.write(chunk)
        stdout.flush()
        try:
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
        except (FileNotFoundError, zipfile.BadZipFile) as e:
            stdout.write(f"{local_zip_path}: {str(e)}", ending=",")

        Area.objects.rebuild()


def load_banks(stdout: OutputWrapper | None = None, style: Style | None = None) -> None:
    if not stdout:
        stdout = OutputWrapper(sys.stdout)
    stdout.write("Loading banks...\n")
    bank_zip_path = Path("~DATA/swift_codes.zip")
    FinancialInstitution.objects.all().delete()
    with zipfile.ZipFile(bank_zip_path, "r") as zf, zf.open("swifts.jsonl") as json_file:
        for line in json_file.readlines():
            data = json.loads(line)
            country_code = data["swift"][4:6]
            bank, __ = FinancialInstitution.objects.get_or_create(
                bank_code=data["swift"][:4], defaults={"name": data["name"]}
            )
            try:
                Branch.objects.get_or_create(
                    institution=bank, swift_code=data["swift"], country=Country.objects.get(iso_code2=country_code)
                )
            except Country.DoesNotExist as e:
                raise ValueError(e) from None
