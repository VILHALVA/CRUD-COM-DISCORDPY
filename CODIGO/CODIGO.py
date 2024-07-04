import discord
from discord.ext import commands
import sqlite3
import os
from TOKEN import TOKEN

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'users.db')

def create_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@bot.command()
async def add(ctx, name: str, age: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, age) VALUES (?, ?)', (name, age))
    conn.commit()
    conn.close()
    await ctx.send(f'Usuário {name} adicionado com sucesso.')

@bot.command()
async def list(ctx):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await ctx.send('Nenhum usuário encontrado.')
    else:
        user_list = '\n'.join([f'{row[0]} - {row[1]} ({row[2]} anos)' for row in rows])
        await ctx.send(f'Lista de Usuários:\n{user_list}')

@bot.command()
async def update(ctx, id: int, name: str, age: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name=?, age=? WHERE id=?', (name, age, id))
    conn.commit()
    conn.close()
    await ctx.send(f'Usuário {id} atualizado com sucesso.')

@bot.command()
async def delete(ctx, id: int):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id=?', (id,))
    conn.commit()
    conn.close()
    await ctx.send(f'Usuário {id} deletado com sucesso.')

@bot.event
async def on_ready():
    create_table()
    print(f'Bot conectado como {bot.user}')

# Executar o bot
bot.run(TOKEN)
