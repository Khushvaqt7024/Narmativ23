from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create default groups and permissions'
    def handle(self, *args, **options):
        groups = ['Admin', 'Moderator', 'User']
        for name in groups:
            group, created = Group.objects.get_or_create(name=name)
            if name == 'Admin':
                group.permissions.set(Permission.objects.all())
            elif name == 'Moderator':
                perms = Permission.objects.filter(codename__in=['add_user', 'change_user', 'delete_user'])
                group.permissions.set(perms)
            group.save()
        self.stdout.write(self.style.SUCCESS('Groups created.'))