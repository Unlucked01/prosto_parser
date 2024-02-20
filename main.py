import pandas as pd
from openpyxl import Workbook

from telegram_client import *
from google_connector import *


async def main():
    telegram_client = await create_telegram_client()
    chats = await telegram_client.get_dialogs()
    names = []
    for chat in chats:
        if chat.title == "КРОССОВКИ НА ДОСТАВКУ":
            async for message in telegram_client.iter_messages(chat, limit=5):
                if message.media:
                    response = await telegram_client.download_media(message.media)
                    if message.message == '':
                        names.append(response)
                    else:
                        links = upload_file(names)
                        out = ' | '.join(links)
                        df = pd.DataFrame(
                            {
                                "Text": [message.message],
                                "Links": [out]
                            }
                        )
                        write(df)
                        names = []

                    


if __name__ == '__main__':
    asyncio.run(main())




