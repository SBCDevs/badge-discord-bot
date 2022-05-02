from discord.ext import commands

class NoAdmin(commands.CommandError): pass

def checkIfAdmin(ctx: commands.Context):
    if ctx.author.id in [795651331721265153, 339013104564305920, 747490864384704622, 726440141391921284, 811398178229583904]: return True
    raise NoAdmin()

def isAdmin(): return commands.check(checkIfAdmin)
