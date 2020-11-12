# -*- coding: utf-8 -*-
from unittest import TestCase, main

from app import db, create_app
from app.models import User

import logging
import sys

app = create_app(environment="testing")
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


class TestApp(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.app_ctx = app.app_context()
        self.app_ctx.push()
        db.create_all()
        user = User(username="admin", password="123")
        user.save()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()

    def register(self, username, password="password", confirmation="password"):
        return self.client.post(
            "/register",
            data=dict(
                username=username,
                password=password,
                password_confirmation=confirmation,
            ),
            follow_redirects=True,
        )

    def login(self, user_id, password="123"):
        return self.client.post(
            "/login",
            data=dict(user_id=user_id, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get("/logout", follow_redirects=True)

    def test_index_page(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_registration_page(self):
        response = self.client.get("/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_registration(self):
        self.login("admin")
        # Valid data should register successfully.
        answer = "Вы зарегистрированы!".encode("utf-8")
        response = self.register("alice")
        self.assertIn(answer, response.data)
        # Password/Confirmation mismatch should fail.
        answer = "Ошибка ввода данных!".encode("utf-8")
        response = self.register("bob", "password", "Password")
        self.assertIn(answer, response.data)
        # Existing username registration should fail.
        response = self.register("alice")
        self.assertIn(answer, response.data)

    def test_new_user_login(self):
        self.login("admin")
        # New user will be automatically logged in.
        response = self.register("sam")
        answer = "Вы зарегистрированы!".encode("utf-8")
        self.assertIn(answer, response.data)
        # Should successfully logout the currently logged in user.
        answer = "Вы вышли".encode("utf-8")
        response = self.logout()
        self.assertIn(answer, response.data)

    def test_incorrect_login(self):
        # Incorrect login credentials should fail.
        answer = "Неверный пользователь или пароль".encode("utf-8")
        response = self.login("admin", "somepassword")
        self.assertIn(answer, response.data)

    def test_login(self):
        # Correct credentials should login
        answer = "Успешная авторизация".encode("utf-8")
        response = self.login("admin")
        self.assertIn(answer, response.data)
        self.logout()


if __name__ == "__main__":
    main()

    # log = logging.getLogger("TestLog")
    # log.debug(response.data.decode('utf-8'))
    # log.debug(answer)
