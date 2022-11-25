PERMISSIONS = (
    ('create_user', 'Create User'),
    ('update_user', 'Update User'),
    ('view_hazards', 'View Hazards'),
    ('delete_hazards', 'Delete Hazards'),
)

JSON_PERMISSIONS = [{'name': key, 'value': value} for value, key in PERMISSIONS]

