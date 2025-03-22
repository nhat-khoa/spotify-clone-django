from mongoengine import Document, EmbeddedDocument, fields
import datetime

class Location(EmbeddedDocument):
    """Embedded document for user location"""
    country = fields.StringField()
    city = fields.StringField()

class UserStream(Document):
    """User streaming history document"""
    user_id = fields.StringField(required=True)
    track_id = fields.StringField(required=True)
    listened_duration_ms = fields.IntField(required=True)
    completed = fields.BooleanField(default=False)
    location = fields.EmbeddedDocumentField(Location)
    timestamp = fields.DateTimeField(default=datetime.datetime.now)
    
    meta = {
        'collection': 'user_streams',
        'indexes': [
            'user_id',
            'track_id',
            {'fields': ['timestamp'], 'expireAfterSeconds': 7776000}  # Optional: expire after 90 days
        ]
    }