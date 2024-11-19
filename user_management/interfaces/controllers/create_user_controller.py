from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from user_management.repository.user_repository_impl import UserRepositoryImpl

user_repo = UserRepositoryImpl()


@api_view(['POST'])
def create_user_controller(request):
    """
    Create a new user.
    """
    try:
        user_data = {
            "name": request.data["name"],
            "lastname": request.data["lastname"],
            "email": request.data["email"],
            "country": request.data["country"],
            "profile_image": request.data.get("profile_image"),
        }
        new_user = user_repo.create(user_data)
        return Response(
            {
                "message": "User created successfully",
                "data": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "lastname": new_user.lastname,
                    "email": new_user.email,
                    "country": new_user.country,
                    "profile_image": new_user.profile_image,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    except KeyError as e:
        return Response(
            {"message": f"Missing field: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            {"message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
