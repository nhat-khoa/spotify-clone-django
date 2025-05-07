from django.urls import path
from .views import db_metadata_view, multi_table_data_view, chat_with_data

urlpatterns = [
    path('db-metadata/', db_metadata_view, name='db_metadata'),
    path("multi-table-data/", multi_table_data_view),
    path("chat-bot/", chat_with_data, name="ollama")
]
