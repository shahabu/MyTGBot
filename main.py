import asyncio

from core.settings import bot, dp
from src.headers.main import main_router
from src.repositories.base_repository import repository


async def application():

    repository.init_db()

    dp.include_router(main_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(application())
