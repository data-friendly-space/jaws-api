"""This module contains the user service"""
from abc import ABC, abstractmethod

from user_management.contract.io.invite_user_analysis_in import InviteUserAnalysisIn
from user_management.contract.io.invite_user_in import InviteUserIn
from user_management.contract.io.sign_in_in import SignInIn
from user_management.contract.io.sign_up_in import SignUpIn
from common.helpers.query_options import QueryOptions


class UsersService(ABC):
    """User service"""

    @abstractmethod
    def get_users(self, query_options: QueryOptions):
        """Retrieves the users"""

    @abstractmethod
    def sign_up(self, sign_up_in: SignUpIn):
        """Create a new user"""

    @abstractmethod
    def sign_in(self, sign_in_in: SignInIn):
        """Log-in a user"""

    @abstractmethod
    def refresh_token(self, refresh_token):
        """Refresh the user's token"""

    @abstractmethod
    def verify_token(self, auth_header):
        """Validate the user's token"""

    @abstractmethod
    def invite_user_to_org(self, invite_user_in: InviteUserIn):
        """Invite user to an organization"""
        pass

    @abstractmethod
    def invite_user_to_analysis(self, invite_user_in: InviteUserAnalysisIn):
        """Invite user to an analysis"""
        pass
