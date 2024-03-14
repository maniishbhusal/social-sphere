from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import ChatConversation
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))

    return render(request, 'ai_app/index.html')

# @login_required(login_url='login')
def artificialIntelligenceView(request):
    if not request.user.is_authenticated:
        return redirect(reverse('user_login'))
    
    # if request.method == 'POST':
    #     prompt = request.POST.get('prompt')
    #     user = request.user
    #     conversation = ChatConversation(user=user, prompt=prompt)
    #     conversation.save()
    #     return render(request, 'ai_app/artificial_intelligence.html', {'prompt': prompt})

        # return redirect(reverse('ai_app:ai_response', args=[prompt]))

    return render(request, 'ai_app/artificial_intelligence.html')