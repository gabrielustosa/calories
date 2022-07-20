import pytest

from calories.apps.calorie.views import home_view
from calories.tests.base import TestCustomBase


@pytest.mark.fast
class HomeViewTest(TestCustomBase):
    def test_home_view_returns_status_code_200(self):
        self.login()
        response = self.response_get('calorie:home')
        self.assertEqual(response.status_code, 200)

    def test_home_view_loads_correct_template(self):
        self.login()
        response = self.response_get('calorie:home')
        self.assertTemplateUsed(response, 'calorie/home.html')
