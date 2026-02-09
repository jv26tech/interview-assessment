import unittest
from main import MiniVenmo
from exceptions import (UsernameException, PaymentException, CreditCardException, FriendshipException,
                        BalanceException)

class TestUser(unittest.TestCase):
    def setUp(self):
        self.venmo = MiniVenmo()

    def test_username(self):
        with self.assertRaises(UsernameException):
            self.venmo.create_user("Ven", 5.00, "4111111111111111")

    def test_username_none(self):
        with self.assertRaises(UsernameException):
            self.venmo.create_user(None, 5.00, "4111111111111111")

    def test_username_non_a_string(self):
        with self.assertRaises(UsernameException):
            self.venmo.create_user(0, 5.00, "4111111111111111")

    def test_balance(self):
        with self.assertRaises(BalanceException):
            self.venmo.create_user("Venmo", -5.00, "4111111111111111")

    def test_credit_card(self):
        with self.assertRaises(CreditCardException):
            self.venmo.create_user("Venmo", 5.00, "1111111111111111")

    def test_credit_card_none(self):
        with self.assertRaises(CreditCardException):
            self.venmo.create_user("Venmo", 10.00, None)

    def test_balance_none(self):
        with self.assertRaises(BalanceException):
            self.venmo.create_user("Venmo", None, "4111111111111111")

    def test_friendship_with_myself(self):
        with self.assertRaises(FriendshipException):
            user1 = self.venmo.create_user("Venmo", 10.00, "4111111111111111")

            user1.add_friend(user1)

    def test_friendship_twice(self):
        with self.assertRaises(FriendshipException):
            user1 = self.venmo.create_user("Venmo", 10.00, "4111111111111111")
            user2 = self.venmo.create_user("VenmoTwo", 10.00, "4111111111111111")
            user1.add_friend(user2)
            user1.add_friend(user2)

    def test_create_user(self):
        user = self.venmo.create_user("Venmo", 5.00, "4111111111111111")
        self.assertEqual(user.username, "Venmo")
        self.assertEqual(user.balance, 5.00)
        self.assertEqual(user.credit_card_number, "4111111111111111")

    def test_pay(self):
        user1 = self.venmo.create_user("user1", 5.00, "4111111111111111")
        user2 = self.venmo.create_user("user2", 10.00, "4242424242424242")

        user1.pay(user2, 5.00, "Coffee")

        self.assertEqual(user1.balance, 0.00)
        self.assertEqual(user2.balance, 15.00)

    def test_pay_negative(self):
        with self.assertRaises(PaymentException):
            user1 = self.venmo.create_user("user1", 5.00, "4111111111111111")
            user2 = self.venmo.create_user("user2", 10.00, "4242424242424242")

            user1.pay(user2, -5.00, "Coffee")

    def test_pay_myself(self):
        with self.assertRaises(PaymentException):
            user1 = self.venmo.create_user("user1", 5.00, "4111111111111111")

            user1.pay(user1, 10.00, "Coffee")

    def test_pay_not_float(self):
        user1 = self.venmo.create_user("user1", 5.00, "4111111111111111")
        user2 = self.venmo.create_user("user2", 10.00, "4242424242424242")
        with self.assertRaises(PaymentException):
            user1.pay(user2, "5.00", "Coffee")

    def test_pay_without_balance(self):
        user1 = self.venmo.create_user("user1", 5.00, "4111111111111111")
        user2 = self.venmo.create_user("user2", 10.00, "4242424242424242")

        user1.pay(user2, 10.00, "Lunch")

        self.assertEqual(user1.balance, 5.00)
        self.assertEqual(user2.balance, 20.00)

    def test_complete_run(self):
        self.assertIsNone(self.venmo.run())


if __name__ == '__main__':
    unittest.main()