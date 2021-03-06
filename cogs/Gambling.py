import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from random import choice, randint


class Gambling(commands.Cog):
    """
    Commands : 
    - flip
    - bet
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx, bet: int = 10):
        """Bet on the result of a coin fliped"""
        if bet % 1 == 0 and bet > 0:
            inventories = get_file("inventories")
            if bet <= inventories[str(ctx.author.id)]["balance"]:

                inventories[str(ctx.author.id)]["balance"] -= bet
                win = choice([True, False])

                embed = discord.Embed(color=default_color)
                embed.set_author(name="🎲 Pile ou face")
                embed = set_footer(embed, ctx)

                if win:
                    inventories[str(ctx.author.id)]["balance"] += bet * 2
                    update_file("inventories", inventories)
                    embed.add_field(name="Resultats",
                                    value=f":trophy: Vous avez gagné : **+**`{bet * 2}` "
                                          f"Votre bourse : `{inventories[str(ctx.author.id)]['balance']}` PO (pièces d'or)")
                else:
                    update_file("inventories", inventories)
                    embed.add_field(name="Results",
                                    value=f":x: Vous avez perdu votre mise : **-**`{bet}` "
                                          f"Votre bourse : `{inventories[str(ctx.author.id)]['balance']}` PO (pièces d'or)")
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_money", ctx)
        else:
            await gen_error("incorrect_value", ctx)


    @commands.command()
    async def bet(self, ctx, bet: int = 10, odd: int = 2):
        """Bet a specified sum with specified odds"""
        if bet >= 1:
            inventories = get_file("inventories")
            if bet <= inventories[str(ctx.author.id)]["balance"]:
                if randint(1, odd) == 1:
                    result_field = f"{ctx.author.mention}, vous avez gagné **{odd}**x votre mise : **+**`{(bet * odd) - bet}`"
                    inventories[str(ctx.author.id)]["balance"] += bet * (odd - 1)
                else:
                    result_field = f"{ctx.author.mention}, vous avez perdu votre mise : **-**`{bet}`"
                    inventories[str(ctx.author.id)]["balance"] -= bet
                update_file("inventories", inventories)
                embed = discord.Embed(color=default_color)
                embed.set_author(name="🎰 Pari")
                embed.add_field(name="Résultats", value=result_field)
                embed = set_footer(embed, ctx)
                await ctx.send(embed=embed)
            else:
                await gen_error("missing_money", ctx)
        else:
            await gen_error("incorrect_value", ctx)
            

def setup(client):
    client.add_cog(Gambling(client))