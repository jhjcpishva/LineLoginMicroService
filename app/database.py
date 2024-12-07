from datetime import datetime
from typing import Optional, cast

import pocketbase.utils
from pocketbase import PocketBase
from pocketbase.models.utils import BaseModel

import config


class LoginRecord(BaseModel):
    nonce: str
    redirect_url: Optional[str] = None
    session: Optional[str] = None


class SessionRecord(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    expire: str
    name: str
    picture: Optional[str] = None


class MyPbDb:
    pb: PocketBase

    def __init__(self):
        self.pb = PocketBase(config.PB_HOST)
        self.pb.admins.auth_with_password(config.PB_ADMIN, config.PB_PASSWORD)

    def get_nonce(self, nonce: str) -> LoginRecord:
        login_db = self.pb.collection("login")
        return login_db.get_first_list_item(f'nonce = "{nonce}"')

    def get_nonce_by_id_or_none(self, _id: str) -> LoginRecord | None:
        try:
            return cast(LoginRecord, self.pb.collection("login").get_one(_id))
        except pocketbase.utils.ClientResponseError as e:
            # expecting for "The requested resource wasn't found."
            if e.status != 404:
                # unexpected error
                raise e
        return None

    def clear_existing_nonce(self, nonce: str):
        login_db = self.pb.collection("login")
        try:
            # とりあえず上書きして動けばいい場合
            while True:
                item = login_db.get_first_list_item(f'nonce = "{nonce}"')
                login_db.delete(item.id)
        except pocketbase.utils.ClientResponseError as e:
            # expecting for "The requested resource wasn't found."
            if e.status != 404:
                # unexpected error
                raise e
        return None

    def create_new_login_nonce(self, nonce: str, redirect_url: str) -> LoginRecord:
        return cast(LoginRecord, self.pb.collection("login").create({
            "nonce": nonce,
            "redirect_url": redirect_url,
        }))

    def update_login_nonce(self, record: LoginRecord) -> LoginRecord:
        login_db = self.pb.collection("login")
        return cast(LoginRecord, login_db.update(record.id, {
            "nonce": record.nonce,
            "redirect_url": record.redirect_url,
            "session": record.session,
        }))

    def create_session(self, access_token: str, refresh_token: str, user_id: str, expire: datetime, name: str,
                       picture: Optional[str] = None) -> SessionRecord:
        return cast(SessionRecord, self.pb.collection('sessions').create({
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user_id,
            "expire": expire.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "name": name,
            "picture": picture,
        }))

    def get_session_or_none(self, _id: str) -> SessionRecord | None:
        try:
            return cast(SessionRecord, self.pb.collection("sessions").get_one(_id))
        except pocketbase.utils.ClientResponseError as e:
            # expecting for "The requested resource wasn't found."
            if e.status != 404:
                # unexpected error
                raise e
        return None

    def update_session(self, record: SessionRecord) -> SessionRecord:
        sessions_db = self.pb.collection("sessions")
        return cast(SessionRecord, sessions_db.update(record.id, {
            "access_token": record.access_token,
            "refresh_token": record.refresh_token,
            "user_id": record.user_id,
            "expire": record.expire,
            "name": record.name,
            "picture": record.picture,
        }))
