from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from users.models import User


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", {})
        text = message.get("text")
        chat = message.get("chat", {})
        chat_id = chat.get("id")
        email = message.get("from", {}).get("username")

        if text == "/start":
            try:
                user = User.objects.get(email__icontains=email)
                user.telegram_chat_id = str(chat_id)
                user.save()
                reply = "Вы успешно подписались на напоминания."
            except User.DoesNotExist:
                reply = "Пользователь с таким email не найден."

            from habits.utils import send_telegram_message

            send_telegram_message(chat_id, reply)
        return JsonResponse({"ok": True})
