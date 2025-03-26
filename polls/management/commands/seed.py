from django.core.management.base import BaseCommand
from polls.models import CustomUser, Class, ClassStudent, Teaching, Poll, Question, Choice
from django.contrib.auth import get_user_model
from faker import Faker
import random

class Command(BaseCommand):
    help = "Seed the database with 200 users, 20 classes, and one quiz per class with questions and choices."

    def handle(self, *args, **options):
        fake = Faker()

        num_users = 200
        num_teachers = 5
        num_students = num_users - num_teachers
        num_classes = 20
        max_students_per_class = 10

        self.stdout.write(f"Seeding {num_users} users, {num_classes} classes")

        User = get_user_model()

        if not User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser not found, please create one manually with 'createsuperuser'.")
            return

        # Create teachers
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

        # Create students
        students = []
        for _ in range(num_students):
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

        # Create 20 class names
        subject_templates = ["Biology", "Chemistry", "History", "Mathematics", "Physics", "Philosophy", "Art", "Literature", "Geography", "Economics"]
        class_names = []
        for i in range(num_classes):
            subject = random.choice(subject_templates)
            number = random.randint(100, 499)
            class_names.append(f"{subject} {number}")

        # Assign 2–4 classes per teacher
        classes = []
        remaining_class_names = class_names.copy()
        for teacher in teachers:
            num_teacher_classes = random.randint(2, 4)
            for _ in range(num_teacher_classes):
                if not remaining_class_names:
                    break
                class_name = remaining_class_names.pop()
                class_instance = Class.objects.create(name=class_name, teacher=teacher)
                classes.append(class_instance)

        # Limit to max_classes
        classes = classes[:num_classes]

        # Enroll students in 2–4 random classes
        for student in students:
            num_classes_for_student = random.randint(2, 4)
            assigned_classes = random.sample(classes, min(num_classes_for_student, len(classes)))
            for class_instance in assigned_classes:
                if ClassStudent.objects.filter(class_instance=class_instance).count() < max_students_per_class:
                    ClassStudent.objects.get_or_create(student=student, class_instance=class_instance)

        # Create teacher-student relationships (Teaching)
        for student in students:
            teacher = random.choice(teachers)
            Teaching.objects.get_or_create(teacher=teacher, student=student)

        # Generate 1 poll only for classes where students are enrolled
        question_types = ['written', 'mcq']

        for class_instance in classes:
            enrolled_students = CustomUser.objects.filter(
                id__in=ClassStudent.objects.filter(class_instance=class_instance).values_list('student_id', flat=True)
            )

            if not enrolled_students.exists():
                continue  # Skip classes with no students

            teacher = class_instance.teacher

            # Create the poll for this class
            poll = Poll.objects.create(
                title=f"{class_instance.name} - {fake.word().capitalize()} Quiz",
                description=fake.sentence(),
                created_by=teacher,
                class_instance=class_instance,
                is_done=False
            )

            # Set participants to enrolled students
            poll.participants.set(enrolled_students)

            # Add questions to the poll
            num_questions = random.randint(3, 6)
            for _ in range(num_questions):
                question_type = random.choice(question_types)
                question_text = fake.sentence(nb_words=10)

                question = Question.objects.create(
                    poll=poll,
                    text=question_text,
                    question_type=question_type,
                    correct_answer=fake.word() if question_type == 'written' else ''
                )

                if question_type == 'mcq':
                    correct_index = random.randint(0, 3)
                    for i in range(4):
                        Choice.objects.create(
                            question=question,
                            text=fake.word().capitalize(),
                            is_correct=(i == correct_index)
                        )


        self.stdout.write(self.style.SUCCESS(
            f"✅ Seeded {len(teachers)} teachers, {len(students)} students, {len(classes)} classes, and 1 poll per class with questions."
        ))
