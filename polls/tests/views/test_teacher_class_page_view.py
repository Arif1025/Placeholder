from django.test import TestCase
from django.urls import reverse

class TeacherPageViewTestCase(TestCase):
    """Tests for the teacher class page view and its elements."""

    def setUp(self):
        self.url = reverse('class_view_teacher') 

    def test_teacher_page_url(self):
        """Test that the URL is correct."""
        self.assertEqual(self.url, '/class_view_teacher/')  

    def test_get_teacher_page(self):
        """Test that the teacher page loads properly."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'class_template_page_teacher.html')

        # Check for expected elements in the HTML (e.g., class title, teacher's name)
        self.assertContains(response, '<h1>Class View</h1>')
        self.assertContains(response, 'Welcome, Teacher!')
        self.assertContains(response, 'Math 101')
        self.assertContains(response, 'Teacher: Mr. Smith')

    def test_enrolled_students_section(self):
        """Test that the list of enrolled students and their grades are displayed correctly."""
        response = self.client.get(self.url)

        self.assertContains(response, 'Enrolled Students')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'Grade: 85')
        self.assertContains(response, 'Polls Answered: Poll 1, Poll 2')
        self.assertContains(response, 'Jane Smith')
        self.assertContains(response, 'Grade: 90')
        self.assertContains(response, 'Polls Answered: Poll 1')
        self.assertContains(response, 'Samuel Adams')
        self.assertContains(response, 'Grade: 78')
        self.assertContains(response, 'Polls Answered: Poll 1, Poll 2')

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

    def test_footer(self):
        """Test that the footer is displayed properly with the correct text."""
        response = self.client.get(self.url)

        self.assertContains(response, '&copy; 2025 Polling System')

    def test_mobile_responsiveness(self):
        """Test if the page is responsive on smaller screens."""
        response = self.client.get(self.url)
        
        self.assertContains(response, '@media screen and (max-width: 768px)')

    def test_student_elements_visibility(self):
        """Test that the teacher-specific elements (grades, polls answered) are visible and rendered correctly."""
        response = self.client.get(self.url)

        # Ensure that grades and poll answers are visible to the teacher
        self.assertContains(response, 'Grade: 85')
        self.assertContains(response, 'Polls Answered: Poll 1, Poll 2')
        self.assertContains(response, 'Grade: 90')
        self.assertContains(response, 'Polls Answered: Poll 1')
        self.assertContains(response, 'Grade: 78')
        self.assertContains(response, 'Polls Answered: Poll 1, Poll 2')

    def test_poll_list_items(self):
        """Test that the poll list items are displayed correctly for the teacher."""
        response = self.client.get(self.url)
        
        self.assertContains(response, '<li>Poll 2: Feedback on last lesson</li>')

    def test_logout_button_position(self):
        """Test that the logout button is correctly positioned at the top-right corner."""
        response = self.client.get(self.url)

        self.assertContains(response, 'position: fixed; top: 20px; right: 20px;')

    def test_back_button_position(self):
        """Test that the back button is correctly positioned at the top-left corner."""
        response = self.client.get(self.url)

        self.assertContains(response, 'position: fixed; top: 20px; left: 20px;')

