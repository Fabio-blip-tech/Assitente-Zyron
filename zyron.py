import discord
from discord.ext import commands
import os
from flask import Flask, redirect
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
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;">

        <h1>🔐 Zyron Verification</h1>
        <p>Confirme sua conta do Discord para continuar.</p>

        <a href="/login">
            <button style="
            padding:15px;
            font-size:18px;
            border-radius:10px;">
            🔵 Verificar com Discord
            </button>
        </a>

    </body>
    </html>
    """


@app.route("/login")
def login():
    url = (
        "https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        "&redirect_uri=https://assitente-zyron.onrender.com/callback"
        "&scope=identify"
    )

    return redirect(url)


@app.route("/callback")
def callback():
    return """
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;">

        <h1>✅ Verificação concluída!</h1>
        <p>Sua conta foi verificada com sucesso.</p>

        <a href="https://discord.gg/veRMhkpuTg">
            <button style="
            padding:15px;
            font-size:18px;
            border-radius:10px;">
            🔙 Voltar para o servidor
            </button>
        </a>

    </body>
    </html>
    """


def run():
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )


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

        view = discord.ui.View()

        view.add_item(
            discord.ui.Button(
                label="🔐 Ir para verificação",
                style=discord.ButtonStyle.link,
                url="https://assitente-zyron.onrender.com/verify"
            )
        )

        await interaction.response.send_message(
            "Clique abaixo para verificar sua conta:",
            view=view,
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
            "Clique no botão abaixo para verificar sua conta.",
            view=Verificar()
        )


@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Zyron funcionando!")


keep_alive()
bot.run(TOKEN)
