import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GUILD_ID = 1530961753578672313
CARGO_VERIFICADO = 1530986790968627351
CANAL_VERIFICACAO = 1530974499061891294

app = Flask(__name__)

@app.route("/")
def home():
    return "Zyron Online!"
@app.route("/verify")
def verify():
    return """
    @app.route("/login")
def login():
    return """
    <h1>🔐 Login Zyron</h1>
    <p>Login com Discord em breve...</p>
    """
    <h1>🔐 Verificação Zyron</h1>
    <p>Clique abaixo para verificar sua conta do Discord.</p>
    <a href="/login">✅ Verifique-se</a>
    """

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    Thread(target=run).start()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


class Verificar(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
    label="✅ Verifique-se",
    style=discord.ButtonStyle.green,
    custom_id="botao_verificar"
    )
    
    async def verificar(self, interaction: discord.Interaction, button: discord.ui.Button):

        cargo = interaction.guild.get_role(CARGO_VERIFICADO)

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


@bot.event
async def on_ready():
    print(f"{bot.user} está online!")

    bot.add_view(Verificar())

    canal = bot.get_channel(CANAL_VERIFICACAO)

    if canal:
        await canal.send(
            "🔐 **Verificação Zyron**\n\n"
            "Clique no botão abaixo para confirmar sua entrada no servidor.",
            view=Verificar()
        )


@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Zyron funcionando!")


keep_alive()
bot.run(TOKEN)
