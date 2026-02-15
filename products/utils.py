from math import floor


DENOMINATIONS = [500, 50, 20, 10, 5, 2, 1]


def calculate_bill(items):
    total_without_tax = 0
    total_tax = 0
    processed_items = []

    for product, qty in items:
        purchase_price = product.unit_price * qty
        tax_amount = purchase_price * (product.tax_percentage / 100)
        total_price = purchase_price + tax_amount

        total_without_tax += purchase_price
        total_tax += tax_amount

        processed_items.append({
            "product": product,
            "quantity": qty,
            "purchase_price": purchase_price,
            "tax_percentage": product.tax_percentage,
            "tax_amount": tax_amount,
            "total_price": total_price,
        })

    net_total = total_without_tax + total_tax
    rounded_total = floor(net_total)

    return processed_items, total_without_tax, total_tax, net_total, rounded_total


def calculate_balance_from_shop(balance):
    from .models import ShopDenomination

    denominations = ShopDenomination.objects.all().order_by('-value')

    result = {}

    for denom in denominations:
        if balance <= 0:
            break

        max_needed = balance // denom.value
        usable = min(max_needed, denom.available_count)

        if usable > 0:
            result[denom.value] = usable
            balance -= usable * denom.value

    return result, balance

