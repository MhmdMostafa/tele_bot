import json, os

PATH: str = os.getcwd()
data = json.loads(
    str(open(f"/home/wily/gitrepo/tele_bot/groups/-693319728/logs/log.json").read())
)
print(data)


new_data = {
    "username": "soe",
    "user_id": "asd1231",
    "message": "awdqwerhlwed",
    "message_type": "command",
    "discription": "aesjhduajk",
    "time": "",
}
data.update(new_data)
print(data)


# message: str = "$add $#Saitama#$ what ever thing you need"
# command = "$add "

# print(message[:5])


# def split_info(command, message):

#     name = ""
#     for i in range(len(message)):
#         if message[i] == "$" and message[i + 1] == "#":
#             index = i + 2
#             while True:
#                 if message[index] == "#" and message[index + 1] == "$":
#                     break
#                 name += message[index]
#                 index += 1
#             break
#     print(name)

#     info = message.replace(command, "").replace(f"$#{name}#$", "")

#     print(info)
