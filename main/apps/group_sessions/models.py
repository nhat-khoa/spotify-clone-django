# from django_mongoengine import Document, EmbeddedDocument, fields
# from django.conf import settings
# import datetime

# class QueueItem(EmbeddedDocument):
#     """Embedded document for queue items in a group session"""
#     track_id = fields.StringField(required=True)
#     track_name = fields.StringField(required=True)
#     artist = fields.StringField(required=True)
#     thumbnail = fields.StringField()  # URL to thumbnail

# class SessionMember(EmbeddedDocument):
#     """Embedded document for session members"""
#     user_id = fields.StringField(required=True)
#     joined_at = fields.DateTimeField(default=datetime.datetime.now)

# class GroupSession(Document):
#     """Document for group listening sessions"""
#     host_user_id = fields.StringField(required=True)
#     session_code = fields.StringField(required=True, unique=True, max_length=10)
#     status = fields.StringField(choices=('active', 'ended'), default='active')
#     is_active = fields.BooleanField(default=True)
#     queue = fields.EmbeddedDocumentListField(QueueItem, default=[])
#     members = fields.EmbeddedDocumentListField(SessionMember, default=[])
#     created_at = fields.DateTimeField(default=datetime.datetime.now)
#     ended_at = fields.DateTimeField()

#     meta = {
#         'collection': 'group_sessions',
#         'indexes': [
#             'session_code',
#             'host_user_id',
#             'created_at',
#             {'fields': ['is_active', 'status'], 'sparse': False}
#         ]
#     }