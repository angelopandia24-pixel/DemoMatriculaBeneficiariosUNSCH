from decimal import Decimal, ROUND_HALF_UP
CENTAVO = Decimal("0.01")
def dinero(valor: Decimal | str | int | float) -> Decimal:
    return Decimal(str(valor)).quantize(CENTAVO, rounding=ROUND_HALF_UP)
