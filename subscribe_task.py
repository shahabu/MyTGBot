import asyncio
import os
import shutil
import sys

from loguru import logger
from telethon.errors import (ChannelPrivateError, InviteRequestSentError,
                             UserAlreadyParticipantError)
from tqdm import tqdm

from src.common.enums import ChannelType
from src.common.exc import InvalidChannelType
from src.services.telethon_service import telethon_service


async def main():

    sessions = [
        file
        for file in os.listdir("./sessions")
        if file.endswith(".session") and os.path.isfile(f"./sessions/{file}")
    ]

    if not sessions:
        logger.warning("No session files in this folder")
        exit()

    if len(sys.argv) < 2:
        logger.warning(
            "You must enter the username or invite link for private channels in the start command line."
        )
        exit()

    channel_entity = sys.argv[1]

    while True:
        print("Select the type of channel:")
        print("1 - Public")
        print("2 - Private")
        channel_type = input("Enter your choice (1 or 2): ")

        if channel_type in ["1", "2"]:
            break

        print("Answer must be 1 or 2")

    channel_type = ChannelType.PUBLIC if channel_type == "1" else ChannelType.PRIVATE

    for session_file in tqdm(sessions, colour="green", desc="joined"):

        try:
            await telethon_service.subscribe_channel(
                session_file, channel_entity, channel_type
            )
        except (ChannelPrivateError, InvalidChannelType) as _:
            logger.error("Invalid type of channel")
            break
        except (InviteRequestSentError, UserAlreadyParticipantError) as _:
            logger.info("User already subcribe channel or request already sent")
        except KeyboardInterrupt as _:
            print("Script stopeed...")
            break
        except (Exception, shutil.Error) as e:
            logger.error(f"Fetch error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
