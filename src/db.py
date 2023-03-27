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
    chat_id = IntegerField()
    notification_time = IntegerField()

    def get_all():
        return User.select()

    def get_by_id(id):
        return User.get(User.id == id)

    def create_user(id, chat_id, notification_time):
        User.create(
            id=id,
            chat_id=chat_id,
            notification_time=notification_time
        )

    def update_notification_time(id, notification_time):
        user = User.get(User.id == id)
        user.notification_time = notification_time
        user.save()


db.create_tables([User])