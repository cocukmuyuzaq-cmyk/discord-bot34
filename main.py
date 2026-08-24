import os
import sys
import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import aiohttp
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# ============================================================
# TOKEN - RENDER ENVIRONMENT (ENV) DEĞİŞKENİNDEN ALMA
# ============================================================

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("❌ HATA: Token boş veya .env / Render Environment üzerinde tanımlanmamış!")
    sys.exit(1)

print("✅ Token başarıyla alındı!")

VOUCH_CHANNEL_ID = 1541375320853192774

# ============================================================
# ROL ID'LERİ
# ============================================================

ROLE_UNLIMITED = 1539170674986319912
ROLE_1_PER_DAY = 1539170716715585557
ROLE_5_PER_DAY = 1539562464377839656

# ============================================================
# VERİ DOSYASI
# ============================================================

user_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')

# ============================================================
# STEAM HESAPLARI
# ============================================================

steam_accounts = [
    {'user': 'gbjmu99702', 'pass': 'mrt12518', 'game': 'ARK: Survival Ascended'},
    {'user': 'KathleenJools', 'pass': 'Kathleen3527', 'game': "Marvel's Spider-Man Remastered"},
    {'user': 'zfccv56213', 'pass': 'Garethbale11!', 'game': 'Windrose'},
    {'user': 'de_derekch', 'pass': 'OPvj3*all2(4Aqq', 'game': 'BeamNG.drive'},
    {'user': 'ordinaryrhinoceros6358', 'pass': 'a8ef32a3b76effb41!aZ', 'game': 'Stray'},
    {'user': 'ydtdo32097', 'pass': 'PzIf3P1GXw2dEJ', 'game': 'MECCHA CHAMELEON'},
    {'user': 'Cu98721', 'pass': 'Tam0768838298@@', 'game': 'Subnautica 2'},
    {'user': 'flsge218009', 'pass': 'QoYyB497464', 'game': 'Escape from Tarkov'},
]

# ============================================================
# FONKSİYONLAR
# ============================================================

def load_user_data():
    try:
        if os.path.exists(user_data_file):
            with open(user_data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except:
        return {}

def save_user_data(data):
    try:
        os.makedirs(os.path.dirname(user_data_file), exist_ok=True)
        with open(user_data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def get_user_role(interaction):
    user_roles = [str(role.id) for role in interaction.user.roles]
    if str(ROLE_UNLIMITED) in user_roles:
        return 'unlimited'
    elif str(ROLE_5_PER_DAY) in user_roles:
        return '5_per_day'
    elif str(ROLE_1_PER_DAY) in user_roles:
        return '1_per_day'
    return 'no_role'

def get_max_limit(role_type):
    if role_type == 'unlimited':
        return float('inf')
    elif role_type == '5_per_day':
        return 5
    elif role_type == '1_per_day':
        return 1
    return 0

def check_user_limit(interaction):
    user_id = str(interaction.user.id)
    role_type = get_user_role(interaction)
    max_limit = get_max_limit(role_type)
    data = load_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in data:
        data[user_id] = {'date': today, 'count': 0, 'last_use': None, 'role': role_type}
    
    if data[user_id].get('role') != role_type:
        data[user_id]['role'] = role_type
        data[user_id]['count'] = 0
    
    if data[user_id]['date'] != today:
        data[user_id]['date'] = today
        data[user_id]['count'] = 0
    
    save_user_data(data)
    return data[user_id], max_limit

def can_use_now(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    role_type = get_user_role(interaction)
    
    if role_type == 'unlimited':
        return True, None
    
    if role_type == '5_per_day':
        if user_id in data and data[user_id].get('last_use'):
            try:
                last_use = datetime.fromisoformat(data[user_id]['last_use'])
                time_diff = datetime.now() - last_use
                if time_diff < timedelta(hours=2):
                    remaining = timedelta(hours=2) - time_diff
                    return False, remaining
            except:
                pass
        return True, None
    
    return True, None

def update_last_use(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    if user_id not in data:
        data[user_id] = {}
    data[user_id]['last_use'] = datetime.now().isoformat()
    save_user_data(data)

def increment_count(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    if user_id in data:
        data[user_id]['count'] = data[user_id].get('count', 0) + 1
        save_user_data(data)

# ============================================================
# WEB SUNUCUSU (Render için)
# ============================================================

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

    def log_message(self, format, *args):
        pass

def run_webserver():
    try:
        port = int(os.environ.get('PORT', 10000))
        server = HTTPServer(('0.0.0.0', port), Handler)
        print(f'🌐 Web sunucusu {port} portunda çalışıyor')
        server.serve_forever()
    except Exception as e:
        print(f'⚠️ Web sunucusu başlatılamadı: {e}')

# Web sunucusunu ayrı bir thread'de başlat
threading.Thread(target=run_webserver, daemon=True).start()

# ============================================================
# BOT
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

class SteamBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f'✅ {self.user} olarak giriş yapıldı!')
        print(f'📊 Toplam {len(steam_accounts)} hesap yüklendi!')

bot = SteamBot()

SOON_GIF = 'https://media.tenor.com/LqPwUfj3fwMAAAAM/puppet-red.gif'

async def get_steam_game_image(game_name):
    try:
        search_url = f"https://steamcommunity.com/actions/SearchApps/{game_name.replace(' ', '%20')}"
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and len(data) > 0:
                        app_id = data[0].get('appid')
                        if app_id:
                            return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{app_id}/header.jpg"
    except:
        pass
    return 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2048px-Steam_icon_logo.svg.png'

# ============================================================
# KOMUTLAR
# ============================================================

@bot.tree.command(name='steam', description='Rastgele bir Steam hesabı gösterir.')
async def steam(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    role_type = get_user_role(interaction)
    
    if role_type == 'no_role':
        embed = discord.Embed(
            title='❌ Yetkiniz Yok!',
            description='Bu komutu kullanmak için bir role sahip olmalısınız.',
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    user_data, max_limit = check_user_limit(interaction)
    
    if role_type != 'unlimited' and user_data['count'] >= max_limit:
        embed = discord.Embed(
            title='⚠️ Günlük Limit Doldu!',
            description=f'Bugünkü {max_limit} hesap hakkını doldurdun.',
            color=discord.Color.red()
        )
        embed.set_image(url=SOON_GIF)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    if role_type == '5_per_day':
        can_use, remaining = can_use_now(interaction)
        if not can_use:
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            embed = discord.Embed(
                title='⏳ Beklemen Gerekiyor!',
                description=f'2 saat beklemelisin!\n\n**Kalan Süre:** {hours} saat {minutes} dakika',
                color=discord.Color.orange()
            )
            embed.set_image(url=SOON_GIF)
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
    
    account = random.choice(steam_accounts)
    increment_count(interaction)
    if role_type == '5_per_day':
        update_last_use(interaction)
    
    user_data, _ = check_user_limit(interaction)
    game_image = await get_steam_game_image(account['game'])
    
    role_info = {
        'unlimited': {'name': '💎 Sınırsız', 'color': discord.Color.gold()},
        '5_per_day': {'name': f'📊 Günde 5 ({user_data["count"]}/5)', 'color': discord.Color.blue()},
        '1_per_day': {'name': f'📊 Günde 1 ({user_data["count"]}/1)', 'color': discord.Color.green()}
    }
    
    embed = discord.Embed(
        title=f'🎮 {account["game"]}',
        description=f'**Kullanıcı Adı:** {account["user"]}\n**Şifre:** {account["pass"]}',
        color=role_info[role_type]['color']
    )
    embed.set_thumbnail(url=game_image)
    embed.add_field(name='👤 Rolün', value=role_info[role_type]['name'], inline=False)
    
    if role_type == '5_per_day':
        remaining = 5 - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
        embed.add_field(name='⏱️ Bekleme', value='2 saat aralıkla', inline=True)
    elif role_type == '1_per_day':
        remaining = 1 - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
    elif role_type == 'unlimited':
        embed.add_field(name='♾️ Limit', value='Sınırsız!', inline=True)
    
    embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap')
    
    vouch_button = discord.ui.Button(label='✅ Vouch', style=discord.ButtonStyle.success, custom_id='vouch')
    status_button = discord.ui.Button(label='📊 STATUS', style=discord.ButtonStyle.primary, custom_id='status')
    view = discord.ui.View()
    view.add_item(vouch_button)
    view.add_item(status_button)
    
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)

@bot.tree.command(name='premium', description='Premium abonelik bilgilerini gösterir.')
async def premium(interaction: discord.Interaction):
    embed = discord.Embed(
        title='💎 Premium Abonelik',
        description='**🔜 SOON!**\n\nPremium özellikler yakında geliyor!',
        color=discord.Color.gold()
    )
    embed.add_field(name='✅ Sınırsız Hesap', value='Günlük limit olmadan hesap alabilirsin', inline=False)
    embed.add_field(name='🎁 Özel Hesaplar', value='Sadece premium üyelere özel hesaplar', inline=False)
    embed.add_field(name='⚡ Öncelikli Destek', value='7/24 öncelikli destek hizmeti', inline=False)
    embed.set_image(url=SOON_GIF)
    embed.set_footer(text='🔜 Yakında...')
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='myrole', description='Kendi rolünü ve kullanım durumunu gösterir.')
async def myrole(interaction: discord.Interaction):
    role_type = get_user_role(interaction)
    user_data, max_limit = check_user_limit(interaction)
    
    role_names = {
        'unlimited': '💎 Sınırsız (Premium)',
        '5_per_day': f'📊 Günde 5 (Kullanılan: {user_data["count"]}/5)',
        '1_per_day': f'📊 Günde 1 (Kullanılan: {user_data["count"]}/1)',
        'no_role': '❌ Yetkin Yok'
    }
    
    embed = discord.Embed(title='📊 Yetki ve Kullanım Bilgilerin', color=discord.Color.blue())
    embed.add_field(name='👤 Rolün', value=role_names[role_type], inline=False)
    
    if role_type != 'no_role' and role_type != 'unlimited':
        remaining = max_limit - user_data['count']
        embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
    
    if role_type == '5_per_day':
        can_use, remaining = can_use_now(interaction)
        if not can_use:
            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)
            embed.add_field(name='⏳ Bekleme Süresi', value=f'{hours} saat {minutes} dakika', inline=True)
        else:
            embed.add_field(name='✅ Durum', value='Hazır, hesap alabilirsin!', inline=True)
    
    embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap mevcut')
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================================
# BUTON OLAYLARI
# ============================================================

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data.get('custom_id') == 'vouch':
            try:
                channel = bot.get_channel(VOUCH_CHANNEL_ID)
                if channel:
                    await channel.send(f'✅ Vouch verildi: {interaction.user.mention} tarafından!')
                    await interaction.response.send_message('✅ Vouch kanala gönderildi!', ephemeral=True)
                else:
                    await interaction.response.send_message('❌ Kanal bulunamadı!', ephemeral=True)
            except Exception as e:
                print(f'Hata: {e}')
                await interaction.response.send_message('❌ Bir hata oluştu!', ephemeral=True)
        
        elif interaction.data.get('custom_id') == 'status':
            role_type = get_user_role(interaction)
            user_data, max_limit = check_user_limit(interaction)
            
            role_names = {
                'unlimited': '💎 Sınırsız (Premium)',
                '5_per_day': f'📊 Günde 5 (Kullanılan: {user_data["count"]}/5)',
                '1_per_day': f'📊 Günde 1 (Kullanılan: {user_data["count"]}/1)',
                'no_role': '❌ Yetkin Yok'
            }
            
            embed = discord.Embed(title=f'📊 {interaction.user.name} - Durum Bilgileri', color=discord.Color.blue())
            embed.add_field(name='👤 Rolün', value=role_names[role_type], inline=False)
            
            if role_type == 'unlimited':
                embed.add_field(name='♾️ Limit', value='Sınırsız! 🎉', inline=True)
            elif role_type != 'no_role':
                remaining = max_limit - user_data['count']
                embed.add_field(name='⏳ Kalan Hak', value=f'{remaining} hesap', inline=True)
            
            if role_type == '5_per_day':
                can_use, remaining = can_use_now(interaction)
                if not can_use:
                    hours = int(remaining.total_seconds() // 3600)
                    minutes = int((remaining.total_seconds() % 3600) // 60)
                    embed.add_field(name='⏳ Bekleme Süresi', value=f'{hours} saat {minutes} dakika', inline=True)
                    embed.add_field(name='⏱️ Durum', value='❌ Beklemede', inline=True)
                else:
                    embed.add_field(name='✅ Durum', value='Hazır! Hesap alabilirsin.', inline=True)
            elif role_type == '1_per_day':
                if user_data['count'] >= 1:
                    embed.add_field(name='⏱️ Durum', value='❌ Bugünlük bitti. Yarın dene!', inline=True)
                else:
                    embed.add_field(name='⏱️ Durum', value='✅ Hazır! Hesap alabilirsin.', inline=True)
            elif role_type == 'unlimited':
                embed.add_field(name='⏱️ Durum', value='✅ Her zaman hazır!', inline=True)
            
            embed.set_footer(text=f'Toplam {len(steam_accounts)} hesap mevcut')
            await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================================
# ADMIN KOMUTLARI
# ============================================================

@bot.tree.command(name='resetall', description='Tüm kullanıcıların limitini sıfırlar (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def reset_all(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    
    data = load_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    for user_id in data:
        data[user_id]['count'] = 0
        data[user_id]['date'] = today
    save_user_data(data)
    await interaction.response.send_message('✅ Tüm kullanıcıların limitleri sıfırlandı!', ephemeral=True)

@bot.tree.command(name='resetuser', description='Bir kullanıcının limitini sıfırlar (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def reset_user(interaction: discord.Interaction, user: discord.User):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    
    user_id = str(user.id)
    data = load_user_data()
    if user_id in data:
        data[user_id]['count'] = 0
        data[user_id]['date'] = datetime.now().strftime('%Y-%m-%d')
        save_user_data(data)
        await interaction.response.send_message(f'✅ {user.mention} limiti sıfırlandı!', ephemeral=True)
    else:
        await interaction.response.send_message(f'❌ {user.mention} için veri bulunamadı!', ephemeral=True)

@bot.tree.command(name='accountcount', description='Toplam hesap sayısını gösterir (Sadece admin)')
@app_commands.default_permissions(administrator=True)
async def account_count(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message('❌ Bu komutu sadece adminler kullanabilir!', ephemeral=True)
        return
    await interaction.response.send_message(f'📊 Toplam {len(steam_accounts)} Steam hesabı mevcut!', ephemeral=True)

# ============================================================
# BOTU BAŞLAT
# ============================================================

if __name__ == "__main__":
    print("🚀 Bot başlatılıyor...")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Bot başlatılamadı: {e}")
        sys.exit(1)
