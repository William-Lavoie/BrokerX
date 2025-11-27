import json
import time
from uuid import UUID

from django.http import HttpResponse, StreamingHttpResponse

connections = {}  # Example: { 3: [queue1, queue2], 7: [queue3] }


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
    user_id = UUID("7a82a0d7197b422c9f884fab0975359a")

    response = StreamingHttpResponse(
        event_stream(user_id),
        content_type="text/event-stream",
    )

    return response


def send_test_notification(request):
    user_id = UUID("7a82a0d7197b422c9f884fab0975359a")
    send_user_notification(user_id, "This is a test notification.")
    return HttpResponse("Test notification sent.")
