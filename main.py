import telebot
import pickle

bot = telebot.TeleBot("672604929:AAHtcmTYe6gJj6YFhkZJhgtuRwv9qNNTxlE")

queue = []
queue_id = []
queue_size = 0
admin_id = 573464296
moder_id = []
black_list = []


def save_data():
    with open('objs.pkl', 'wb') as f:
        pickle.dump([queue, queue_id, queue_size, black_list, moder_id], f)


def load_data():
    global queue, queue_id, queue_size, black_list, moder_id
    with open('objs.pkl', 'rb') as f:
        queue, queue_id, queue_size, black_list, moder_id = pickle.load(f)


def log(message):
    print("\n ------")
    from datetime import datetime
    print(datetime.now())
    print("Message from {0} {1}. (id = {2}) \nText: {3}".format(message.from_user.first_name,
                                                                message.from_user.last_name,
                                                                str(message.from_user.id), message.text))
    with open('log.txt', 'a') as f:
        f.write(str(datetime.now()) + str("Message from {0} {1}. (id = {2}) "
                                          "\nText: {3}\n".format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id), message.text)))


@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, """ОСНОВНЫЕ КОМАНДЫ: 
очередь - просмотр очереди на стирку
запись - записаться в очередь
пропуск - выйти из очереди
ключи - узнать у кого ключи(закончить стирку)
напомнить - написать первому в очереди чтоб он поторопился""")
    log(message)


@bot.message_handler(commands=['log'])
def handle_text(message):
    bot.send_message(message.chat.id, """ИСТОРИЯ ИЗМЕНЕНИЙ: 
0.8 - Добавлен лог версий, добавлены команды для модераторов, стикеры.
0.7 - Открытый бета тест, добавлена возможность назначать модераторов.
0.1-0.6 - разработка стандартных функций.""")
    log(message)


@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, """Привет! Это бот, который поможет тебе следить за очередью на стирку.
    Чтобы понять как им управлять введи /help\n\nDeveloper: Danil Stepanov @Leronov\nQA: Sergij Lavrenko
    v.0.8""")
    log(message)


@bot.message_handler(commands=['alist'])
def handle_text(message):
    bot.send_message(message.chat.id, """СПИСОК АДМИНИСТРАТОРОВ:
🙈 Creator Данил Степанов @leronov""")
    log(message)


@bot.message_handler(commands=['admin'])
def handle_text(message):
    if message.chat.id == admin_id:
        bot.send_message(message.chat.id, """АДМИН КОМАНДЫ: 
        banID - бан пользователя по ID
        сброс - очистка очереди
        clear - разбан пользователя
        del - удаление из очереди
        send.id.text - отправить сообщение по id
        ans.N.text - отправить текст N-ому человеку в очереди
        moder - добавить модератора
        remod - убрать модератора""")
    else:
        bot.send_sticker(message.chat.id, data="CAADAgADcgADFWxSHvYiqyusxbOoAg")
        bot.send_message(message.chat.id, "Отказано в доступе!")
    log(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    log(message)
    load_data()
    cid = message.chat.id
    global queue_size
    queue_str = str(queue)

    queue_str = queue_str.replace("', '", ")\n")
    queue_str = queue_str.replace(".", "(")
    queue_str = queue_str.replace("']", ")")
    queue_str = queue_str.replace("['", "")
    queue_str = queue_str.title()

    message.text = message.text.lower()
    if str(cid) in black_list and not cid == admin_id:
        bot.send_message(cid, "Вы были заблокированы! Обратитесь к модератору.")
        bot.send_sticker(cid, data="CAADAgADbwADFWxSHoFhXikz_YidAg")
    elif not message.text.find("moder") == -1 and cid == admin_id:
        moder_id.append(message.text[message.text.find("r")+1:len(message.text)])
        save_data()
        bot.send_message(admin_id, "НОВЫЙ МОДЕРАТОР БЫЛ ДОБАВЛЕН")
    elif not message.text.find("remod") == -1 and cid == admin_id:
        moder_id.remove(message.text[message.text.find("d")+1:len(message.text)])
        save_data()
        bot.send_message(admin_id, "МОДЕРАТОР БЫЛ УДАЛЁН")
    elif not message.text.find("send") == -1 and (cid == admin_id or str(cid) in moder_id):
        com, usid, mes = message.text.split(".")
        bot.send_message(usid, mes)
        bot.send_message(cid, "Сообщение было успешно отправлено!")
    elif not message.text.find("ans") == -1 and (cid == admin_id or str(cid) in moder_id):
        com, usid, mes = message.text.split(".")
        bot.send_message(queue_id[int(usid)-1], mes)
        bot.send_message(cid, "Сообщение было успешно отправлено!")
    elif message.text == "сброс" and (cid == admin_id or str(cid) in moder_id):
        queue.clear()
        queue_size = 0
        queue_id.clear()
        save_data()
        bot.send_message(cid, "Ты сбросил очередь!")
        bot.send_message(admin_id, "БЫЛ ВЫПОЛНЕН СБРОС ОЧЕРЕДИ!")
    elif not message.text.find("ban") == -1 and (cid == admin_id or str(cid) in moder_id):
        black_list.append(message.text[message.text.find("n")+1:len(message.text)])
        bot.send_message(cid, "БЫЛ ЗАБЛОКИРОВАН ПОЛЬЗОВАТЕЛЬ " + str(black_list[-1]))
        save_data()
    elif not message.text.find("clear") == -1 and (cid == admin_id or str(cid) in moder_id):
        if message.text[message.text.find("r") + 1:len(message.text)] in black_list:
            black_list.remove(message.text[message.text.find("r") + 1:len(message.text)])
            bot.send_message(cid, "ПОЛЬЗОВАТЕЛЬ РАЗБЛОКИРОВАН!")
        else:
            bot.send_message(cid, "ПОЛЬЗОВАТЕЛЬ НЕ ЗАБЛОКИРОВАН!")
        save_data()
    elif not message.text.find("del") == -1 and (cid == admin_id or str(cid) in moder_id):
        index = message.text[message.text.find("l")+1:len(message.text):1]
        queue.pop(int(index)-1)
        bot.send_message(cid, "ID пользователя: " + str(queue_id.pop(int(index)-1)))
        bot.send_message(cid, "ПОЛЬЗОВАТЕЛЬ УДАЛЁН ИЗ ОЧЕРЕДИ!")
        queue_size -= 1
        save_data()
    elif message.text == "очередь":
        if queue_size == 0:
            bot.send_message(cid, "Очередь пустая! Будь первым - введи \"запись\"")
        elif cid == queue_id[0]:
            bot.send_message(cid, "Ты первый в очереди! Бегом стирать!\n"
                                  "Чтобы выйти из очереди введи - ключи")
        else:
            bot.send_message(cid, "Очередь на стирку:\n"+queue_str)
    elif not message.text.find("запись!") == -1 and not message.text.find(".") == -1:
        if cid in queue_id:
            bot.send_message(cid, "Вы уже добавляли себя в очередь!")
        else:
            queue.append(message.text[message.text.find("!")+1:len(message.text):1])
            queue_id.append(cid)
            queue_size += 1
            save_data()
            bot.send_message(cid, "Вы успешно записаны!")
    elif not message.text.find("запись") == -1:
        bot.send_message(cid, "Чтобы записаться введите \"запись!Фамилия.№комнаты\"\nПРИМЕР: запись!Иванов.22")
    elif message.text == "напомнить":
        if queue_size == 0:
            bot.send_message(cid, "В очереди никого нет!")
        else:
            bot.forward_message(queue_id[0], cid, message.message_id)
            bot.send_message(cid, "Напомнил человеку об очереди!")
            bot.send_message(queue_id[0], "Вам напомнили об очереди! Возьмите/передайте ключ!")
    elif message.text == "ключи":
        if queue_size == 0:
            bot.send_message(cid, "Очередь пустая!")
        elif cid == queue_id[0]:
            bot.send_message(cid, "Вы закончили стирку! Отнесите ключи в следущую комнату.")
            queue.pop(0)
            queue_id.pop(0)
            queue_size -= 1
            save_data()
        else:
            bot.send_message(cid, "Ключи в комнате: " + queue[0])
    elif message.text == "пропуск":
        if cid in queue_id:
            index = queue_id.index(cid)
            queue_id.pop(index)
            queue.pop(index)
            queue_size -= 1
            save_data()
            bot.send_message(cid, "Ты был успешно удалён из очереди.")
        else:
            bot.send_message(cid, "Тебя не было в очереди.")
    else:
        bot.send_sticker(cid, data="CAADAgADfAADFWxSHhxDFfUvGy3vAg")
        bot.send_message(cid, "Я не понимаю что ты от меня хочешь!")


bot.polling(none_stop=True, interval=0)
