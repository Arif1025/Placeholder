from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = "Seed the database with 100 fake users"

    def handle(self, *args, **options):
        fake = Faker()

        num_users = 100

        self.stdout.write(f"Seeding {num_users} users...")

        for _ in range(num_users):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "password123" 

            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )
            if created:
                user.set_password(password)
                user.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {num_users} users."))