import asyncio

from loguru import logger

from core.settings import config
from src.repositories.base_repository import repository
from src.services.telethon_service import telethon_service


async def check_channels():

    while True:
        channel_links = repository.read_links()

        if not channel_links:
            logger.info("List of channels links is empty")
            await asyncio.sleep(config.DELAY_BETWEEN_CHECK)
            continue

        channels_entities = await telethon_service.get_channels_entities(channel_links)

        for dialog in channels_entities.dialogs:
            unread_count = dialog.unread_count

            if unread_count:
                logger.info(f"Unread count: {unread_count}")
                msgs = await telethon_service.get_messages_ids_for_read(
                    dialog.peer.channel_id, unread_count
                )

                logger.info(msgs)

                await telethon_service.read_messages(dialog, msgs)
                logger.success(
                    f"All accounts success read messages in {dialog.peer.channel_id}"
                )
                continue

            logger.info(f"{dialog.peer.channel_id} doesn't have new posts")

        await asyncio.sleep(config.DELAY_BETWEEN_CHECK)


if __name__ == "__main__":
    asyncio.run(check_channels())
