from django.db import migrations

from user_management.models import Permission, Role


def create_roles_and_permissions(apps, schema_editor):
    permissions_data = [
        {"name": "USER_MANAGEMENT", "type": "all"},
        {"name": "TEAMS", "type": "all"},
        {"name": "PERMISSIONS", "type": "all"},
        {"name": "CREATE_WORKSPACE", "type": "write"},
        {"name": "INVITE_FACILITATORS_TO_WORKSPACE", "type": "write"},
        {"name": "INVITE_MEMBERS_TO_WORKSPACE", "type": "write"},
        {"name": "INVITE_SAME_ROLE_TO_WORKSPACE", "type": "write"},
        {"name": "CREATE_NEW_ANALYSIS", "type": "write"},
        {"name": "ACCESS_DESIGN_STEP", "type": "read"},
        {"name": "ACCESS_DATA_COLLATION_STEP", "type": "read"},
    ]

    permissions = {}
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(**perm_data)
        permissions[perm_data["name"]] = permission

    roles_data = [
        "ADMIN",
        "FACILITATOR",
        "DATA_MANAGER",
        "ANALYST",
        "EXPERT",
        "VISITOR",
    ]

    role_permissions_map = {
        "ADMIN": list(permissions.values()),
        "FACILITATOR": [
            permissions["CREATE_WORKSPACE"],
            permissions["INVITE_FACILITATORS_TO_WORKSPACE"],
            permissions["INVITE_MEMBERS_TO_WORKSPACE"],
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["CREATE_NEW_ANALYSIS"],
            permissions["ACCESS_DESIGN_STEP"],
            permissions["ACCESS_DATA_COLLATION_STEP"],
        ],
        "DATA_MANAGER": [
            permissions["INVITE_MEMBERS_TO_WORKSPACE"],
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["ACCESS_DATA_COLLATION_STEP"],
        ],
        "ANALYST": [
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
        ],
        "EXPERT": [
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
        ],
        "VISITOR": [],
    }

    for role_name in roles_data:
        role, created = Role.objects.get_or_create(role=role_name)
        role.permissions.add(*role_permissions_map[role_name])
        print(role)
        role.save()


class Migration(migrations.Migration):
    dependencies = [('user_management', '0001_initial'), ]

    operations = [
        migrations.RunPython(create_roles_and_permissions),
    ]
