import json
import logging
import time
from uuid import UUID

from django.http import HttpResponse, StreamingHttpResponse
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from rest_framework.decorators import api_view, permission_classes

connections = {}  # Example: { 3: [queue1, queue2], 7: [queue3] }
import jwt

SECRET_KEY = "gq35rgaerFW53T45GQ345FAdasfawf24k7iy"

logger = logging.getLogger("notification")


def send_user_notification(user_id, message):
    event = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "message": message,
    }

    if user_id in connections:
        for queue in connections[user_id]:
            queue.append(event)


def event_stream(user_id):
    queue = []

    if user_id not in connections:
        connections[user_id] = []
    connections[user_id].append(queue)

    try:
        while True:
            if queue:
                event = queue.pop(0)
                payload = f"data: {json.dumps(event)}\n\n"
                yield payload

            time.sleep(0.2)

    finally:
        connections[user_id].remove(queue)
        if not connections[user_id]:
            del connections[user_id]


def sse_notifications(request):
    # Extract the token from the query parameter
    token = request.GET.get("token")
    # If no token is provided, return an unauthorized response
    if not token:
        return HttpResponse("Unauthorized", status=401)

    try:

        logger.error(f"Token received: {token}")
        # Decode the token to get the UUID (assuming it's a JWT token)
        uuid = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("uuid")

        # If the UUID is not in the token, return unauthorized
        if not uuid:
            return HttpResponse("Unauthorized", status=401)

    except Exception as e:
        logger.error(f"Token decoding error: {str(e)}")
        return HttpResponse("Unauthorized", status=401)

    # Now create the streaming response
    response = StreamingHttpResponse(
        event_stream(uuid),  # your event stream function
        content_type="text/event-stream",
    )

    # Return the streaming response
    return response


def send_test_notification(request):
    user_id = UUID("7a82a0d7197b422c9f884fab0975359a")
    send_user_notification(user_id, "This is a test notification.")
    return HttpResponse("Test notification sent.")
