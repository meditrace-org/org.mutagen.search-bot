from aiogram import Router, F
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message
from .keyboards import score_kb
from .get_response import top10
from .database import insert_result, count_storage
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging
import uuid
from datetime import datetime

router = Router()


last_message = []


class QueryCache(StatesGroup):
    queried = State()
    scored = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Бот для теста и разметки нашего поиска. "
        "Для написания запроса пиши /search."
        "Для загрузки нового видео пиши /upload"
    )


@router.message(Command("search"))
async def cmd_search(message: Message, state: FSMContext):
    await message.answer(
        "Напиши свой запрос:"
    )


@router.message(Command("rows"))
async def cmd_search(message: Message):
    await message.answer(
        f"rows in db: {count_storage()}"
    )


@router.message(Command("upload"))
async def cmd_upload(message: Message):
    await message.answer(
        "Пока не умею так"
    )


@router.message(F.text.regexp(r'\d+'), QueryCache.queried)
async def collect_score(message: Message, state: FSMContext):

    try:
        data = await state.get_data()
        if data:
            rows = []
            query = data["query"]
            etime = data["execution_time"]
            num = 0
            for i in data["result"]:
                rows.append((
                    int(message.text),
                    query,
                    uuid.UUID(i["uuid"]),
                    i["video_url"],
                    num,
                    etime,
                    datetime.now(),
                    message.from_user.id
                ))
                num += 1
            insert_result(rows)

            for m in last_message:
                m.delete()
            await message.delete()
            await state.clear()
            logging.info(f"ROWS IN DB: {count_storage()}")
        else:
            await message.answer("Нет данных от сервера")

    except Exception as e:
        await message.answer(f"Возникла ошибка: {e}")


@router.message(F.text)
async def make_request(message: Message,  state: FSMContext):
    await state.set_state(QueryCache.queried)
    logging.info(f"Sendind query with promt `{message.text.lower()}`")
    data = top10(message.text.lower())
    await state.update_data(query=message.text.lower(),
                            execution_time=data["execution_time"],
                            result=data["result"])

    media_group = MediaGroupBuilder(caption=f"Время: {float(data['execution_time'])} ms")

    for v in data["result"]:
        media_group.add_video(media=v["video_url"])

    await message.answer_media_group(media_group.build())
    m = await message.answer(text="Оцени релевантность от 1 до 10", reply_markup=score_kb())
    last_message.append(m)

