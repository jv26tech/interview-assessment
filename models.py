import re
import uuid
from exceptions import (UsernameException, PaymentException, CreditCardException,
                        FriendshipException)

class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note


class User:
    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.feed = []
        self.friends = []

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')

    def retrieve_activity(self):
        return self.feed

    def add_friend(self, new_friend):
        if new_friend in self.friends:
            raise FriendshipException('Friendship already exists.')
        elif new_friend == self:
            raise FriendshipException('Friendship with yourself is not permitted.')

        self.friends.append(new_friend)
        new_friend.friends.append(self)

        message = f"{self.username} added {new_friend.username} as friend."
        self.feed.append(message)
        new_friend.feed.append(message)


    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        if not isinstance(amount, float):
            raise PaymentException('Amount must be a float.')
        elif target == self:
            raise PaymentException('User cannot pay themselves.')

        payment = self.pay_with_card(target, amount, note) if self.balance < amount \
            else self.pay_with_balance(target, amount, note)

        message = f"{self.username} paid {target.username} ${amount:.2f} for {note}"
        self.feed.append(message)
        target.feed.append(message)

        return payment

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)


        return payment

    def pay_with_balance(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        self.add_to_balance(-amount)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment


    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass