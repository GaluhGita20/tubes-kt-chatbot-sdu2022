
import telebot
from telebot import types
import mysql.connector
from nltk.chat.util import Chat, reflections
from database_config import *
mydb = mysql.connector.connect(
  host=hostname,
  user=username,
  passwd=password,
  port=port,
  database=databasename
)
mycursor = mydb.cursor(buffered=True)
API_TOKEN = apitoken
bot = telebot.TeleBot(API_TOKEN)

#start
@bot.message_handler(commands=['start', 'Start', 'START'])
def send_welcome(message):
  markup = types.ReplyKeyboardMarkup(row_width=3)
  itembtn1 = types.KeyboardButton('/START_PESERTA')
  itembtn2 = types.KeyboardButton('/INFO_JADWAL')
  itembtn3 = types.KeyboardButton('/CEK_DATA_PESERTA')
  itembtn4 = types.KeyboardButton('/CEK_GUGUS')
  itembtn5 = types.KeyboardButton('/REMINDER')
  itembtn6 = types.KeyboardButton('/EXIT')
  markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
  # variabel message
  message_awal_nonregis = "Halooo Ksatria Muda Udayana!!!\n\n Selamat datang di akun Telegram Official SDU Udayana 2022." \
                          "Karena ini pertama kalinya Anda memulai chatbot telegram official dari " \
                          "SDU 2022, \nyuk isi nama Anda : "
  message_info = "Berikut merupakan command yang kami gunakan.\n\n" \
                 "/START_PESERTA untuk memulai pendaftaran peserta SDU 2022.\n" \
                 "/INFO_JADWAL untuk menampilkan jadwal SDU 2023.\n" \
                 "/CEK_DATA_PESERTA untuk melakukan pengecekan data peserta user.\n" \
                 "/CEK_GUGUS untuk menampilkan hasil gugus dari user.\n" \
                 "/REMINDER untuk menampilkan susunan kegiatan dalam waktu dekat.\n" \
                 "/EXIT untuk mengakhiri sesi chatbot.\n\n" \
                 "Jangan sampai ketinggalan info ya.\n" \
                 "Jangan semangat dan tetap menyerah:)....."
  cursor = mydb.cursor()
  val = (message.chat.id, )
  query = "SELECT chatId FROM users WHERE chatId= '%s' " % (val)
  cursor.execute(query)
  exist = cursor.fetchone()
  if cursor.rowcount >0:
    query = "SELECT chatId, displayName FROM users WHERE chatId= '%s' " % (val)
    cursor.execute(query)
    resultSet = cursor.fetchone()
    global displayName
    global id_user
    displayName =str(resultSet[1])
    id_user = str(resultSet[0])
    message_awal = "Hi " + displayName + "!!! Selamat datang di akun Telegram Official SDU Udayana 2022. \n\n" \
                                        "Untuk info lebih lanjut tentang SDU 2022, cek sosial media kami!\n" \
                                        "linktr.ee/SocmedJSDU2023."
    bot.reply_to(message, message_awal)
    bot.reply_to(message, message_info, reply_markup=markup)
  else:
    msg = bot.reply_to(message, message_awal_nonregis)
    bot.register_next_step_handler(msg, register_user)
  # set up markup


@bot.message_handler(commands=['INFO_JADWAL'])
def exit_bot(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn = types.KeyboardButton('/START')
    markup.add(itembtn)
    msg = bot.reply_to(message, 'Well then, Good Bye.',reply_markup=markup)
    bot.register_next_step_handler(msg, send_welcome)

@bot.message_handler(commands=['EXIT'])
def exit_bot(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn = types.KeyboardButton('/START')
    markup.add(itembtn)
    msg = bot.reply_to(message, 'Well then, Good Bye.',reply_markup=markup)
    bot.register_next_step_handler(msg, send_welcome)


def register_user(message):
  value = message.text
  if value == '/EXIT':
    markup = types.ReplyKeyboardMarkup()
    itembtn = types.KeyboardButton('/start')
    markup.add(itembtn)
    msg = bot.reply_to(message, 'Terimakasih, sampai ketemu lagi ya.', reply_markup=markup)
    bot.register_next_step_handler(msg, send_welcome)
  else:
    cursor = mydb.cursor()
    query = ("INSERT INTO users(chatId, displayName) VALUES (%s,%s)")
    val = (message.chat.id, message.text)
    cursor.execute(query, val)
    msg = bot.reply_to(message, 'User Registered.\n/START')
    mydb.commit()
    bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
  pairs = [
    # keluhan tidak bisa cek data peserta (saya bingung) (bingung)
    # kenapa tidak  bisa daftar
    # kenapa sih aku tidak bisa daftar
    [r"((.*)|(.?))(mengapa|kenapa|mgp|knp|knapa) ((.*)|(.?))tidak bisa ((.*)|(.?))(mendaftar|daftar|register|registrasi) ((.*)|(.?))data ((.*)|(.?))peserta",
      ["Sebelum itu apakah Anda sudah pernah mendaftarkan menjadi peserta SDU? Silahkan lakukan command /CEK_DATA_PESERTA untuk mengetahuinya."]],

    # mendapatkan info lebih lanjut
    [r"((.*)|(.?))(dimana|bagaiamana|gimana|bgmn|gmn) ((.*)|(.?))info ((.*)|(.?))(lebih lanjut|lengkap|selengkapnya|selanjutnya)",
      ["Untuk mengetahui info lebih lanjut bisa mengecek website studentday.bemudayana.id."]],

    # cek info jadwal
    [r"((.*)|(.?))(dimana|bagaimana|gimana|bgmn|gmn) ((.*)|(.?))(info|info jadwal|jadwal)",
     ["Untuk mengecek data peserta Anda bisa menggunakan command /CEK_DATA_PESERTA."]],

    # cek data peserta
    [r"((.*)|(.?))(dimana|bagaimana|gimana|bgmn|gmn) ((.*)|(.?))(mengecek|cek) ((.*)|(.?))data ((.*)|(.?))peserta",
     ["Untuk mengecek data peserta Anda bisa menggunakan command /CEK_DATA_PESERTA."]],

    # cek gugus
    [r"((.*)|(.?))(mengapa|kenapa|mgp|knp|knapa) ((.*)|(.?))cek ((.*)|(.?))gugus",
     ["Untuk mengecek gugus yang Anda dapatkan, Anda bisa menggunakan command /CEK_GUGUS."]],

    # daftar peserta
    [r"((.*)|(.?))(bagaimana|gimana|gmn|dimana|dmn) ((.*)|(.?))(mendaftar|daftar|registrasi|regis|register) ((.*)|(.?))peserta",
     ["Untuk mendaftar dalam bagian peserta SDU 2023, Anda bisa menggunakan command /START_PESERTA."]],

    # cek gugus
    [r"((.*)|(.?))(bagaimana|gimana|gmn|dimana|dmn) ((.*)|(.?))cek ((.*)|(.?))gugus",
     ["Untuk mengecek gugus yang Anda dapatkan, Anda bisa menggunakan command /CEK_GUGUS."]],

    # apa info terbaru
    [r"((.*)|(.?))(apa|dimana|dmn) ((.*)|(.?))info ((.*)|(.?))terbaru",
     ["Untuk mendapatkan info terbaru, Anda bisa menggunakan command /REMINDER."]],

    # sdu offline atau online
    [r"((.*)|(.?))(apakah) ((.*)|(.?))sdu ((.*)|(.?))(online atau offline|offline atau online|daring atau luring|luring atau daring)",
      ["Untuk tahun ini Student Day 2022 akan dilaksanakan secara hybrid ya dek. Jadi untuk registrasinya akan dilakukan secara offline"
        ", tetapi untuk pelaksanaan 3 hari sdu 2022 akan dilaksanakan secara online. Untuk info yang lebih pasti bisa ditunggu informasinya ya."]],

    # keluhan telat daftar
    [r"((.*)|(.?))(bagaimana) ((.*)|(.?))telah ((.*)|(.?))daftar",
     ["Mohon maaf ya, solusinya satu-satunya jika kalian telat mendaftar menjadi peserta Student Day 2022 adalah dapat mengikuti"
      " Student Day tahun berikutnya. Karena data-data peserta akan diproses untuk pembagian kelompok dan juga gugus. Kami tidak menjamin "
      "bahwa proses tersebut dilakukan dengan waktu cepat."]],

    # kenapa sdu itu penting
    [r"((.*)|(.?))(kenapa|knapa|knp|seberapa) ((.*)|(.?))(sdu penting|penting sdu|student day penting|penting student day)",
      ["Karena Student Day 2022 Universitas Udayana berperan sebagai wadah orientasi mahasiswa baru yang mencakup pemberian nilai,"
        "gagasan, pembentukan karakter, serta pemberian bekal keterampilan softskills serta hardskills yang harapannya dapat menunjang kapabilitas"
        "diri mahasiswa dalam menjalani kehidupan perkuliahan, lebih jauh lagi dalam kehidupan bermasyarakat dan bernegara."]],

    # pengertian sdu
    [r"((.*)|(.?))(apa pengertian|apa itu) ((.*)|(.?))sdu?",
     ["Student Day 2022 Universitas Udayana adalah kegiatan masa orientasi bagi mahasiswa baru Universitas Udayana di tingkat Universitas."
       "Lebih dari itu, Student Day 2022 Universitas Udayana adalah sebuah momentum penanaman nilai-nilai positif serta akselerator"
       "daripada proses perjalanan seseorang dalam menapaki akan memperoleh kehidupan kampus. Karena di saat ini lah, mahasiswa akan memperoleh"
       "sedikit tidaknya proses berpikir, memahami, belajar, dan mengembangkan diri melalui seluruh rangkaian kegiatan yang telah dirancang."]],

    # yang bingung
    [r"((.*)|(.?))bingung", ["Apa yang Anda bingungkan?"]],

    #perkenalan nama
    [r"((.*)|(.?))namaku", ["Hallo ksatria muda udayana. Ada yang bisa kami bantu?"]],
  ]
  try:
    chatbot = Chat(pairs, reflections)
    bot.reply_to(message, chatbot.respond(message.text))
    # bot.reply_to(message, chatbot.respond())
  except:
    bot.reply_to(message, "Maaf, engine tidak mengerti!!!")
  # bot.reply_to(message, chatbot.)


bot.infinity_polling()







