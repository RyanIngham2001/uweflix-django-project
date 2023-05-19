def get_user_permissions(request):
    """
    Returns:
    perms (str): The user's permission level, as a string.
    """
    perms = None
    if request.user.is_authenticated:
        if request.user.groups.filter(name="admin").exists():
            perms = "4"
        elif (
            request.user.groups.filter(name="cinema_manager").exists()
            or request.user.groups.filter(name="cinema_manager_temp").exists()
        ):
            perms = "3"
        elif request.user.groups.filter(name="account_manager").exists():
            perms = "2"
        elif request.user.is_rep:
            perms = "1"
        else:
            perms = "0"
    else:
        perms = "-1"

    return perms


def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
