from typing import Dict, Any


class Report:
    def __init__(self, result: Dict[str, Any]):
        self.analysis = result["analysis"]

