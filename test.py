message: str = "$add $#Saitama#$ what ever thing you need"
command = "$add "

print(message[:5])


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

    print(info)
