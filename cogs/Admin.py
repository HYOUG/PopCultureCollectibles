import discord
from discord.ext import commands
from modules.bot_functions import *
from modules.chat_effects import *
from os import system
from json import dumps


class Admin(commands.Cog):
    """
    Commands : 
    - admin_off
    - admin_reboot
    - admin_reload_cog
    - admin_give
    - admin_credit
    - admin_reset
    - admin_add_item
    - admin_skip
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["=off", "=shutdown"])
    @commands.check(is_bot_owner)
    async def admin_off(self, ctx):
        """Shutdown the bot"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔌 Extinction", value=f"{ctx.author.mention}, Pop culture Collectibles va bientôt se déconnecter")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        await self.bot.logout()                                                     # logout the bot

        print("=" * 45)                                                             # log system
        print(red("Pop culture Collectibles se deconnecte..."))                     # //
        print("=" * 45 + "\n")                                                      # //


    @commands.command(aliases = ["=reboot", "=reload"])
    @commands.check(is_bot_owner)
    async def admin_reboot(self, ctx):
        """Reboot the bot"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 Reboot", value=f"{ctx.author.mention}, Pop culture Collectibles va bientôt se reboot")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        
        print("=" * 45 )                                                            # log system
        print(red("Pop culture Collectibles se relance..."))                        # //
        print("=" * 45 + "\n")                                                      # //
        system("python main.py")                                                    # re-launching the main script


    @commands.command(aliases = ["=reloadcog"])
    @commands.check(is_bot_owner)
    async def admin_reload_cog(self, ctx, cog_name: str):
        """Reload the specified cog"""
        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="🔁 Reloading cog", value=f"{ctx.author.mention}, le cog **{cog_name}** va bientôt se redémarrer")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)
        reload_cog(self.bot, cog_name)


    @commands.command(aliases = ["=give"])
    @commands.check(is_bot_owner)
    async def admin_give(self, ctx, target: discord.Member, item_id: str, item_float: float):
        """Generate the specified item (item_id, item_float) to the given member"""
        inventories = get_file("inventories")
        items = get_file("items")
        if item_id in items:
            inventories[str(target.id)]["items"].append({"id": item_id, "float": item_float})
            update_file("inventories", inventories)
            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="➕ Give", value=f"{ctx.author.mention}, `{item_id}:{item_float}` a été procuré avec succès à : {target.mention}")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await gen_error("missing_item", ctx)

    
    @commands.command(aliases=["=credit"])
    @commands.check(is_bot_owner)
    async def admin_credit(self, ctx, target: discord.Member, sum: int = 100):
        """Credit the specified sum of the specified sum"""
        if is_registered(target.id):
            
            inventories = get_file("inventories")
            inventories[str(target.id)]["balance"] += sum
            update_file("inventories", inventories)

            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="💰 Credit",
                            value=f"{ctx.author.mention}, {target.mention} a été crédité de `{sum}` PO (pièces d'or)")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)


    @commands.command(aliases=["=reset"])
    @commands.check(is_bot_owner)
    async def admin_reset(self, ctx, target: discord.Member):
        """Reset the account of the given user"""
        inventories = get_file("inventories")
        cooldowns = get_file("cooldowns")
        del inventories[str(target.id)]
        del cooldowns[str(target.id)]
        update_file("inventories", inventories)
        update_file("cooldowns", cooldowns)

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="♻️ Reset", value=f"{ctx.author.mention}, le compte de {target.mention} a été supprimé")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=additem"])
    @commands.check(is_bot_owner)
    async def admin_add_item(self, ctx, *item_infos: tuple):
        """Add a new item from the given item_infos"""
        items = get_file("items")
        item_infos = "".join(item_infos)
        item_id, item_name, item_from, item_desc, item_tier = item_infos.split(",")
        items[item_id] = {"name": item_name, "from": item_from, "description": item_desc, "tier": item_tier}
        update_file("items", items)

        embed = discord.Embed(color=admin_color)
        embed.set_author(name="🛠️ Admin")
        embed.add_field(name="➕ Add item", value=f"{ctx.author.mention}, l'item : **{item_name}** ({item_id}) a été ajouté")
        embed = set_footer(embed, ctx)
        await ctx.send(embed=embed)


    @commands.command(aliases=["=skip"])
    @commands.check(is_bot_owner)
    async def admin_skip(self, ctx, target: discord.Member, category: str = "spin"):
        """Skip the target's category cooldown"""
        cooldowns = get_file("cooldowns")
        if category in cooldowns[str(target.id)]:
            cooldowns[str(target.id)][category] = 0
            update_file("cooldowns", cooldowns)
            embed = discord.Embed(color=admin_color)
            embed.set_author(name="🛠️ Admin")
            embed.add_field(name="⏩ Cooldown skip", value=f"{ctx.author.mention}, le cooldown `{category}` de {target.mention} a été réinitialisé")
            embed = set_footer(embed, ctx)
            await ctx.send(embed=embed)
        else:
            await gen_error("invalid_synthax", ctx)


def setup(client):
    client.add_cog(Admin(client))
