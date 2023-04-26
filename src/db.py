import os

from peewee import *

db_name = os.getenv('DATABASE_NAME')
db_user = os.getenv('DATABASE_USER')
db_password = os.getenv('DATABASE_PASSWORD')
db_host = os.getenv('DATABASE_HOST')
db_port = os.getenv('DATABASE_PORT')

db = PostgresqlDatabase(
    db_name,
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_password
)


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    notification_time = IntegerField()

    @staticmethod
    def get_all():
        return User.select()

    @staticmethod
    def get_by_id(user_id):
        return User.get(User.id == user_id)

    @staticmethod
    def create_user(user_id, notification_time):
        User.create(
            id=user_id,
            notification_time=notification_time
        )

    @staticmethod
    def update_notification_time(user_id, notification_time):
        user = User.get(User.id == user_id)
        user.notification_time = notification_time
        user.save()


class Class(BaseModel):
    id = IntegerField(primary_key=True)
    title = CharField()
    starts_at = TimeField()
    teacher_name = CharField()
    google_meet_link = CharField()


db.create_tables([User, Class])
