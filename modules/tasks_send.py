from modules.keyboards import main_keyboard, task_inline_keyboard
import constants

class TasksSend:
    def __init__(self, tasks):
        self.tasks = tasks

    async def send(self, message, date):
        tasks = list(self.tasks.find({'user': message.from_user.id, 'date': date}))

        markup = main_keyboard()

        if tasks:
            text = constants.ALL_NOTES_TEXT_DATE + ' ' + date

            await message.answer(text, reply_markup=markup)

            for i, el in enumerate(tasks):
                task_text = f'{"✅"*14 if el["done"] else "❌"*14}\n\n{el["text"]}'

                if date == str(message.date.date()):
                    markup = task_inline_keyboard()

                    await message.answer(task_text, reply_markup=markup)
                else:
                    await message.answer(task_text)

        else:
            await message.answer(constants.NO_NOTES, reply_markup=markup)
