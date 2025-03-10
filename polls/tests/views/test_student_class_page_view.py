from django.test import TestCase
from django.urls import reverse

class StudentPageViewTestCase(TestCase):
    """Tests for the student class page view and its elements."""

    def setUp(self):
        self.url = reverse('class_view_student')

    def test_student_page_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/class_view_student/')

    def test_get_student_page(self):
        """Test that the student page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'class_template_page_student.html')

        # Check for expected elements in the HTML (e.g., class title, teacher's name)
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
        """Test that the average grade for the most recent poll is displayed."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Average Grade for Recent Poll: 84.3')

    def test_logout_button(self):
        """Test that the 'Logout' button is visible on the page."""
        response = self.client.get(self.url)

        self.assertContains(response, '<button type="submit" class="logout-button">Logout</button>')

    def test_back_button(self):
        """Test that the 'Back' button is visible and correctly renders a back action."""
        response = self.client.get(self.url)

        # Check for the back button's presence
        self.assertContains(response, '<a href="javascript:history.back()" class="back-button">Back</a>')

    def test_footer(self):
        """Test that the footer is displayed properly with the correct text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the page is responsive on smaller screens."""
        response = self.client.get(self.url)

        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_student_elements_visibility(self):
        """Test that the student-specific elements are visible and rendered correctly."""
        response = self.client.get(self.url)

        # Ensure no grade information is displayed (grades should not be visible to students)
        self.assertNotContains(response, 'Grade:')
        self.assertNotContains(response, 'Polls Answered:')

        # Ensure students can only see their name and not others' information
        self.assertContains(response, 'John Doe')
        self.assertNotContains(response, 'Jane Smith')
        self.assertNotContains(response, 'Samuel Adams')

    def test_poll_list_items(self):
        """Test that the poll list items are displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, '<li>Poll 2: Feedback on last lesson</li>')
