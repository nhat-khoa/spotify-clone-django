# from django_mongoengine import Document, EmbeddedDocument, fields
# import datetime

# class Location(EmbeddedDocument):
#     """Embedded document for location data"""
#     country = fields.StringField(max_length=2)  # Country code
#     city = fields.StringField()

# class UserStream(Document):
#     """Document for tracking user streaming history"""
#     user_id = fields.StringField(required=True)
#     track_id = fields.StringField(required=True)
#     listened_duration_ms = fields.IntField(required=True)
#     completed = fields.BooleanField(default=False)
#     location = fields.EmbeddedDocumentField(Location)
#     timestamp = fields.DateTimeField(default=datetime.datetime.now)
    
#     meta = {
#         'collection': 'user_streams',
#         'indexes': [
#             'user_id',
#             'track_id',
#             'timestamp',
#             {'fields': ['user_id', 'timestamp'], 'sparse': False}
#         ]
#     }