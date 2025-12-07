"""
Importing Specializations data.
"""
import os
import csv

from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.contrib.auth import get_user_model
from core.models import Specialization

User = get_user_model()


class Command(BaseCommand):
    help = 'Import specializations from CSV at /data/ad_specialization.csv'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        csv_file_path = os.path.join(base_dir, 'data', 'ad_specialization.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found: {csv_file_path}"))
            return

        user = User.objects.filter(is_superuser=True).first() or User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("No user found to assign specializations."))
            return

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            count = 0
            for row in reader:
                try:
                    (
                        _id,
                        created_at,
                        updated_at,
                        is_active_flag,
                        name,
                        slug,
                        description
                    ) = row

                    is_active = True if is_active_flag.lower() == 'f' else False

                    if not description:
                        description = "No description available."

                    # Avoid duplicates by name
                    obj, created = Specialization.objects.get_or_create(
                        name=name,
                        defaults={
                            'user': user,
                            'slug': slug,
                            'specialty': slug.replace('-', ' ').title(),
                            'description': description,
                            'is_active': is_active,
                            'created_at': parse_datetime(created_at),
                            'updated_at': parse_datetime(updated_at),
                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Imported: {name}'))
                        count += 1
                    else:
                        self.stdout.write(self.style.WARNING(f'Skipped (exists): {name}'))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Failed to import row: {row}\nError: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Import complete: {count} specializations added.'))
