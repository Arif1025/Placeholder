from django.test import TestCase
from polls.models import (
    Poll, Question, Choice, CustomUser,
    Teaching, Class, ClassStudent,
    StudentResponse, StudentQuizResult
)

class ModelTests(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher', password='pass1234', role='teacher')
        self.student = CustomUser.objects.create_user(username='student', password='pass1234', role='student')

    def test_poll_code_auto_generated(self):
        poll = Poll.objects.create(title='Auto Code Test', created_by=self.teacher)
        self.assertIsNotNone(poll.code)
        self.assertEqual(len(poll.code), 8)

    def test_poll_code_not_overwritten(self):
        poll = Poll.objects.create(title='Static Code', created_by=self.teacher, code='STATIC01')
        poll.save()
        self.assertEqual(poll.code, 'STATIC01')

    def test_poll_participant_addition(self):
        poll = Poll.objects.create(title='Poll X', created_by=self.teacher)
        poll.participants.add(self.student)
        self.assertIn(self.student, poll.participants.all())

    def test_question_string_representation(self):
        poll = Poll.objects.create(title='Quiz', created_by=self.teacher)
        question = Question.objects.create(poll=poll, text='What is Python?', question_type='written')
        self.assertEqual(str(question), 'What is Python?')

    def test_question_get_options(self):
        poll = Poll.objects.create(title='Quiz', created_by=self.teacher)
        q = Question.objects.create(poll=poll, text='Select one', question_type='mcq')
        q.options = "A,B,C"
        self.assertEqual(q.get_options(), ['A', 'B', 'C'])

    def test_choice_string_representation_and_cleaning(self):
        poll = Poll.objects.create(title='Quiz', created_by=self.teacher)
        question = Question.objects.create(poll=poll, text='Color?', question_type='mcq')
        choice = Choice.objects.create(question=question, text=' Blue \n ', is_correct=True)
        self.assertEqual(str(choice), 'Blue')

    def test_choice_text_cleaned_on_save(self):
        poll = Poll.objects.create(title='Clean Test', created_by=self.teacher)
        q = Question.objects.create(poll=poll, text='MCQ?', question_type='mcq')
        choice = Choice.objects.create(question=q, text='  Messy \n Text ')
        self.assertEqual(choice.text, 'Messy Text')

    def test_custom_user_role_assignment(self):
        self.assertEqual(self.teacher.role, 'teacher')
        self.assertEqual(self.student.role, 'student')

    def test_teacher_teaches_multiple_students(self):
        s2 = CustomUser.objects.create_user(username='student2', password='pass', role='student')
        Teaching.objects.create(teacher=self.teacher, student=self.student)
        Teaching.objects.create(teacher=self.teacher, student=s2)
        self.assertEqual(self.teacher.students.count(), 2)

    def test_teaching_relationship(self):
        Teaching.objects.create(teacher=self.teacher, student=self.student)
        self.assertIn(self.student, self.teacher.students.all())

    def test_class_and_student_assignment(self):
        class_instance = Class.objects.create(name='Math 101', teacher=self.teacher)
        ClassStudent.objects.create(student=self.student, class_instance=class_instance)
        self.assertEqual(str(class_instance), 'Math 101')
        self.assertEqual(str(ClassStudent.objects.first()), 'student in Math 101')

    def test_student_response_model(self):
        poll = Poll.objects.create(title='Poll', created_by=self.teacher)
        question = Question.objects.create(poll=poll, text='Capital of France?', question_type='written')
        response = StudentResponse.objects.create(student=self.student, question=question, response='Paris')
        self.assertEqual(response.response, 'Paris')

    def test_student_multiple_responses_possible(self):
        poll = Poll.objects.create(title='Poll', created_by=self.teacher)
        question = Question.objects.create(poll=poll, text='Type something', question_type='written')
        StudentResponse.objects.create(student=self.student, question=question, response='A')
        StudentResponse.objects.create(student=self.student, question=question, response='B')
        self.assertEqual(StudentResponse.objects.filter(student=self.student, question=question).count(), 2)

    def test_quiz_result_model(self):
        poll = Poll.objects.create(title='Poll', created_by=self.teacher)
        result = StudentQuizResult.objects.create(student=self.student, poll=poll, score=4, total_questions=5)
        self.assertEqual(result.score, 4)
        self.assertEqual(result.total_questions, 5)

    def test_quiz_result_percentage(self):
        poll = Poll.objects.create(title='Poll', created_by=self.teacher)
        result = StudentQuizResult.objects.create(student=self.student, poll=poll, score=3, total_questions=5)
        percentage = (result.score / result.total_questions) * 100
        self.assertEqual(percentage, 60.0)

    def test_poll_deletes_related_questions(self):
        poll = Poll.objects.create(title='Cascade Poll', created_by=self.teacher)
        Question.objects.create(poll=poll, text='Q1', question_type='written')
        self.assertEqual(poll.questions.count(), 1)
        poll.delete()
        self.assertEqual(Question.objects.count(), 0)
