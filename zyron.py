import discord
from discord.ext import commands
from discord import app_commands
import os

TOKEN = os.getenv("TOKEN")

CATEGORIA_TICKET = 1531278993133801614
CARGO_STAFF = 1531274767011811509
CANAL_PAINEL = 1531276511800332329


intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="🎫 Realizar atendimento",
        style=discord.ButtonStyle.green,
        custom_id="abrir_ticket"
    )
    async def abrir(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        categoria = interaction.guild.get_channel(CATEGORIA_TICKET)

        for canal in interaction.guild.text_channels:
            if canal.name == f"ticket-{interaction.user.name.lower()}":
                await interaction.response.send_message(
                    "❌ Você já possui um ticket aberto.",
                    ephemeral=True
                )
                return


        permissoes = {
            interaction.guild.default_role:
            discord.PermissionOverwrite(view_channel=False),

            interaction.user:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            ),

            interaction.guild.get_role(CARGO_STAFF):
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True
            )
        }


        canal = await interaction.guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=categoria,
            overwrites=permissoes
        )


        embed = discord.Embed(
            title="🎫 Ticket aberto",
            description=(
                f"Olá {interaction.user.mention}!\n\n"
                "A equipe já foi notificada.\n"
                "Aguarde um atendimento."
            ),
            color=0x000000
        )


        await canal.send(
            embed=embed,
            view=Fechar()
        )


        await interaction.response.send_message(
            f"✅ Ticket criado: {canal.mention}",
            ephemeral=True
        )



class Fechar(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="🔒 Fechar ticket",
        style=discord.ButtonStyle.red,
        custom_id="fechar_ticket"
    )
    async def fechar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🔒 Fechando ticket...",
            ephemeral=True
        )

        await interaction.channel.delete()



@bot.event
async def on_ready():

    print(f"{bot.user} online!")

    bot.add_view(Ticket())
    bot.add_view(Fechar())

    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} comandos sincronizados")
    except Exception as erro:
        print(erro)



@bot.tree.command(
    name="painel",
    description="Envia o painel de atendimento"
)
async def painel(
    interaction: discord.Interaction
):

    if interaction.channel.id != CANAL_PAINEL:
        await interaction.response.send_message(
            "❌ Use esse comando no canal correto.",
            ephemeral=True
        )
        return


    embed = discord.Embed(
        title="Central de Atendimento | Zyron Store",
        description=(
            "Após solicitar um atendimento, aguarde um integrante da equipe "
            "responde-lo(a). O atendimento é realizado de forma privada, "
            "contudo, somente integrantes da equipe terá acesso ao atendimento.\n\n"
            "Tenha ciência que a nossa equipe não se encontra presente 24 horas "
            "por dia, contudo, dentro dos horários disponíveis nossos, iremos atender conforme."
        ),
        color=0x000000
    )


    await interaction.response.send_message(
        embed=embed,
        view=Ticket()
    )


bot.run(TOKEN)
