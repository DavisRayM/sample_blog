"""
Tokens Module for Users
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Account Activation Token Generator
    """

    def _make_hash_value(self, user, timestamp):
        """
        Modified _make_hash_value method
        """
        return (
            str(user.pk) + str(timestamp) + str(
                user.userprofile.email_confirmed))
