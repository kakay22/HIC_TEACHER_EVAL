import csv
from django.core.management.base import BaseCommand
from evaluation.models import Student  # adjust if your app name is different
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Import student IDs from a CSV file into the Student table'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file containing student IDs'
        )

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        count = 0

        try:
            with open(csv_file, newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                for row in reader:
                    if not row:
                        continue
                    student_id = row[0].strip()
                    if student_id:
                        try:
                            Student.objects.create(student_id=student_id)
                            count += 1
                        except IntegrityError:
                            # skip duplicates
                            continue
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} students.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))