import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

# Token va API kalitlar to'g'ridan-to'g'ri yozildi
TELEGRAM_TOKEN = "9098530159:AAE1_GTG78mSGg-C5uvn3XmoSWdWd208PVw"
GEMINI_API_KEY = "AQ.Ab8RN6I1sDtKCrIJCfa9T1Ynpu01D-D8dSDLJDNbJtUFG8GcWA"

# Gemini'ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
  await message.answer(
      "Salom! Men sun'iy intellekt (Gemini) asosida ishlaydigan yordamchi"
      " botman. 🤖\n\nMenga istalgan savolingizni yuborishingiz mumkin!",
      reply_markup=ReplyKeyboardRemove(),
  )


@router.message()
async def ai_chat_handler(message: Message):
  user_text = message.text
  if not user_text:
    return

  waiting_msg = await message.answer("O'ylayapman... 🧠")

  try:
    response = model.generate_content(user_text)
    answer_text = response.text

    await waiting_msg.delete()
    await message.answer(answer_text)
  except Exception as e:
    await waiting_msg.edit_text(
        "Xatolik yuz berdi. Iltimos, birozdan keyin qayta urinib ko'ring. ❌"
    )


async def main():
  dp.include_router(router)
  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)


if __name__ == "__main__":
  asyncio.run(main())
    
