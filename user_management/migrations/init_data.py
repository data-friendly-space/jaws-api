from django.db import migrations

from user_management.models import Permission, Role, Position, Affiliation


def create_roles_and_permissions(apps, schema_editor):
    positions_data = ["Project Manager", "Communications", "Data Expert", "Data Lead", "IM Manager", "Journalist"]
    affiliations_data = [
        {"name": "JAWS", "color": "#6941C6", "background": "#F9F5FF"},
        {"name": "DEEP", "color": "white", "background": "#008EFF"},
        {"name": "JIAF", "color": "white", "background": "#8EB5F0"}
    ]
    permissions_data = [
        {"alias": "User management", "name": "USER_MANAGEMENT", "type": "all"},
        {"alias": "Teams", "name": "TEAMS", "type": "all"},
        {"alias": "Permissions", "name": "PERMISSIONS", "type": "all"},
        {"alias": "Create workspaces", "name": "CREATE_WORKSPACE", "type": "all"},
        {"alias": "Invite facilitators to workspace", "name": "INVITE_FACILITATORS_TO_WORKSPACE", "type": "all"},
        {"alias": "Invite members to workspace", "name": "INVITE_MEMBERS_TO_WORKSPACE", "type": "all"},
        {"alias": "Invite same role to workspace", "name": "INVITE_SAME_ROLE_TO_WORKSPACE", "type": "all"},
        {"alias": "Create new analysis", "name": "CREATE_NEW_ANALYSIS", "type": "all"},
        {"alias": "Access 'Design' step", "name": "ACCESS_DESIGN_STEP", "type": "all"},
        {"alias": "Access 'Data Collation' step", "name": "ACCESS_DATA_COLLATION_STEP", "type": "all"},
        {"alias": "Access 'Data preparation' step", "name": "ACCESS_DATA_PREPARATION_STEP", "type": "all"},
        {"alias": "Access 'Description' step", "name": "ACCESS_DESCRIPTION_STEP", "type": "all"},
        {"alias": "Access 'Explanation' step", "name": "ACCESS_EXPLANATION_STEP", "type": "all"},
        {"alias": "Access 'Interpretation' step", "name": "ACCESS_INTERPRETATION_STEP", "type": "all"},
        {"alias": "Access 'Anticipation' step", "name": "ACCESS_ANTICIPATION_STEP", "type": "all"},
        {"alias": "Access 'Communication' step", "name": "ACCESS_COMMUNICATION_STEP", "type": "all"},
        {"alias": "Workspace view", "name": "WORKSPACE_VIEW", "type": "read"},
        {"alias": "Analysis view", "name": "ANALYSIS_VIEW", "type": "read"},
    ]

    permissions = {}
    for perm_data in permissions_data:
        permission, created = Permission.objects.get_or_create(**perm_data)
        permissions[perm_data["name"]] = permission

    roles_data = [
        {"alias": "General Admin", "role": "ADMIN"},
        {"alias": "Global Viewer", "role": "GLOBAL_VIEWER"},
        {"alias": "Facilitator", "role": "FACILITATOR"},
        {"alias": "Data Manager", "role": "DATA_MANAGER"},
        {"alias": "Analyst", "role": "ANALYST"},
        {"alias": "Expert", "role": "EXPERT"},
        {"alias": "Visitor", "role": "VISITOR"},
    ]

    role_permissions_map = {
        "ADMIN": list(permissions.values()),
        "GLOBAL_VIEWER": [
            permissions["WORKSPACE_VIEW"],
            permissions["ANALYSIS_VIEW"]
        ],
        "FACILITATOR": [
            permissions["CREATE_WORKSPACE"],
            permissions["INVITE_FACILITATORS_TO_WORKSPACE"],
            permissions["INVITE_MEMBERS_TO_WORKSPACE"],
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["CREATE_NEW_ANALYSIS"],
            permissions["ACCESS_DESIGN_STEP"],
            permissions["ACCESS_DATA_COLLATION_STEP"],
            permissions["ACCESS_DATA_PREPARATION_STEP"],
            permissions["ACCESS_DESCRIPTION_STEP"],
            permissions["ACCESS_EXPLANATION_STEP"],
            permissions["ACCESS_INTERPRETATION_STEP"],
            permissions["ACCESS_ANTICIPATION_STEP"],
            permissions["ACCESS_COMMUNICATION_STEP"]

        ],
        "DATA_MANAGER": [
            permissions["INVITE_MEMBERS_TO_WORKSPACE"],
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["ACCESS_DATA_COLLATION_STEP"],
            permissions["ACCESS_DATA_PREPARATION_STEP"],
            permissions["ACCESS_DESCRIPTION_STEP"],
            permissions["ACCESS_EXPLANATION_STEP"],
            permissions["ACCESS_INTERPRETATION_STEP"],
            permissions["ACCESS_ANTICIPATION_STEP"],
            permissions["ACCESS_COMMUNICATION_STEP"]
        ],
        "ANALYST": [
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["ACCESS_DESCRIPTION_STEP"],
            permissions["ACCESS_EXPLANATION_STEP"],
            permissions["ACCESS_INTERPRETATION_STEP"],
            permissions["ACCESS_ANTICIPATION_STEP"],
            permissions["ACCESS_COMMUNICATION_STEP"]
        ],
        "EXPERT": [
            permissions["INVITE_SAME_ROLE_TO_WORKSPACE"],
            permissions["ACCESS_DESCRIPTION_STEP"],
            permissions["ACCESS_EXPLANATION_STEP"],
            permissions["ACCESS_INTERPRETATION_STEP"],
            permissions["ACCESS_ANTICIPATION_STEP"],
            permissions["ACCESS_COMMUNICATION_STEP"]
        ],
        "VISITOR": [
            permissions["ANALYSIS_VIEW"]
        ],
    }

    for role_data in roles_data:
        role, created = Role.objects.get_or_create(**role_data)
        role.permissions.add(*role_permissions_map[role_data["role"]])
        role.save()

    for position in positions_data:
        Position.objects.get_or_create(name=position)

    for affiliation in affiliations_data:
        Affiliation.objects.get_or_create(affiliation)


def undo_roles(apps, schema_editor):
    Role.objects.all().delete()
    Permission.objects.all().delete()
    Position.objects.all().delete()
    Affiliation.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('user_management', '0004_permission_alias_alter_permission_name'), ]

    operations = [
        migrations.RunPython(create_roles_and_permissions, undo_roles),
    ]
