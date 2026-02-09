from exceptions import (UsernameException, PaymentException, CreditCardException, FriendshipException,
                        BalanceException)
from models import User, Payment


class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        if username is None:
            raise UsernameException("Must have a username to make a payment.")
        elif not isinstance(username, str):
            raise UsernameException("Username must be a string.")
        elif balance is None or balance < 0:
            raise BalanceException("Balance must be a non-negative number.")
        elif credit_card_number is None:
            raise CreditCardException("Must have a credit card to make a payment.")

        user = User(username)
        user.add_to_balance(balance)
        user.add_credit_card(credit_card_number)

        return user


    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        if feed is not None:
            for line in feed:
                print(line)

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")

            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_activity()
        venmo.render_feed(feed)

        bobby.add_friend(carol)


if __name__ == "__main__":
    MiniVenmo.run()