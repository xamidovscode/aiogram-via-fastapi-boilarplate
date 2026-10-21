from enum import Enum


class UserRoles(str, Enum):
    admin = 'admin'
    user = 'user'
    super_admin = 'super_admin'