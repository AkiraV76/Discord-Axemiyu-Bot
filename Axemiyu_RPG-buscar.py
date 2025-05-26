import discord
from discord.ext import commands
import random
import json
import aiohttp
import os

# Copyright (c) 2025 Axemiyu
# Licensed under the MIT License

################### IMPORTANTE!!!! ###################

# Para ejecutar el bot TIENE QUE SER desde la MISMA carpeta. En terminar ir con "cd" a la carpeta. Si no, da FALLO pa buscar las imágenes
######################################################

# Configurar bot. Funciona con "!" de prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Imprime esto en el prompt cuando se conecte a Discord
@bot.event
async def on_ready():
    print(f'✅ Bot Axemiyu.{bot.user} ha iniciado sesión.')
    print(f'📁 Ruta de ejecución actual: {os.getcwd()}')

# Obtener un ítem aleatorio desde items.json
def obtener_item_aleatorio(tipo, rareza):
    try:
        # Testear que el archivo exista y que lo comunique si no lo encuentra
        ruta_archivo = os.path.join(os.getcwd(), "items.json")
        if not os.path.exists(ruta_archivo):
            print("❌ Archivo 'items.json' no encontrado.")
            return None

        with open(ruta_archivo, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"🔍 Buscando ítem: tipo='{tipo}', rareza='{rareza}'")

        categoria = data.get(tipo)
        if not categoria:
            print(f"⚠️ Categoría '{tipo}' no encontrada.")
            return None

        items_de_rareza = categoria.get(rareza)
        if not items_de_rareza:
            print(f"⚠️ Rareza '{rareza}' no encontrada en categoría '{tipo}'.")
            return None

        item_elegido = random.choice(items_de_rareza)
        return item_elegido

    except json.JSONDecodeError as e:
        print(f"❌ Error al leer el archivo JSON: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    
    return None

# Comando "!busca" en discord
@bot.command()
async def busca(ctx):
    tipo = random.choice(["Alimento", "Arma", "Mineral"])

    numero = random.randint(1, 100)
    if numero <= 50:
        rareza = "comun"
    elif numero <= 80:
        rareza = "raro"
    elif numero <= 95:
        rareza = "epico"
    else:
        rareza = "legendario"

    item = obtener_item_aleatorio(tipo, rareza)

    if item:
        nombre = item.get("nombre", "Objeto sin nombre")
        imagen_url = item.get("imagen")

        async with aiohttp.ClientSession() as session:
            try:
                async with session.head(imagen_url) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title=f'🎉 ¡{nombre} encontrado!',
                            description=f'Has encontrado un **{tipo}** de rareza **{rareza.upper()}**.'
                        )
                        embed.set_image(url=imagen_url)
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(
                            f'🎁 Has obtenido un **{tipo}** de rareza **{rareza.upper()}**!\n'
                            f'⚠️ Imagen no accesible en la URL: `{imagen_url}`'
                        )
            except Exception as e:
                await ctx.send(
                    f'🎁 Has obtenido un **{tipo}** de rareza **{rareza.upper()}**!\n'
                    f'⚠️ Error al acceder a la imagen: {e}'
                )
    else:
        await ctx.send(
            f'⚠️ No se encontró ningún ítem en la categoría **{tipo}** con rareza **{rareza}**. '
            f'Revisa el archivo `items.json`.'
        )


# Aquí el token del bot. Se obtiene en la página de Desarrollador de Discord, desde el menú para invitarlo a un servidor y darle permisos
bot.run('token')