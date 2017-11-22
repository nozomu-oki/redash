from tests import BaseTestCase

from redash.models import User

class TestUserUpdateGroupAssignments(BaseTestCase):
    def test_default_group_always_added(self):
        user = self.factory.create_user()

        user.update_group_assignments(["g_unknown"])
        self.assertItemsEqual([user.org.default_group.id], user.group_ids)

    def test_update_group_assignments(self):
        user = self.factory.user
        new_group = self.factory.create_group(name="g1")

        user.update_group_assignments(["g1"])
        self.assertItemsEqual([user.org.default_group.id, new_group.id], user.group_ids)


class TestUserFindByEmail(BaseTestCase):
    def test_finds_users(self):
        user = self.factory.create_user(email='test@example.com')
        user2 = self.factory.create_user(email='test@example.com', org=self.factory.create_org())

        users = User.find_by_email(user.email)
        self.assertIn(user, users)
        self.assertIn(user2, users)

    def test_finds_users_case_insensitive(self):
        user = self.factory.create_user(email='test@example.com')

        users = User.find_by_email('test@EXAMPLE.com')
        self.assertIn(user, users)


class TestUserGetByEmailAndOrg(BaseTestCase):
    def test_get_user_by_email_and_org(self):
        user = self.factory.create_user(email='test@example.com')

        found_user = User.get_by_email_and_org(user.email, user.org)
        self.assertEqual(user, found_user)

    def test_get_user_by_email_and_org_case_insensitive(self):
        user = self.factory.create_user(email='test@example.com')

        found_user = User.get_by_email_and_org("TEST@example.com", user.org)
        self.assertEqual(user, found_user)
