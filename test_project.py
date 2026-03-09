#!/usr/bin/env python
"""Быстрый тест проекта через Django test client."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bat.settings')
os.environ['DJANGO_DEBUG'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.test import Client

def main():
    import uuid
    client = Client()
    uname = f'test_{uuid.uuid4().hex[:8]}'
    # Главная
    r = client.get('/')
    assert r.status_code == 200, f'Home: expected 200, got {r.status_code}'
    assert 'батарейк' in r.content.decode() or 'total' in r.content.decode().lower()
    print('OK: / (home) -> 200')
    # Регистрация
    r = client.get('/register/')
    assert r.status_code == 200, f'Register: expected 200, got {r.status_code}'
    print('OK: /register/ -> 200')
    # Регистрация POST
    r = client.post('/register/', {
        'username': uname,
        'email': f'{uname}@example.com',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!',
    })
    assert r.status_code in (200, 302), f'Register POST: {r.status_code}'
    print('OK: /register/ POST ->', r.status_code)
    # Логин POST
    r = client.post('/login/', {'username': uname, 'password': 'TestPass123!'})
    assert r.status_code in (200, 302), f'Login POST: {r.status_code}'
    print('OK: /login/ POST ->', r.status_code)
    # Мои сдачи (после логина)
    r = client.get('/my/')
    assert r.status_code == 200, f'My: expected 200, got {r.status_code}'
    print('OK: /my/ -> 200')
    # Добавление сдачи
    r = client.post('/my/', {'count': 5, 'city': 'Москва'})
    assert r.status_code in (200, 302), f'Add submission: {r.status_code}'
    print('OK: /my/ POST (add) ->', r.status_code)
    print('All tests passed.')

if __name__ == '__main__':
    main()
