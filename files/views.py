from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from .models import FileUpload
from django.contrib import messages

class FileListView(LoginRequiredMixin, ListView):
    model = FileUpload
    template_name = 'files/file_list.html'
    context_object_name = 'files'

    def get_queryset(self):
        return FileUpload.objects.filter(user=self.request.user)

class FileUploadView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = FileUpload
    fields = ['title', 'file']
    template_name = 'files/file_upload.html'
    success_url = reverse_lazy('file_list')
    permission_required = 'files.add_fileupload'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FileDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = FileUpload
    template_name = 'files/file_confirm_delete.html'
    success_url = reverse_lazy('file_list')
    permission_required = 'files.delete_fileupload'

    def get_queryset(self):
        return FileUpload.objects.filter(user=self.request.user)