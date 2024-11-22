from rest_framework.response import Response
from rest_framework import status

from analysis.repository.analysis_repository_impl import AnalysisRepositoryImpl

analysis_repository = AnalysisRepositoryImpl()

def analysis_scope_controller(request):
    """
    Create a new user.
    """
    try:
        if request.method == "GET":
            return get_scope(request)
        elif request.method == "PUT":
            return put_scope(request)
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


def get_scope(request):
    """
    Get the analysis's scope
    """
    return ""

def put_scope(request):
    """
    Update the analysis's scope
    """
    analysis_id = request.data["id"]
    analysis = {
        "id": analysis_id,
        "title": request.data.get("title"),
        "start_date": request.data.get("start_date"),
        "end_date": request.data.get("end_date"),
        "disaggregation": request.data.get("disaggregations"),
        "objetives": request.data.get("objetives"),
        "sectors": request.data.get("sectors"),
    }
    analysis_updated = analysis_repository.update(obj_id=analysis_id, data=analysis)
    return Response(
        {
            "message": "Scope updated",
            "data": {
                "id": analysis_updated.id,
                "title": analysis_updated.title,
                "start_date": analysis_updated.start_date,
                "end_date": analysis_updated.end_date,
                "disaggregations": analysis_updated.disaggregations,
                "objetives": analysis_updated.objetives,
                "sectors": analysis_updated.sectors,
                "last_access": analysis_updated.last_change,
                "created_on": analysis_updated.created_on
            },

        },
        status=status.HTTP_201_CREATED,
    )
