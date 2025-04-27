from django.http import HttpResponseForbidden
from .models import FileUpload
from django.contrib.auth.models import Group

class FileUploadLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/files/upload/' and request.method == 'POST':
            if not request.user.groups.filter(name='Premium').exists():
                file_count = FileUpload.objects.filter(user=request.user).count()
                if file_count >= 5:
                    return HttpResponseForbidden("Siz faqat 5 ta fayl yuklay olasiz. Premium obuna sotib oling.")
        response = self.get_response(request)
        return response