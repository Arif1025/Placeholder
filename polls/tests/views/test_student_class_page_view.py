from django.test import TestCase
from django.urls import reverse

class StudentPageViewTestCase(TestCase):
    """Tests for the student class page view and its elements."""

    def setUp(self):
        """Set up the URL for the student class page."""
        self.url = reverse('class_view_student')

    def test_student_page_url(self):
        """Test that the URL for the student class page is correct."""
        self.assertEqual(self.url, '/class_view_student/')

    def test_get_student_page(self):
        """
        Test that the student class page loads properly with the correct template 
        and key elements like class title and teacher's name.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'class_template_page_student.html')

        # Check that the page contains expected content
        self.assertContains(response, '<h1>Class View</h1>')
        self.assertContains(response, 'Welcome, Student!')
        self.assertContains(response, 'Math 101')
        self.assertContains(response, 'Teacher: Mr. Smith')

    def test_enrolled_students_section(self):
        """Test that the list of enrolled students is displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Enrolled Students')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Jane Smith')
        self.assertContains(response, 'Samuel Adams')

    def test_most_recent_poll_section(self):
        """Test that the most recent poll is displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Most Recent Poll')
        self.assertContains(response, 'Poll 2: Feedback on last lesson')

    def test_average_grade_section(self):
        """Test that the average grade for the most recent poll is displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Average Grade for Recent Poll: 84.3')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_back_button(self):
        """Test that the 'Back' button is visible and works as expected."""
        response = self.client.get(self.url)

        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')

    def test_footer(self):
        """Test that the footer is displayed properly with the correct copyright text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the student page is responsive on smaller screens."""
        response = self.client.get(self.url)

        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_student_elements_visibility(self):
        """
        Test that student-specific elements are visible (e.g., student name),
        while restricting access to grade or other sensitive information.
        """
        response = self.client.get(self.url)

        # Ensure that grade and poll answered data is not visible to students
        self.assertNotContains(response, 'Grade:')
        self.assertNotContains(response, 'Polls Answered:')

        # Ensure students can only see their name, not others'
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')
        self.assertNotContains(response, 'Samuel Adams')

    def test_poll_list_items(self):
        """Test that the list of polls is displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, '<li>Poll 2: Feedback on last lesson</li>')
