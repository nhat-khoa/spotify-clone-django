from django.apps import AppConfig
import mongoengine

class GroupSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.group_sessions'
    
    # def ready(self):
    #     # Ensure MongoDB connection is established
    #     from django.conf import settings
    #     if not mongoengine.connection.get_connection():
    #         mongoengine.connect(
    #             db=settings.MONGODB_NAME,
    #             host=settings.MONGODB_HOST,
    #             port=settings.MONGODB_PORT,
    #             username=settings.MONGODB_USER,
    #             password=settings.MONGODB_PASSWORD
    #         )
