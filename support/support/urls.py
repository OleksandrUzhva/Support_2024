import httpx
from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
async def currency(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = request.POST
        currency_from = data.get("from_currency")
        currency_to = data.get("to_currency")

        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_from}&to_currency={currency_to}&apikey=D5G28HSZ0FWYD5WQ"

        async with httpx.AsyncClient() as client:
            response: httpx.Response = await client.get(url)
            rate = response.json()

        return JsonResponse({"rate": rate})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("currency", view=currency),
]
