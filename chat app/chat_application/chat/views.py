from django.shortcuts import render

# Create your views he# chat/views.py
from django.shortcuts import render, redirect
from .models import User, Message

def index(request):
    if request.user.is_authenticated:
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chat/index.html', {'users': users})
    return redirect('login')

def chat(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user
    chat_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        (models.Q(from_user=user) & models.Q(to_user=chat_user)) |
        (models.Q(from_user=chat_user) & models.Q(to_user=user))
    ).order_by('timestamp')

    return render(request, 'chat/chat.html', {'user': user, 'chat_user': chat_user, 'messages': messages})
re.
