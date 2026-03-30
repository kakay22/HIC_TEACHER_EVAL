import csv
from django.core.management.base import BaseCommand
from evaluation.models import Student

class Command(BaseCommand):
    help = "Import student IDs from CSV"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                student_id = row['student_id']

                Student.objects.get_or_create(
                    student_id=student_id
                )

        self.stdout.write(self.style.SUCCESS("Students imported successfully"))