import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")

app = Flask(__name__)

@app.route("/")
def home():
    return "Zyron Online!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} está online!")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Zyron funcionando!")

keep_alive()
bot.run(TOKEN)
