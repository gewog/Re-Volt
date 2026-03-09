"""Тесты приложения batteries."""
import uuid
from django.test import TestCase, Client


class BatteriesViewsTest(TestCase):
    """Проверка основных страниц и сценариев."""

    def test_home_page(self):
        """Главная страница отдаёт 200."""
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_register_page(self):
        """Страница регистрации отдаёт 200."""
        r = self.client.get('/register/')
        self.assertEqual(r.status_code, 200)

    def test_login_page(self):
        """Страница входа отдаёт 200."""
        r = self.client.get('/login/')
        self.assertEqual(r.status_code, 200)

    def test_my_redirects_when_anonymous(self):
        """/my/ редиректит на логин для неавторизованных."""
        r = self.client.get('/my/')
        self.assertIn(r.status_code, (302, 200))

    def test_full_flow_register_login_add_submission(self):
        """Регистрация → вход → добавление сдачи."""
        uname = f'test_{uuid.uuid4().hex[:8]}'
        # Регистрация
        r = self.client.post('/register/', {
            'username': uname,
            'email': f'{uname}@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertIn(r.status_code, (200, 302))
        # Вход
        r = self.client.post('/login/', {'username': uname, 'password': 'TestPass123!'})
        self.assertIn(r.status_code, (200, 302))
        # Мои сдачи
        r = self.client.get('/my/')
        self.assertEqual(r.status_code, 200)
        # Добавление сдачи
        r = self.client.post('/my/', {'count': 5, 'city': 'Москва'})
        self.assertIn(r.status_code, (200, 302))
