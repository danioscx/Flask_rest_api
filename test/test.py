import asyncio
import json

from flask_testing import TestCase

from app import app_test
from src.databases import db


class TestDatabase(TestCase):
    TESTING = True

    def create_app(self):
        self.apps = app_test()
        self.apps.app_context().push()
        return self.apps


class SignUpTest(TestDatabase):
    jwt_token = None
    is_signin = False

    def test_create_database(self):
        db.create_all(app=self.app)

    def test_signup(self):
        response = self.client.post(
            "/api/v1/signUp",
            data=json.dumps(dict(username="dani", email="test@test.com", password="123456")),
            content_type="application/json"
        )
        try:
            self.assertEqual(response.status_code, 200)
        except Exception:
            self.assertEqual(response.status_code, 409)

    async def run_signin(self):
        response = self.client.post(
            "/api/v1/signIn",
            data=json.dumps(dict(email="test@test.com", password="123456")),
            content_type="application/json"
        )
        self.jwt_token = response.json["token"]
        self.assertEqual(response.status_code, 200)

    async def run_fetch(self):
        response = self.client.get(
            "api/v1/welcome",
            headers={"Authorization": "Bearer " + self.jwt_token}
        )
        self.assertEqual(response.status_code, 200)

    async def run_clean_database(self):
        db.drop_all(app=self.app)

    async def main(self):
        await self.run_signin()
        await asyncio.sleep(2)
        await self.run_fetch()
        await asyncio.sleep(3)
        await self.run_clean_database()

    def test_jwt(self):
        asyncio.run(self.main())



