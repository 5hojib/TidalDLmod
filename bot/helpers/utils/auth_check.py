from bot import Config
from bot.helpers.translations import lang
from bot.helpers.database.postgres_impl import users_db, admins_db, chats_db, user_settings

allowed_chats = []
allowed_users = []
admins = []

# NOOB WAY TO HANDLE BOTH ENV AND DB XD

async def get_chats(return_msg=False):
    # CHATS 
    database_chats = chats_db.get_chats()
    for chat in Config.AUTH_CHAT:
        if chat not in allowed_chats:
            allowed_chats.append(chat)
    for chat in database_chats:
        if chat != None and chat[0] not in allowed_chats and chat[0] != None:
            allowed_chats.append(chat[0])
    # ADMINS
    database_admins = admins_db.get_admins()
    for admin in Config.ADMINS:
        if admin not in admins:
            admins.append(admin)
    for admin in database_admins:
        if admin != None and admin[0] not in admins and admin[0] != None:
            admins.append(admin[0])
    # USERS
    if Config.IS_BOT_PUBLIC != "True":
        database_users = users_db.get_users()
        for user in Config.AUTH_USERS:
            if user not in allowed_users:
                allowed_users.append(user)
        for user in database_users:
            if (
                user != None
                and user[0] not in allowed_users
                and user[0] != None
            ):
                allowed_users.append(user[0])

    if return_msg:
        msg = "<b>ALLOWED CHATS</b>"
        for chat in allowed_chats:
            msg += f"\n<code>{chat}</code>"

        msg += "\n\n<b>ALLOWED USERS</b>"
        if Config.IS_BOT_PUBLIC == "True":
            msg += "\nAllowed For Everyone"
        try:
            for user in allowed_users:
                msg += f"\n<code>{user}</code>"
        except:
            pass

        msg += "\n\n<b>ADMINS</b>"
        for admin in admins:
            msg += f"\n<code>{admin}</code>"

        return msg

async def check_id(id=None, message=None, restricted=False):
    all_list = allowed_chats + allowed_users + admins
    if restricted:
        return id in admins
        # Seperating Group and PM
    id = (
        message.chat.id
        if message.from_user.id != message.chat.id
        else message.from_user.id
    )
    if Config.ANIT_SPAM_MODE == "True":
        if check := user_settings.get_var(id, "ON_TASK"):
            await message.reply_text(lang.select.ANTI_SPAM_WAIT)
            return False          

    return Config.IS_BOT_PUBLIC == "True" or id in all_list




    


    
