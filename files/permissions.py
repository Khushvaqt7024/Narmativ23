from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from files.models import FileUpload

class Command(BaseCommand):
    help = 'Setup groups and permissions'

    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        moderator_group, _ = Group.objects.get_or_create(name='Moderator')
        user_group, _ = Group.objects.get_or_create(name='User')
        premium_group, _ = Group.objects.get_or_create(name='Premium')

        # Get content type for FileUpload
        content_type = ContentType.objects.get_for_model(FileUpload)

        # Create permissions
        add_permission = Permission.objects.get(codename='add_fileupload', content_type=content_type)
        delete_permission = Permission.objects.get(codename='delete_fileupload', content_type=content_type)

        # Assign permissions to groups
        admin_group.permissions.set([add_permission, delete_permission])
        moderator_group.permissions.set([add_permission, delete_permission])
        user_group.permissions.set([add_permission])