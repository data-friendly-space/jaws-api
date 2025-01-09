'''This module contains the Organization Transfer Object'''
from typing import Dict

from common.contract.to.base_to import BaseTO


class PaginatedResultTO():
    results: list = []
    total: int = 0

    def __init__(self, results, total):
        self.results = [res.to_dict() if isinstance(res, BaseTO) else res for res in results] if results else []
        self.total = total

    def to_dict(self) -> Dict:
        """Return a dict of the object"""
        return {
            "results": self.results,
            "total": self.total,
        }
