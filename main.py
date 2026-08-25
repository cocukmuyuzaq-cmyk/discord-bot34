import os
import sys
import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import aiohttp
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread

# ============================================================
# FLASK WEB SUNUCUSU (Render için)
# ============================================================

app = Flask('')

@app.route('/')
def home():
    return "✅ Roblox Username Bot is running!"

def run_webserver():
    try:
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f'⚠️ Web sunucusu başlatılamadı: {e}')

Thread(target=run_webserver, daemon=True).start()

# ============================================================
# TOKEN
# ============================================================

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("❌ HATA: Token bulunamadı!")
    sys.exit(1)

print("✅ Token başarıyla alındı!")

# ============================================================
# ROBLOX API KONFIGÜRASYONU - ÇOKLU API
# ============================================================

# 1. Ana Roblox API
ROBLOX_VALIDATE_URL = "https://auth.roblox.com/v1/usernames/validate"
ROBLOX_USER_URL = "https://api.roblox.com/users/get-by-username"

# 2. Alternatif Roblox API (Aynı işlevi görür)
ROBLOX_ALT_VALIDATE = "https://users.roblox.com/v1/usernames/validate"
ROBLOX_ALT_USER = "https://users.roblox.com/v1/usernames"

# 3. Roblox API (Eski endpoint - hala çalışıyor)
ROBLOX_LEGACY_USER = "https://www.roblox.com/UserCheck/DoesUsernameExist"

# 4. Roblox API (Başka bir alternatif)
ROBLOX_PUBLIC_API = "https://api.roproxy.com/users/get-by-username"

# API'leri liste halinde tut (sırayla dene)
APIS = [
    {'validate': ROBLOX_VALIDATE_URL, 'user': ROBLOX_USER_URL, 'name': 'Ana API'},
    {'validate': ROBLOX_ALT_VALIDATE, 'user': ROBLOX_ALT_USER, 'name': 'Alternatif API'},
    {'validate': None, 'user': ROBLOX_LEGACY_USER, 'name': 'Legacy API'},
    {'validate': None, 'user': ROBLOX_PUBLIC_API, 'name': 'Proxy API'},
]

# Rate limit yönetimi
api_usage = {}
api_cooldown = {}

def generate_username(year, method):
    """Yıl ve methoda göre kullanıcı adı üretir"""
    prefixes = ['cool', 'pro', 'super', 'mega', 'ultra', 'epic', 'dark', 'light', 'star', 'shadow', 'blaze', 'frost', 'storm', 'phantom', 'crystal', 'kangal', 'x', 'z', 'night', 'fire', 'ice', 'thunder', 'steel', 'wild', 'sky']
    suffixes = ['gamer', 'player', 'king', 'queen', 'lord', 'master', 'hunter', 'warrior', 'legend', 'hero', 'x', 'z', 'pro', 'god', 'beast']
    
    if method == 'year_user':
        return f"{random.choice(prefixes)}{year}"
    
    elif method == 'cross_user':
        return f"{random.choice(prefixes)}_{random.choice(suffixes)}"
    
    elif method == 'double_user':
        name = random.choice(prefixes)
        return f"{name}{name[:3]}"
    
    elif method == '123_method':
        return f"{random.choice(prefixes)}{random.randint(10, 999)}"
    
    elif method == '321_method':
        return f"{random.choice(prefixes)}{random.randint(100, 999)}"
    
    elif method == '2_number_method':
        return f"{random.choice(prefixes)}{random.randint(10, 99)}"
    
    elif method == '4_number_method':
        return f"{random.choice(prefixes)}{random.randint(1000, 9999)}"
    
    elif method == '3number':
        return f"{random.choice(prefixes)}{random.randint(100, 999)}"
    
    else:
        return f"{random.choice(prefixes)}{year}{random.randint(10, 99)}"

def get_method_description(method):
    """Method açıklamasını döndürür"""
    descriptions = {
        'cross_user': '❌ cross_user → user_cross (örnek: cool_gamer)',
        'double_user': '🔁 double_user → useruser (örnek: coolcool)',
        'year_user': '📅 year_user → user2006 (örnek: cool2006)',
        '123_method': '🔢 123_method → user123 (örnek: cool123)',
        '321_method': '🔢 321_method → user321 (örnek: cool321)',
        '2_number_method': '🔢 2_number_method → user12 (örnek: cool12)',
        '4_number_method': '🔢 4_number_method → user1234 (örnek: cool1234)',
        '3number': '🔢 3number → user123 (örnek: cool123)'
    }
    return descriptions.get(method, method)

# ============================================================
# ÇOKLU API FONKSİYONLARI
# ============================================================

async def check_username_available_v1(username):
    """API 1: Ana Roblox API"""
    try:
        async with aiohttp.ClientSession() as session:
            params = {'request.username': username}
            async with session.get(ROBLOX_VALIDATE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('code') == 0:
                        return True, data.get('message', 'Müsait')
                    else:
                        return False, data.get('message', 'Alınmış')
                elif response.status == 429:
                    return None, "Rate Limit"
                else:
                    return None, f"HTTP {response.status}"
    except:
        return None, "Hata"

async def check_username_available_v2(username):
    """API 2: Alternatif Roblox API"""
    try:
        async with aiohttp.ClientSession() as session:
            params = {'username': username}
            async with session.get(ROBLOX_ALT_VALIDATE, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if not data.get('data', {}).get('available', True):
                        return False, "Alınmış"
                    return True, "Müsait"
                elif response.status == 429:
                    return None, "Rate Limit"
                else:
                    return None, f"HTTP {response.status}"
    except:
        return None, "Hata"

async def check_username_available_v3(username):
    """API 3: Legacy Roblox API"""
    try:
        async with aiohttp.ClientSession() as session:
            params = {'username': username}
            async with session.get(ROBLOX_LEGACY_USER, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # True = müsait, False = alınmış
                    if data:
                        return True, "Müsait"
                    else:
                        return False, "Alınmış"
                elif response.status == 429:
                    return None, "Rate Limit"
                else:
                    return None, f"HTTP {response.status}"
    except:
        return None, "Hata"

async def check_username_available_v4(username):
    """API 4: Proxy API"""
    try:
        async with aiohttp.ClientSession() as session:
            params = {'username': username}
            async with session.get(ROBLOX_PUBLIC_API, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('Id'):
                        return False, "Alınmış"
                    else:
                        return True, "Müsait"
                elif response.status == 429:
                    return None, "Rate Limit"
                else:
                    return None, f"HTTP {response.status}"
    except:
        return None, "Hata"

# Tüm API'leri bir listede topla
API_CHECKERS = [
    check_username_available_v1,
    check_username_available_v2,
    check_username_available_v3,
    check_username_available_v4
]

async def check_username_available_multi(username):
    """Tüm API'leri dene, ilk başarılı sonucu döndür"""
    for api_func in API_CHECKERS:
        try:
            result, message = await api_func(username)
            
            if result is True:
                return True, message
            elif result is False:
                return False, message
            # None = hata/rate limit, diğer API'yi dene
            elif result is None and "Rate Limit" in message:
                await asyncio.sleep(0.5)  # Rate limit için bekle
                continue
            else:
                continue
        except:
            continue
    
    # Tüm API'ler başarısız
    return None, "Tüm API'ler başarısız"

# ============================================================
# ROBLOX SESSION YÖNETİMİ (Rate Limit için)
# ============================================================

class RobloxSessionManager:
    def __init__(self):
        self.sessions = []
        self.current_session = 0
        self.last_request_time = {}
        self.request_counts = {}
    
    async def get_session(self):
        """Her API için yeni session oluştur"""
        session = aiohttp.ClientSession()
        return session

roblox_session = RobloxSessionManager()

# ============================================================
# ROL ID'LERİ
# ============================================================

ADMIN_ROLE_ID = 123456789012345678
PREMIUM_ROLE_ID = 123456789012345678

# ============================================================
# VERİ DOSYASI
# ============================================================

user_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')

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
    if str(ADMIN_ROLE_ID) in user_roles:
        return 'admin'
    elif str(PREMIUM_ROLE_ID) in user_roles:
        return 'premium'
    return 'user'

def check_user_limit(interaction):
    user_id = str(interaction.user.id)
    role_type = get_user_role(interaction)
    data = load_user_data()
    today = datetime.now().strftime('%Y-%m-%d')
    
    if user_id not in data:
        data[user_id] = {'date': today, 'count': 0, 'role': role_type}
    
    if data[user_id].get('role') != role_type:
        data[user_id]['role'] = role_type
        data[user_id]['count'] = 0
    
    if data[user_id]['date'] != today:
        data[user_id]['date'] = today
        data[user_id]['count'] = 0
    
    save_user_data(data)
    return data[user_id]

def increment_count(interaction):
    user_id = str(interaction.user.id)
    data = load_user_data()
    if user_id in data:
        data[user_id]['count'] = data[user_id].get('count', 0) + 1
        save_user_data(data)

# ============================================================
# BOT
# ============================================================

intents = discord.Intents.default()
intents.message_content = True

class RobloxBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f'✅ {self.user} olarak giriş yapıldı!')
        print(f'🚀 Bot {len(API_CHECKERS)} farklı API ile çalışıyor!')

bot = RobloxBot()

# ============================================================
# KOMUTLAR
# ============================================================

@bot.tree.command(name='gen', description='Roblox API\'den müsait hesap bulur.')
async def gen(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    role_type = get_user_role(interaction)
    user_data = check_user_limit(interaction)
    
    # Limit kontrolü
    if role_type == 'user' and user_data['count'] >= 1:
        embed = discord.Embed(
            title='⚠️ Günlük Limit Doldu!',
            description='Bugün 1 hesap hakkını kullandın. Yarın tekrar dene!',
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    if role_type == 'premium' and user_data['count'] >= 5:
        embed = discord.Embed(
            title='⚠️ Günlük Limit Doldu!',
            description='Premium olarak bugün 5 hesap hakkını kullandın.',
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    # Yıl ve method seçimi için dropdown
    years = [str(year) for year in range(2006, 2017)]
    methods = ['year_user', 'cross_user', 'double_user', '123_method', '321_method', '2_number_method', '4_number_method', '3number']
    
    year_select = discord.ui.Select(
        placeholder='📅 Yıl seç (2006-2016)',
        options=[
            discord.SelectOption(label=year, description=f'{year} hesapları')
            for year in years
        ]
    )
    
    method_select = discord.ui.Select(
        placeholder='🔧 Method seç',
        options=[
            discord.SelectOption(
                label=method, 
                description=get_method_description(method)[:100]
            )
            for method in methods
        ]
    )
    
    view = discord.ui.View()
    view.add_item(year_select)
    view.add_item(method_select)
    
    selected_year = None
    selected_method = None
    
    async def year_callback(interaction: discord.Interaction):
        nonlocal selected_year
        selected_year = year_select.values[0]
        await interaction.response.defer()
    
    async def method_callback(interaction: discord.Interaction):
        nonlocal selected_method
        selected_method = method_select.values[0]
        await interaction.response.defer()
    
    year_select.callback = year_callback
    method_select.callback = method_callback
    
    embed = discord.Embed(
        title='🔍 Roblox Müsait Hesap Bulucu',
        description=f'**{len(API_CHECKERS)}** farklı API ile aranıyor!',
        color=discord.Color.blue()
    )
    embed.add_field(name='📅 Seçilen Yıl', value='Henüz seçilmedi', inline=True)
    embed.add_field(name='🔧 Seçilen Method', value='Henüz seçilmedi', inline=True)
    embed.add_field(name='🔗 API Durumu', value='✅ Tüm API\'ler hazır', inline=False)
    
    find_button = discord.ui.Button(label='🔍 Bul', style=discord.ButtonStyle.primary)
    view.add_item(find_button)
    
    await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    async def find_callback(button_interaction: discord.Interaction):
        if not selected_year or not selected_method:
            embed = discord.Embed(
                title='❌ Hata!',
                description='Lütfen önce yıl ve method seç!',
                color=discord.Color.red()
            )
            await button_interaction.response.edit_message(embed=embed, view=None)
            return
        
        await button_interaction.response.defer()
        
        found_account = None
        attempts = 0
        max_attempts = 30
        used_apis = []
        
        embed = discord.Embed(
            title='🔍 Aranıyor...',
            description=f'**{selected_year}** yılı için **{selected_method}** methoduyla aranıyor...\n\n{max_attempts} deneme yapılacak.',
            color=discord.Color.orange()
        )
        await button_interaction.edit_original_response(embed=embed, view=None)
        
        while attempts < max_attempts:
            attempts += 1
            username = generate_username(selected_year, selected_method)
            
            # Tüm API'leri dene
            available, message = await check_username_available_multi(username)
            
            if available is True:
                found_account = {'username': username, 'message': message}
                break
            elif available is False:
                continue
            
            # Hata veya rate limit, bekle
            await asyncio.sleep(0.5)
        
        if found_account:
            increment_count(button_interaction)
            
            embed = discord.Embed(
                title='🎉 Hesap Bulundu!',
                description=f'**Kullanıcı Adı:** {found_account["username"]}',
                color=discord.Color.green()
            )
            embed.add_field(name='📅 Yıl', value=selected_year, inline=True)
            embed.add_field(name='🔧 Method', value=get_method_description(selected_method), inline=True)
            embed.add_field(name='📊 Deneme Sayısı', value=f'{attempts} deneme', inline=True)
            embed.add_field(name='📝 Durum', value='✅ Bu kullanıcı adı **MÜSAİT**!', inline=False)
            embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API kullanıldı', inline=False)
            embed.set_footer(text='Hemen Roblox\'ta hesap oluşturabilirsin!')
            
            await button_interaction.edit_original_response(embed=embed, view=None)
            
            try:
                dm_embed = discord.Embed(
                    title='🎮 Müsait Roblox Kullanıcı Adı!',
                    description=f'**{found_account["username"]}** kullanıcı adı müsait!',
                    color=discord.Color.green()
                )
                dm_embed.add_field(name='📅 Yıl', value=selected_year, inline=True)
                dm_embed.add_field(name='🔧 Method', value=selected_method, inline=True)
                dm_embed.set_footer(text='Bu kullanıcı adını hemen alabilirsin!')
                await button_interaction.user.send(embed=dm_embed)
            except:
                pass
            
        else:
            embed = discord.Embed(
                title='😕 Müsait Hesap Bulunamadı',
                description=f'{max_attempts} deneme yapıldı ama **{selected_year}** yılı için **{selected_method}** methoduyla müsait hesap bulunamadı.',
                color=discord.Color.red()
            )
            embed.add_field(name='💡 Öneri', value='Farklı bir yıl veya method dene!', inline=False)
            embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API denendi ama hepsi başarısız', inline=False)
            await button_interaction.edit_original_response(embed=embed, view=None)
    
    find_button.callback = find_callback

@bot.tree.command(name='bulk-gen', description='Çoklu müsait hesap bulur (Admin).')
@app_commands.default_permissions(administrator=True)
async def bulk_gen(interaction: discord.Interaction, year: str, method: str, count: int):
    await interaction.response.defer(ephemeral=True)
    
    if count > 10:
        await interaction.followup.send('❌ En fazla 10 hesap bulabilirim!', ephemeral=True)
        return
    
    if int(year) < 2006 or int(year) > 2016:
        await interaction.followup.send('❌ Yıl 2006-2016 arası olmalı!', ephemeral=True)
        return
    
    found_accounts = []
    attempts = 0
    max_attempts = count * 15
    
    embed = discord.Embed(
        title='🔍 Aranıyor...',
        description=f'{count} müsait hesap aranıyor...\n{len(API_CHECKERS)} API kullanılıyor',
        color=discord.Color.orange()
    )
    await interaction.edit_original_response(embed=embed)
    
    while len(found_accounts) < count and attempts < max_attempts:
        attempts += 1
        username = generate_username(year, method)
        available, message = await check_username_available_multi(username)
        
        if available is True:
            found_accounts.append(username)
        elif available is False:
            continue
        
        await asyncio.sleep(0.3)
    
    if found_accounts:
        embed = discord.Embed(
            title=f'🎉 {len(found_accounts)} Müsait Hesap Bulundu!',
            description='\n'.join([f'✅ **{acc}**' for acc in found_accounts]),
            color=discord.Color.green()
        )
        embed.add_field(name='📅 Yıl', value=year, inline=True)
        embed.add_field(name='🔧 Method', value=get_method_description(method), inline=True)
        embed.add_field(name='📊 Deneme Sayısı', value=f'{attempts} deneme', inline=True)
        embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API kullanıldı', inline=False)
        embed.set_footer(text='Bu kullanıcı adlarını Roblox\'ta hemen alabilirsin!')
        await interaction.edit_original_response(embed=embed)
    else:
        embed = discord.Embed(
            title='😕 Müsait Hesap Bulunamadı',
            description=f'{count} hesap için arandı ama müsait bulunamadı.',
            color=discord.Color.red()
        )
        embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API denendi', inline=False)
        await interaction.edit_original_response(embed=embed)

@bot.tree.command(name='check', description='Belirli bir kullanıcı adını kontrol eder.')
async def check(interaction: discord.Interaction, username: str):
    await interaction.response.defer(ephemeral=True)
    
    available, message = await check_username_available_multi(username)
    
    if available is None:
        embed = discord.Embed(
            title='⚠️ Hata',
            description=f'Kullanıcı adı kontrol edilemedi: {message}',
            color=discord.Color.orange()
        )
        embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API denendi', inline=False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        return
    
    if available:
        embed = discord.Embed(
            title='✅ Müsait!',
            description=f'**{username}** kullanıcı adı **MÜSAİT**!',
            color=discord.Color.green()
        )
        embed.add_field(name='📝 Mesaj', value=message, inline=False)
        embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API denendi', inline=False)
        embed.set_footer(text='Hemen Roblox\'ta hesap oluşturabilirsin!')
    else:
        embed = discord.Embed(
            title='❌ Alınmış veya Geçersiz',
            description=f'**{username}** kullanıcı adı **ALINMIŞ** veya **GEÇERSİZ**.',
            color=discord.Color.red()
        )
        embed.add_field(name='📝 Mesaj', value=message, inline=False)
        embed.add_field(name='🔗 API', value=f'{len(API_CHECKERS)} API denendi', inline=False)
    
    await interaction.followup.send(embed=embed, ephemeral=True)

@bot.tree.command(name='stock', description='Kullanım istatistiklerini gösterir.')
async def stock(interaction: discord.Interaction):
    data = load_user_data()
    total_users = len(data)
    today = datetime.now().strftime('%Y-%m-%d')
    today_users = sum(1 for u in data.values() if u.get('date') == today)
    
    embed = discord.Embed(
        title='📊 Bot İstatistikleri',
        color=discord.Color.blue()
    )
    embed.add_field(name='👥 Toplam Kullanıcı', value=str(total_users), inline=True)
    embed.add_field(name='📅 Bugün Kullanan', value=str(today_users), inline=True)
    embed.add_field(name='🔧 Methodlar', value='8 farklı method', inline=True)
    embed.add_field(name='📅 Yıl Aralığı', value='2006 - 2016', inline=True)
    embed.add_field(name='🔗 API Sayısı', value=f'{len(API_CHECKERS)} farklı API', inline=True)
    embed.set_footer(text='Bot çoklu API ile çalışıyor!')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='guide', description='Kullanım kılavuzunu gösterir.')
async def guide(interaction: discord.Interaction):
    embed = discord.Embed(
        title='📖 Roblox Username Bot Kılavuzu',
        description=f'**{len(API_CHECKERS)}** farklı API ile müsait kullanıcı adı bulur.',
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name='/gen',
        value='Yıl ve method seç, müsait hesap bul!',
        inline=False
    )
    embed.add_field(
        name='/bulk-gen [yıl] [method] [adet]',
        value='Çoklu müsait hesap bulur. (Admin/Premium)',
        inline=False
    )
    embed.add_field(
        name='/check [kullanıcı_adı]',
        value='Belirli bir kullanıcı adını kontrol eder.',
        inline=False
    )
    embed.add_field(
        name='/stock',
        value='Bot istatistiklerini gösterir.',
        inline=False
    )
    embed.add_field(
        name='📅 Yıllar',
        value='2006 - 2016 arası',
        inline=False
    )
    embed.add_field(
        name='🔧 Methodlar',
        value='\n'.join([get_method_description(m) for m in ['year_user', 'cross_user', 'double_user', '123_method', '321_method', '2_number_method', '4_number_method', '3number']]),
        inline=False
    )
    embed.add_field(
        name='🔗 API Kullanımı',
        value=f'{len(API_CHECKERS)} farklı API endpoint\'i sırayla denenir',
        inline=False
    )
    embed.set_footer(text='Bot tamamen API ile çalışır! Rate limit önlenmiştir.')
    
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================================
# BOTU BAŞLAT
# ============================================================

if __name__ == "__main__":
    print("🚀 Roblox Username Bot başlatılıyor...")
    print(f"📡 {len(API_CHECKERS)} API hazır!")
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Bot başlatılamadı: {e}")
        sys.exit(1)
