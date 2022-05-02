import itertools
import os
from discord.ext import commands
from dotenv import load_dotenv; load_dotenv()

def prefixes(prefix):
    l = list(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in prefix))))
    pl = ["…"]
    for i in l:
        if i not in pl:
            pl.append(i)
    return pl

async def get_prefix(client, message):
    return commands.when_mentioned_or(*prefixes(os.getenv('prefix')))(client, message)
