import os
import uuid

from django.contrib.sites import requests
from dotenv import load_dotenv
from rest_framework.response import Response

from config import settings

load_dotenv()
root = os.getenv("BASE_ROUTE")


def initiate_payment(amount, email, pending_id, user):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {settings.FLW_SEC_KEY}"
    }
    first_name = user.first_name
    last_name = user.last_name
    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "NGN",
        "redirect_url": f"{root}/api/pending/confirm_payment/?p_id=" + pending_id,
        "meta": {
            "consumer_id": 23,
            "consumer_mac": "92a3-912ba-1192a"
        },
        "customer": {
            "email": email,
            "phonenumber": "080****4528",
            "name": f"{last_name} {first_name}"
        },
        "customizations": {
            "title": "Success Air",
            "logo": "https://jetinternational.com/wp-content/uploads/2016/11/iStock-177708665-5.jpg"

        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        return Response({"error": str(err)}, status=500)