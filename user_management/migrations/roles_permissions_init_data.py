from django.db import migrations

from user_management.models import Permission, Role


def create_roles_and_permissions(apps, schema_editor):
    permissions_data = [
        {"alias": "User management", "name": "USER_MANAGEMENT", "type": "all"},
        {"alias": "Teams", "name": "TEAMS", "type": "all"},
        {"alias": "Permissions", "name": "PERMISSIONS", "type": "all"},
        {"alias": "Create workspaces", "name": "CREATE_WORKSPACE", "type": "write"},
        {"alias": "Invite facilitators to workspace", "name": "INVITE_FACILITATORS_TO_WORKSPACE", "type": "write"},
        {"alias": "Invite members to workspace", "name": "INVITE_MEMBERS_TO_WORKSPACE", "type": "write"},
        {"alias": "Invite same role to workspace", "name": "INVITE_SAME_ROLE_TO_WORKSPACE", "type": "write"},
        {"alias": "Create", "name": "CREATE_NEW_ANALYSIS", "type": "write"},
        {"alias": "Access design step", "name": "ACCESS_DESIGN_STEP", "type": "read"},
        {"alias": "Access data collation step", "name": "ACCESS_DATA_COLLATION_STEP", "type": "read"},
    ]

    permissions = {}
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(**perm_data)
        permissions[perm_data["name"]] = permission

    roles_data = [
        {"alias": "Admin", "role": "ADMIN"},
        {"alias": "Facilitator", "role": "FACILITATOR"},
        {"alias": "Data Manager", "role": "DATA_MANAGER"},
        {"alias": "Analyst", "role": "ANALYST"},
        {"alias": "Expert", "role": "EXPERT"},
        {"alias": "Visitor", "role": "VISITOR"},
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

    for role_data in roles_data:
        role, created = Role.objects.get_or_create(**role_data)
        role.permissions.add(*role_permissions_map[role_data.get("name")])
        print(role)
        role.save()


def undo_roles(apps, schema_editor):
    Role.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('user_management', '0001_initial'), ]

    operations = [
        migrations.RunPython(create_roles_and_permissions, undo_roles),
    ]
