import fastapi
import requests
from fastapi import FastAPI

handler = FastAPI(title="payment_callback_handler")


@handler.post("/callback")
async def handle_callback(request: fastapi.Request) -> None:
    # Check signature exists
    request_body = await request.json()
    request_signature = request.headers.get("x-nowpayments-sig")
    if not request_signature:
        return

    # Send request to jsonrpc api
    jsonrpc_request = {
        "jsonrpc": "2.0",
        "id": "payment_handler",
        "method": "nowpayments_callback",
        "params": request_body.dict(),
    }
    headers = {"x-now-payments-sig": request_signature}
    requests.post(
        url="https://api.milf-tochka.ru/api/v1/jsonrpc",
        json=jsonrpc_request,
        headers=headers,
    )
    return
