from django.core.management.base import BaseCommand
from polls.models import CustomUser, Class, ClassStudent, Teaching

class Command(BaseCommand):
    help = "Unseed the database by removing all seeded students, teachers, classes, and related records."

    def handle(self, *args, **options):
        self.stdout.write("Starting unseeding process...")

        # Delete ClassStudent relationships
        ClassStudent.objects.all().delete()
        self.stdout.write("Deleted all ClassStudent relationships.")

        # Delete Teaching relationships
        Teaching.objects.all().delete()
        self.stdout.write("Deleted all Teaching relationships.")

        # Delete Classes
        Class.objects.all().delete()
        self.stdout.write("Deleted all Classes.")

        # Delete students and teachers
        deleted_users = CustomUser.objects.filter(is_superuser=False, role__in=["student", "teacher"]).delete()
        self.stdout.write(f"Deleted {deleted_users[0]} seeded users (students & teachers).")

        self.stdout.write(self.style.SUCCESS("Unseeding complete."))
