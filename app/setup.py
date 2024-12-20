from pocketbase import PocketBase
import config

pb = PocketBase(config.PB_HOST)
r = pb.admins.auth_with_password(config.PB_ADMIN, config.PB_PASSWORD)
print("login", r.is_valid)

session_table = pb.collections.create(
    {
        "name": "sessions",
        "type": "base",
        "schema": [
            {
                "name": "access_token",
                "type": "text",
                "required": True,
            },
            {
                "name": "refresh_token",
                "type": "text",
                "required": True,
            },
            {
                "name": "user_id",
                "type": "text",
                "required": True,
            },
            {
                "name": "name",
                "type": "text",
                "required": False,
            },
            {
                "name": "picture",
                "type": "text",
                "required": False,
            },
            {
                "name": "expire",
                "type": "date",
                "required": True,
            }
        ],
    }
)

login_table = (pb.collections.create(
    {
        "name": "login",
        "type": "base",
        "schema": [
            {
                "name": "nonce",
                "type": "text",
                "required": True,
            },
            {
                "name": "redirect_url",
                "type": "text",
                "required": False,
            },
            {
                "name": "session",
                "type": "relation",
                "options": {
                    "collectionId": session_table.id,
                    "cascadeDelete": False,
                    "minSelect": None,
                    "maxSelect": 1,
                    "displayFields": None
                }
            }
        ],
    }
))

print(session_table, login_table)