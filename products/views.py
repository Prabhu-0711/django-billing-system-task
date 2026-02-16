from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from threading import Thread
from django.contrib import messages
from .models import Product, Purchase, PurchaseItem, ShopDenomination
from .utils import calculate_bill, calculate_balance_from_shop, DENOMINATIONS


def billing_page(request):
    if request.method == "POST":
        customer_email = request.POST.get("customer_email")
        amount_paid = float(request.POST.get("amount_paid"))

        product_ids = request.POST.getlist("product_id")
        quantities = request.POST.getlist("quantity")

        items = []

        for pid, qty in zip(product_ids, quantities):
            if pid and qty:
                product = Product.objects.get(product_id=pid)
                qty = int(qty)
                items.append((product, qty))

        processed_items, total_wo_tax, total_tax, net_total, rounded_total = calculate_bill(items)

        balance = amount_paid - rounded_total

        if balance < 0:
            print("Insufficient amount paid")
            return render(request, "billing_page.html", {
                "error": "Insufficient amount paid"
            })

        balance_denom, remaining_balance = calculate_balance_from_shop(balance)

        if remaining_balance != 0:
            print("Insufficient denominations available in shop to return balance")
            return render(request, "billing_page.html", {
                "error": "Insufficient denominations available in shop to return balance"
            })
        # Get denomination counts
        denom_counts = {}
        for d in [500, 50, 20, 10, 5, 2, 1]:
            try:
                denom_counts[d] = int(request.POST.get(f"denom_{d}") or 0)
            except ValueError:
                denom_counts[d] = 0

        for value, count in balance_denom.items():
            denom = ShopDenomination.objects.get(value=value)
            denom.available_count -= count
            denom.save()

        purchase = Purchase.objects.create(
            customer_email=customer_email,
            total_without_tax=total_wo_tax,
            total_tax=total_tax,
            net_total=net_total,
            rounded_total=rounded_total,
            amount_paid=amount_paid,
            balance_returned=balance
        )

        for item in processed_items:
            PurchaseItem.objects.create(
                purchase=purchase,
                product=item["product"],
                quantity=item["quantity"],
                purchase_price=item["purchase_price"],
                tax_amount=item["tax_amount"],
                total_price=item["total_price"]
            )

        # Async Email
        Thread(target=send_invoice_email, args=(purchase,)).start()

        return render(request, "invoice.html", {
            "purchase": purchase,
            "items": purchase.items.all(),
            "balance_denom": balance_denom,
            "remaining_denom": ShopDenomination.objects.all().order_by('-value'),
            "success": True
        })

    return render(request, "billing_page.html", {
        "denominations": DENOMINATIONS
    })

def customer_purchases(request):
    email = request.GET.get("email")
    purchases = None
    if email:
        purchases = Purchase.objects.filter(
            customer_email=email
        ).order_by('-created_at')

    return render(request, "purchases.html", {"purchases": purchases, "email": email})


def purchase_detail(request, pk):
    purchase = get_object_or_404(
        Purchase.objects.prefetch_related('items__product'),
        pk=pk
    )
    return render(request, "purchase_detail.html", {"purchase": purchase})


def send_invoice_email(purchase):
    subject = f"Invoice - Purchase #{purchase.id}"

    message = render_to_string(
        "email_invoice.html",
        {"purchase": purchase}
    )

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=None,
        to=[purchase.customer_email],
    )

    email.content_subtype = "html"  # Send HTML email
    email.send(fail_silently=False)