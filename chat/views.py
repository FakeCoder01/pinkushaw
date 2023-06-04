from rest_framework.response import Response
from .models import Chat
# Create your views here.


def all_user_chat(request):
    data = []
    for x in Chat.objects.order_by('sent_at'):
        is_unique = True
        if len(data) >= 10:
            break
        for y in range(len(data)):
            if data[y]["profile_id"] == x.profile.uid:
                is_unique = False
                break
        if is_unique:
            data.append({
                "profile_id" : x.profile.uid,
                "sender" : x.sender,
                "name" : x.profile.user.email,
                "message" : x.message,
                "image" : x.image,
                "sent_at" : x.sent_at
            })

     

        return Response(data)
    


def older_message(request):
    return Response()

