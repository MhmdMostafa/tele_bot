import telegram, logging, requests
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# https://api.telegram.org/bot/getupdates
# context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
TOKEN: str = ""
bot = telegram.Bot(token=TOKEN)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

PATH: str = os.getcwd()


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
    time_now = datetime.now()
    curr_data = time_now.strftime("%d/%m/%Y")
    curr_time = time_now.strftime("%H:%M:%S")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Wait Please")
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
    elif update.message.from_user.id in get_admin_ids(bot, update.message.chat_id):
        if "/$add " in command[:6]:
            print("data")

            data = split_info("/$add ", command)
            print(data)
            file = open(f"data/{update.effective_chat.id}.{data[0]}", "w")
            file.write(
                data[1]
                + f"\n-\n-\n-\n-\n-\nLast Update: \n[{curr_data}]\n[{curr_time}]\nBy: [@{update.message.from_user.username} - {update.message.chat_id}] "
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
    print(name)

    info = message.replace(command, "").replace(f"$#{name}#$", "")
    return [name, info]


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


print(bot.get_me())
updater.start_polling()
