import discord
from discord.ext import commands
import os
from yt_dlp import YoutubeDL
import imageio_ffmpeg

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()

# Configuración para yt_dlp
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'extract_flat': 'in_playlist',
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ytdl = YoutubeDL(ytdl_format_options)

@bot.event
async def on_ready():
    print(f"Bot listo como {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

        # Reproducir sonido al unirse
        audio_source = discord.FFmpegPCMAudio('alohalokitas.mp3', executable=FFMPEG_PATH)
        voice_client.play(audio_source)

        await ctx.send(f"🎧 Conectado a {channel}. ¡Sin ritmos caribeños!")
    else:
        await ctx.send("¡Tenés que estar en un canal de voz!")

async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("¡Tenés que estar en un canal de voz!")
            return False
    return True

@bot.command()
async def play(ctx, *, source: str):
    prohibited_keywords = [
        "cumbia", "reggaeton", "daddy yankee", "bad bunny",
        "karol g", "vallenato", "ozuna", "anuel"
    ]

    if any(keyword.lower() in source.lower() for keyword in prohibited_keywords):
        await ctx.send("⛔ Esta COSA está vetada por la ley anti ritmos caribeños y no cumple con el código anti-tropi #2343256. Buscate algo con más guitarra o músicos de verdad al menos, bigote de ornitorrinco 😎")
        return

    connected = await ensure_voice(ctx)
    if not connected:
        return

    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    try:
        info = ytdl.extract_info(source, download=False)
        url_audio = info['url']
        titulo = info.get('title', source)

        if any(keyword.lower() in titulo.lower() for keyword in prohibited_keywords):
            await ctx.send(f"⛔ '{titulo}' Esta COSA está vetada por la ley anti ritmos caribeños y no cumple con el código anti-tropi #2343256. Buscate algo con más guitarra o músicos de verdad al menos, bigote de ornitorrinco 😎")
            return

        audio_source = discord.FFmpegPCMAudio(url_audio, executable=FFMPEG_PATH, options='-vn')
        ctx.voice_client.play(audio_source)
        await ctx.send(f"🎶 Reproduciendo: {titulo}")
    except Exception as e:
        await ctx.send(f"No pude reproducir eso: {e}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        ctx.voice_client.stop()
        await ctx.send("⏹️ Música detenida.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Me fui del canal, chatranes! Aguante la empanada sin papa.")

bot.run(os.getenv("DISCORD_TOKEN"))
