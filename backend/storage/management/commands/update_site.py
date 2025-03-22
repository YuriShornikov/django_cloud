# from django.core.management.base import BaseCommand
# from django.contrib.sites.models import Site
# import environ

# class Command(BaseCommand):
#     help = 'Update site domain and name'

#     def handle(self, *args, **kwargs):
#         env = environ.Env()
#         env.read_env('/home/aukor/django_cloud/backend/.env')

#         domain = env('DOMAIN', default='localhost:8000')
#         name = env('SITE_NAME', default='localhost')

#         site, created = Site.objects.update_or_create(
#             id=1,
#             defaults={'domain': domain, 'name': name}
#         )

#         self.stdout.write(self.style.SUCCESS(f'Updated site: {site.domain}'))
