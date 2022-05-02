import os
import discord
import aiohttp
import traceback
from discord import Webhook
from datetime import datetime

async def log_error(error):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(os.getenv('webhook'), session=session)
        try: raise error
        except Exception:
            await webhook.send(embed=discord.Embed(title="Error Report", description=f"""Time: {datetime.now().strftime("%H:%M:%S")}\nDay: {datetime.now().strftime("%B %d, %Y ")}\nError: {error}\nTraceback:\n\n```py\n{traceback.format_exc()}\n```""", color=0xff0000), username='Error Log')
