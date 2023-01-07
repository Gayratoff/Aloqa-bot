from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, ForceReply

from data.config import ADMINS
from keyboards.inline.menu import kb
from loader import dp, db, bot
from states.state import Add_user, Aloqa


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    tekshirsh =db.count_user_id(user_id=message.from_user.id)
    if tekshirsh[0] >0:
        await message.reply(f"Taklif va mulohazalaringiz bo'lsa yoki savolingiz bo'lsa yozing. Ismingiz va nomeringizni qoldirishni unutmang  👨‍✈️Admin  bilan bog'lanmoqchi bo'lsangiz Ismingiz va raqamingizni yozib qoldiring Admin siz bilan 5 daqiqada bog'lanadi📞", reply_markup=kb.main())
        await state.finish()
    else:
        await message.reply("Botdan to'liq foydalanishingiz uchun avvalo o'zingizni tanishtirish qismidan o'tin.\nIsm familyangizni yozing")
        await Add_user.full_name.set()

@dp.message_handler(state=Add_user.full_name)
async def add_full_name(message :types.Message,state:FSMContext):
    full_name = message.text
    await state.update_data({'full_name':full_name})
    await message.answer("Telefon raqamingiz pastdagi tugmani bosish orqali jo'nating!",reply_markup=kb.contact())
    await Add_user.number.set()

@dp.message_handler(content_types=['contact'], state=Add_user.number)
async def add_number(message: types.Message,state:FSMContext):
    id = message.contact.user_id
    phone_number =message.contact.phone_number
    await state.update_data({"phone_number":phone_number, "id": id})
    message_id = (await message.answer("Saqlanmoqda...",reply_markup=ReplyKeyboardRemove())).message_id
    await bot.delete_message(chat_id=message.from_user.id, message_id=message_id)
    await message.answer("Endi Viloyatingizni Tanlang !",reply_markup=kb.city())
    await Add_user.city.set()

@dp.callback_query_handler(state=Add_user.city)
async def add_city(call: types.CallbackQuery,state: FSMContext):
    data = call.data
    print(data)
    await call.message.delete()
    await state.update_data({"data": data})
    malumot = await state.get_data()
    user_id = malumot.get("id")
    full_name = malumot.get("full_name")
    number = malumot.get("phone_number")
    city = malumot.get("data")
    try:
        db.add_user(user_id=user_id,full_name=full_name,number=number,city=city)
    except Exception as xatolik:
        print(xatolik)

    await call.message.answer("Talif va mulohazalaringiz bo'lsa yoki savolingiz bo'lsa yozing  👨‍✈️Admin  bilan bog'lanmoqchi bo'lsangiz Ismingiz va raqamingizni yozib qoldiring Admin siz bilan 5 daqiqada bog'lanadi📞",reply_markup=ForceReply())
    await state.finish()
    await Aloqa.aloqa.set()

@dp.message_handler(state=Aloqa.aloqa)
async def add_full_name(message :types.Message,state:FSMContext):
    user_id = message.from_user.id
    Aloqa_TXT = message.text
    await state.update_data({'Aloqa_TXT': Aloqa_TXT,"user_id":user_id})
    tg_id = db.select_all_user(user_id=user_id)
    for x in tg_id:
        text = f"{message.from_user.get_mention()} Dan Xabar Keldi\n\n"
        text += f"<i>👤 Ism va familiyasi:</i> <b>{x[2]}\n</b>"
        text += f"<i>📞 Telefon raqami :</i> <b>+{x[3]}</b>\n"
        text += f"<i>🏘 Yashash Joyi :</i> <b>{x[4]}</b>\n\n"
        text += f"<i>📝 Murojati :</i>  <b>{Aloqa_TXT}</b>"
        await bot.send_message(chat_id=ADMINS[0],text=text)
        await message.answer("<b>Yuborildi ...</b>")
        await state.finish()

@dp.callback_query_handler(text="habar")
async def add_full_name(call : types.CallbackQuery):
    await call.message.answer("Xabar yozing ....",reply_markup=ForceReply())
    await Aloqa.aloqa.set()