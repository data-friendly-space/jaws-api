"""Contains the decorator for validating if an analysis exist"""
from analysis.service.impl.analysis_service_impl import AnalysisServiceImpl


def validate_analysis_exist(function):
    """Decorator for validating if an analysis exist"""
    def wrapper(*args, **kwargs):
        analysis_id = kwargs.get("analysis_id")
        if not analysis_id:
            for arg in args:
                if isinstance(arg, dict) and "analysis_id" in arg:
                    analysis_id = arg["analysis_id"]
                    break
        if not analysis_id:
            raise ValueError("Analysis id required")
        analysis_service = AnalysisServiceImpl()
        analysis_service.get_analysis_by_id(analysis_id)
        return function(*args, **kwargs)
    return wrapper
