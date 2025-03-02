import csv
from django.test import TestCase
from django.urls import reverse
from models import Quiz, Question

class DownloadReportTests(TestCase):
    def setUp(self):
        """Create a test quiz with a few questions."""
        self.quiz = Quiz.objects.create(title="Test Quiz")
        self.question1 = Question.objects.create(text="Question 1", question_type="text", options="")
        self.question2 = Question.objects.create(text="Question 2", question_type="mcq", options="A,B,C,D")

    def test_download_report(self):
        """Test that the CSV report can be downloaded."""
        response = self.client.get(reverse('download_report', kwargs={'quiz_id': self.quiz.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Check CSV content
        csv_content = response.content.decode('utf-8').split("\n")
        csv_reader = csv.reader(csv_content)
        header = next(csv_reader)

        self.assertEqual(header, ["Question", "Type", "Options"])
        self.assertIn(["Question 1", "text", ""], csv_reader)
        self.assertIn(["Question 2", "mcq", "A,B,C,D"], csv_reader)