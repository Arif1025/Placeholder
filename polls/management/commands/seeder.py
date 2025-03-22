from django.core.management.base import BaseCommand
from polls.models import CustomUser, Class, ClassStudent, Teaching
from django.contrib.auth import get_user_model
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed the database with 100 fake users, student, teachers and classes."

    def handle(self, *args, **options):
        fake = Faker()

        num_users = 100
        num_classes = 10
        num_teachers = 5
        num_students_per_class = 20

        self.stdout.write(f"Seeding {num_users} users, {num_classes} classes, {num_teachers} teachers, and students...")

        User = get_user_model()

        # Ensure a superuser exists (skip creating a superuser in the seeder)
        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser not found, please create one manually with 'createsuperuser'.")
            return

        users = []
        teachers = []
        for _ in range(num_teachers):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "Password123"
            
            teacher, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={"email": email, "role": "teacher"}
            )
            if created:
                teacher.set_password(password)
                teacher.save()
                teachers.append(teacher)
        
        students = []
        for _ in range(num_users - num_teachers):
            username = fake.unique.user_name()
            email = fake.unique.email()
            password = "Password123"

            student, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={"email": email, "role": "student"}
            )
            if created:
                student.set_password(password)
                student.save()
                students.append(student)

        # Create fake classes
        classes = []
        for _ in range(num_classes):
            if teachers:
                teacher = random.choice(teachers)
                class_name = fake.company()
                class_instance = Class.objects.create(name=class_name, teacher=teacher)
                classes.append(class_instance)

         # Enroll students in classes
        for class_instance in classes:
            if len(students) < num_students_per_class:
                self.stdout.write(self.style.WARNING("Not enough students available. Adjusting number of students per class."))
                num_students_per_class = len(students)

            students_in_class = random.sample(students, num_students_per_class)
            for student in students_in_class:
                # Create the relationship between student and class in ClassStudent
                ClassStudent.objects.create(student=student, class_instance=class_instance)

        # Assign students to teachers
        for student in students:
            teacher = random.choice(teachers)
            Teaching.objects.create(teacher=teacher, student=student)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {num_users} users, {num_classes} classes, {num_teachers} teachers, and {num_students_per_class} students per class."))