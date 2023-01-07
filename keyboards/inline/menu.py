from aiogram import types


class Keyboards:
    def main(self):
        menu = types.InlineKeyboardMarkup(row_width=2)
        Aloqa = types.InlineKeyboardButton("Adminga Xabar jo'natish",callback_data="habar")
        Channel = types.InlineKeyboardButton("Bizning Kanal",url="https://t.me/+Cp2jQXXJLEM4MTMx")
        return menu.add(Aloqa,Channel)

    def contact(self):
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        contact = types.KeyboardButton("Raqamni yuborish 📞",request_contact=True)
        return menu.add(contact)

    def city(self):
        menu = types.InlineKeyboardMarkup(row_width=2)
        Fargona = types.InlineKeyboardButton("Fargona",callback_data="Fargona")
        Andijon = types.InlineKeyboardButton("Andijon",callback_data="Andijon")
        Namangan = types.InlineKeyboardButton("Namangan",callback_data="Namangan")
        Jizzah = types.InlineKeyboardButton("Jizzah",callback_data="Jizzah")
        return menu.add(Fargona,Andijon,Namangan,Jizzah)

kb = Keyboards()
