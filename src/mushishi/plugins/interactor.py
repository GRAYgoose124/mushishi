import discord
import asyncio

from discord import app_commands
from discord.ext import commands


class Interactor(commands.Cog, discord.ui.Select):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        cm = app_commands.ContextMenu(name='Context Test', callback=self.context_menu_callback)
        print(self.bot.tree.add_command(cm))
        
        super().__init__(
            placeholder="Select something",
            options=[
                discord.SelectOption(label="😆 - Fun", value="1", description="Get all commands according to \"Fun\""),
                discord.SelectOption(label="🪛 - Utility", value="2", description="Get all commands according to \"Utility\""),
                discord.SelectOption(label="❓ - Info", value="3", description="Get all commands according to \"Info\""),
                discord.SelectOption(label="🎭 - Roleplay", value="4", description="Get all commands according to \"Roleplay\""),
                discord.SelectOption(label="🪙 - Economy", value="5", description="Get all commands according to \"Economy\""),
                discord.SelectOption(label="🛑 - Cancel", value="Cancel", description="Cancel this interaction.")
            ]
        )

    async def context_menu_callback(self, interaction: discord.Interaction, message: discord.Message) -> None:        
        embed = discord.Embed(title="Help panel!", description="Your Desc")
        
        async def callback(interaction):
            if self.values[0] == "1":
                await interaction.response.send_message("Test")
        self.callback = callback

        view = discord.ui.View()
        view.add_item(self)
        await interaction.response.send_message('Select the vote type below', view=view, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Interactor(bot))
    await bot.tree.sync()


async def teardown(bot: commands.Bot) -> None:
    await bot.remove_cog('Interactor')
