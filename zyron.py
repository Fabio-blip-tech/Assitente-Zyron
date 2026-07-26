import discord
from discord.ext import commands
import os
import requests
from flask import Flask, redirect, request
from threading import Thread

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

GUILD_ID = 1530961753578672313
CARGO_VERIFICADO = 1530986790968627351
CANAL_VERIFICACAO = 1530974499061891294


app = Flask(__name__)

usuarios_pendentes = {}


@app.route("/")
def home():
    return """
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;padding-top:80px">
        <h1>🔐 Zyron Verification</h1>
        <p>Sistema de verificação online.</p>
    </body>
    </html>
    """


@app.route("/verify")
def verify():

    return """
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;padding-top:80px">

        <h1>🔐 Verificação Zyron</h1>

        <p>Clique abaixo para verificar sua conta Discord.</p>

        <a href="/login">
            <button style="padding:15px;font-size:18px">
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
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=identify"
    )

    return redirect(url)


@app.route("/callback")
def callback():

    code = request.args.get("code")

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    resposta = requests.post(
        "https://discord.com/api/oauth2/token",
        data=data,
        headers=headers
    )

    token = resposta.json()["access_token"]

    usuario = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    ).json()

    usuarios_pendentes[usuario["id"]] = int(usuario["id"])


    return """
    <html>
    <body style="background:#111;color:white;text-align:center;font-family:Arial;padding-top:80px">

        <h1>✅ Verificação concluída!</h1>

        <p>Agora volte para o servidor.</p>

        <a href="https://discord.gg/veRMhkpuTg">
            <button style="padding:15px;font-size:18px">
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
intents.members = True
intents.message_content = True


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
    async def verificar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "🔐 Abrindo verificação...",
            ephemeral=True
        )

        await interaction.followup.send(
            "Clique aqui para verificar:",
            view=discord.ui.View().add_item(
                discord.ui.Button(
                    label="🔵 Verificar com Discord",
                    style=discord.ButtonStyle.link,
                    url="https://assitente-zyron.onrender.com/verify"
                )
            ),
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
            "Clique no botão abaixo para se verificar.",
            view=Verificar()
        )



@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Zyron funcionando!")



keep_alive()

bot.run(TOKEN)
