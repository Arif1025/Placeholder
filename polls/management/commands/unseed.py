from django.core.management.base import BaseCommand
from polls.models import (
    CustomUser, Class, ClassStudent, Teaching,
    Poll, Question, Choice
)

class Command(BaseCommand):
    help = "Unseed the database by deleting all seeded polls, questions, choices, classes, and users (excluding superusers)."

    def handle(self, *args, **options):
        self.stdout.write("🧹 Starting unseeding process...")

        # Delete poll-related data
        Choice.objects.all().delete()
        self.stdout.write("✅ Deleted all Choices.")

        Question.objects.all().delete()
        self.stdout.write("✅ Deleted all Questions.")

        Poll.objects.all().delete()
        self.stdout.write("✅ Deleted all Polls.")

        # Delete class/student/teaching structure
        Teaching.objects.all().delete()
        self.stdout.write("✅ Deleted all Teaching relationships.")

        ClassStudent.objects.all().delete()
        self.stdout.write("✅ Deleted all ClassStudent relationships.")

        Class.objects.all().delete()
        self.stdout.write("✅ Deleted all Classes.")

        # Delete seeded users (students & teachers, excluding superusers)
        deleted_user_count, _ = CustomUser.objects.filter(
            is_superuser=False,
            role__in=["student", "teacher"]
        ).delete()
        self.stdout.write(f"✅ Deleted {deleted_user_count} seeded users.")

        self.stdout.write(self.style.SUCCESS("🎉 Unseeding complete!"))
