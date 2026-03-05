from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'List all inactive user accounts'

    def handle(self, *args, **options):
        inactive_users = User.objects.filter(is_active=False)
        
        if not inactive_users:
            self.stdout.write('No inactive users found.')
            return
        
        self.stdout.write(self.style.SUCCESS(f'Found {inactive_users.count()} inactive users:'))
        for user in inactive_users:
            groups = list(user.groups.values_list('name', flat=True))
            self.stdout.write(f'  - {user.username} ({user.email}) - Groups: {groups}')
