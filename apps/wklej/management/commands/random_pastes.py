from django.core.management.base import BaseCommand
from wklej.models import Wklejka
from wklej.populate import wklejka


class Command(BaseCommand):
    help = "Create set of new pastes"
    args = "[how many]"

    def handle(self, how_many=100, **options):
        for i in range(int(how_many)):
            w = Wklejka(**wklejka())
            w.save()
            print "WKLEJKA", w.id
