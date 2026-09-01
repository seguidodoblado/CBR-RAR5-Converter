from collections.abc import Iterable
from .conversion import ConversionService
from .models import ConversionItem

class ConversionQueue:
    def __init__(self, service: ConversionService):
        self.service = service
    def run(self, items: Iterable[ConversionItem]) -> list[ConversionItem]:
        return [self.service.convert(item) for item in items]
