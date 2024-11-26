from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl
from app.core.api_response import api_response

analysis_repository = AnalysisRepositoryImpl()

@api_view(["GET"])
def get_analysis_scope_controller(request, id):
    """
    Retrieve an analysis scope.
    """
    try:
        return api_response(id, request.method, status.HTTP_200_OK)
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

