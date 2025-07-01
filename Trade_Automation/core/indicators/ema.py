class EMA:
    def __init__(self, period: int):
        self.period = period
        self.k = 2 / (period + 1)
        self._value: float | None = None

    def update(self, price: float) -> float:
        self._value = price if self._value is None else (
            price * self.k + self._value * (1 - self.k)
        )
        return self._value

    @property
    def value(self) -> float | None:
        return self._value
