from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from datetime import datetime, timedelta

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = datetime.fromisoformat(last_activity)
                if datetime.now() - last_activity > timedelta(minutes=15):
                    logout(request)
                    return redirect(reverse('accounts:login'))
            request.session['last_activity'] = datetime.now().isoformat()
        return self.get_response(request)