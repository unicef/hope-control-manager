import logging
from typing import TYPE_CHECKING, Any

from django.core.management import BaseCommand

from hope_control_manager.utils.loaders import load_areas, load_banks

if TYPE_CHECKING:
    from argparse import ArgumentParser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    requires_migrations_checks = False
    requires_system_checks = []

    def add_arguments(self, parser: "ArgumentParser") -> None:
        parser.add_argument(
            "--only",
            "-o",
            default=[],
            action="append",
            help=("Only process this country code. It can be specified multiple times."),
        )

    def handle(self, *args: Any, **options: Any) -> None:  # noqa: C901
        from hope_control_manager.models import Country

        Country.objects.load()
        load_areas(stdout=self.stdout, style=self.style, only=options["only"])
        load_banks(stdout=self.stdout, style=self.style)
