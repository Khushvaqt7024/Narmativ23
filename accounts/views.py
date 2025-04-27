from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import User
import requests
from decouple import config
from django.contrib import messages
from django.views import View

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Assign 'User' group to new users
        from django.contrib.auth.models import Group
        user_group, _ = Group.objects.get_or_create(name='User')
        self.object.groups.add(user_group)
        return response

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

class GoogleLoginView(View):
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={config('GOOGLE_OAUTH2_CLIENT_ID')}&"
            f"redirect_uri={config('GOOGLE_OAUTH2_REDIRECT_URI')}&"
            "response_type=code&"
            "scope=email%20profile&"
            "access_type=offline"
        )
        return redirect(google_auth_url)

class GoogleCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        if not code:
            messages.error(request, "Google authentication failed.")
            return redirect('login')

        # Exchange code for access token
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            'code': code,
            'client_id': config('GOOGLE_OAUTH2_CLIENT_ID'),
            'client_secret': config('GOOGLE_OAUTH2_CLIENT_SECRET'),
            'redirect_uri': config('GOOGLE_OAUTH2_REDIRECT_URI'),
            'grant_type': 'authorization_code',
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        if 'access_token' not in token_json:
            messages.error(request, "Failed to obtain access token.")
            return redirect('login')

        # Get user info
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f"Bearer {token_json['access_token']}"}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Create or get user
        email = user_info.get('email')
        user, created = CustomUser.objects.get_or_create(email=email, defaults={'email': email})
        if created:
            user.set_unusable_password()
            user.save()
            from django.contrib.auth.models import Group
            user_group, _ = Group.objects.get_or_create(name='User')
            user.groups.add(user_group)

        login(request, user)
        return redirect('home')

class AdminView(PermissionRequiredMixin, View):
    permission_required = 'auth.view_user'

    def get(self, request):
        return render(request, 'accounts/admin_page.html', {'message': 'Welcome, Admin!'})