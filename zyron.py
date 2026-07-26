class Verificar(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verifique-se",
        style=discord.ButtonStyle.green,
        custom_id="verificar"
    )
    async def verificar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        cargo = interaction.guild.get_role(CARGO_VERIFICADO)

        if cargo is None:
            await interaction.response.send_message(
                "❌ Cargo não encontrado.",
                ephemeral=True
            )
            return

        if cargo in interaction.user.roles:
            await interaction.response.send_message(
                "✅ Você já está verificado!",
                ephemeral=True
            )
            return

        await interaction.user.add_roles(cargo)

        await interaction.response.send_message(
            "✅ Verificação concluída! Você recebeu o cargo.",
            ephemeral=True
        )
