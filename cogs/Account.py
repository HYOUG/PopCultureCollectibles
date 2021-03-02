import asyncio
import discord
from discord.ext import commands
from discord.utils import get
from modules.bot_functions import *
from modules.chat_effects import *


class Account(commands.Cog):
    """
    Commands : 
    - start
    - delete_account
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        """Create the author's game account"""
        if not is_registered(ctx.author.id):

            inventories = get_file("inventories")
            cooldowns = get_file("cooldowns")
            cooldowns[str(ctx.author.id)] = {"daily": 0, "spin": 0}
            inventories[str(ctx.author.id)] = {"balance": 0,
                                               "items": [],
                                               "packs": {},
                                               "powers": [],
                                               "shares":{},
                                               "shield_active": False}
            update_file("cooldowns", cooldowns)
            update_file("inventories", inventories)

            embed = discord.Embed(color=default_color)
            embed.set_author(name="🚩 Inscription")
            embed.add_field(name="Start", value=f"{ctx.author.mention}, votre compte a été créer !")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)

        else:
            await gen_error("account_existing", ctx)

    
    @commands.command(aliases=["delete account", "ragequit"])
    async def delete_account(self, ctx):
        """Delete the author's account"""
        confirmation_text = "Vous êtes sur le point de supprimer définitivement votre         \
                            compte de jeu. Vos items, packs, actions et power-ups seront      \
                            également définitivement supprimés. Vous ne serez jamais          \
                            remboursé et vos possessions ne seront pas réstaurées.\n          \
                            Confirmez cette action en ajoutant une réction "


        embed = discord.Embed(color=warning_color)
        embed.set_author(name="🗑️ Suppression de compte")
        embed.add_field(name="Confirmation", value=confirmation_text)
        embed = set_footer(embed, ctx)
        confirmation = await ctx.send(embed=embed)

        await confirmation.add_reaction("✅")
        await confirmation.add_reaction("❌")

        check = lambda reaction, reaction_user: reaction.emoji in ["✅", "❌"] and reaction_user.id == ctx.author.id

        try:
            reaction, reaction_user = await self.bot.wait_for("reaction_add", check=check, timeout=10.0)
            
            if reaction.emoji == "✅":
                cooldowns = get_file("cooldowns")
                inventories = get_file("inventories")
                market = get_file("market")
                
                del cooldowns[str(ctx.author.id)]
                del inventories[str(ctx.author.id)]
                for offer in market["offers"]:
                    if offer["seller"] == ctx.author.id:
                        market["offers"].remove(offer)
                        
                update_file("cooldowns", cooldowns)
                update_file("inventories", inventories)
                update_file("market", market)
                
                embed.clear_fields()
                embed.add_field(name="Conclusion", value=f"{ctx.author.mention} votre compte a été définitivement supprimé")
                embed = set_footer(embed, ctx)
                await confirmation.edit(embed=embed)
                
            elif reaction.emoji == "❌":
                await confirmation.delete()
                await gen_error("canceled", ctx)
            
        except asyncio.TimeoutError:
            await confirmation.delete()
            await gen_error("timeout", ctx)


def setup(client):
    client.add_cog(Account(client))
