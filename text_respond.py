import telegram, logging, json
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# https://api.telegram.org/bot/getupdates
# context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

TOKEN: str = ""
BOT = telegram.Bot(token=TOKEN)
PATH: str = os.getcwd()

json = {
    "username": "soe",
    "user_id": "asd1231",
    "message": "awdqwerhlwed",
    "message_type": "command",
    "discription": "aesjhduajk",
    "time": "",
}


def send_msg_group(massege):
    pass


def get_admin_ids(bot, chat_id):
    return [admin.user.id for admin in bot.get_chat_administrators(chat_id)]


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to ProWily DB Bot",
    )
    print(update.effective_chat.id)


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Wait Please")
    # giteing time
    time_now = datetime.now()
    curr_date = time_now.strftime("%d/%m/%Y")
    curr_time = time_now.strftime("%H:%M:%S")

    chat_id = update.effective_chat.id
    create_dir(chat_id)
    print(PATH + f"/groups/{chat_id}/logs/log.json")
    with open(PATH + f"/groups/{chat_id}/logs/log.json", "r") as log_file:
        print(log_file.read())
    new_data = {
        "username": update.message.from_user.username,
        "user_id": update.message.from_user.id,
        "message": update.message.text,
        "time": f"[{curr_date} - {curr_time}]",
    }
    log_data = json.loads(new_data)
    print(log_data)

    log_data.update(new_data)

    print(log_data)
    print(f"here>>{update.message.from_user}")

    command: str = update.message.text.lower()
    if "/$about " in command[:8]:
        try:
            name = data = split_info("/$about ", command)[0]
            file = open(f"data/{update.effective_chat.id}.{name}")
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Info About [{name}]:\n{file.read()}",
            )
        except:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"There is no such file named: **{name}**",
            )
        finally:
            file.close()
            return
    elif update.message.from_user.id in get_admin_ids(BOT, update.message.chat_id):
        if "/$add " in command[:6]:
            print("data")

            data = split_info("/$add ", command)
            print(data)
            file = open(f"data/{update.effective_chat.id}.{data[0]}", "w")
            file.write(
                data[1]
                + f"\n-\n-\n-\n-\n-\nLast Update: \n[{curr_date}]\n[{curr_time}]\nBy: [@{update.message.from_user.username} - {update.message.chat_id}] "
            )
            print(f"admin : {update.message.from_user.id} ")
            return

        if "/$edit" in command:
            print(f"admin : {update.message.from_user.id} ")

        if "/$delete " in command[:9]:
            try:
                name = data = split_info("/$about ", command)[0]
                os.remove(f"data/{update.effective_chat.id}.{name}")
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"{name} Has been deleted!!",
                )
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"There is no such file named: **{name}**",
                )
            finally:
                return

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Unvalid command"
        )

    # os.remove(file)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done")


def split_info(command, message):
    name = ""
    for i in range(len(message)):
        if message[i] == "$" and message[i + 1] == "#":
            index = i + 2
            while True:
                if message[index] == "#" and message[index + 1] == "$":
                    break
                name += message[index]
                index += 1
            break
    info = message.replace(command, "").replace(f"$#{name}#$", "")
    return [name, info]


def main():

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    create_dir()

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    print(BOT.get_me())
    updater.start_polling()


def create_dir(groub_id=None):
    if not os.path.isdir(PATH + "/groups"):
        os.mkdir(PATH + "/groups")
    if groub_id is not None:
        if not os.path.isdir(PATH + f"/groups/{groub_id}"):
            os.mkdir(PATH + f"/groups/{groub_id}")
            os.mkdir(PATH + f"/groups/{groub_id}/logs")
            os.mkdir(PATH + f"/groups/{groub_id}/data")
            open(PATH + f"/groups/{groub_id}/logs/log.json", "w").close()


if __name__ == "__main__":
    main()
