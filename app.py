import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = "8585664250:AAE00pAF5SVNPwdpwgkNE8XK9dO-NsWQLpU"
SUPERADMIN_ID = 7790487358

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class AdminStates(StatesGroup):
    waiting_for_custom_limit = State()
    waiting_for_admin_id = State()

# --- LUG'ATLAR (Ko'p tillilik tizimi) ---
LANGS = {
    "uz": {
        "start": "Assalomu alaykum, **{name}**! 👋\n\nBu guruhlarni himoya qiluvchi va tartibga soluvchi professional tizim.",
        "admin_start": "Assalomu alaykum, **{name}**! 👑\n\nSiz tizimning boshqaruvchisiz. Quyidagi tugma orqali boshqaruv markaziga o'ting:",
        "btn_add_group": "➕ Guruhga botni qo'shish",
        "btn_admin_panel": "💎 Ultimate Admin Panel",
        "btn_manual": "📖 Botdan foydalanish qo'llanmasi",
        "btn_lang": "🌐 Tilni o'zgartirish",
        "btn_test_out": "🚶‍♂️ Tashqariga chiqish (Oddiy odam bo'lish)",
        "btn_test_in": "📥 Ichkariga kirish (Adminlikni yoqish)",
        "not_admin_test": "⚠️ **Kechirasiz, siz hozir 'Tashqarida' (Test rejimidarisiz)!**\n\nSiz bot nazarida oddiy foydalanuvchisiz va admin emassiz. Admin huquqini qaytarish uchun quyidagi tugmani bosing:",
        "back": "🔙 Orqaga",
        "panel_title": "💎 **ULTIMATE BOSHQARUV MARKAZI**\n\nBoshqarish uchun o'zingiz admin bo'lgan guruhni tanlang:",
        "no_groups": "\n\n⚠️ Faol guruhlar topilmadi. Avval botni guruhingizga qo'shib, admin bering.",
        "manual_text": "📖 **Botdan foydalanish qo'llanmasi:**\n\n1. Botni guruhingizga qo'shing va **Admin** huquqini bering.\n2. Lichkada /start bosing va **Ultimate Admin Panel** orqali guruhingizni tanlang.",
        "lang_select": "🌐 Bot uchun tilni tanlang:",
        "lang_changed": "✅ Til muvaffaqiyatli o'zgartirildi!",
        "limit_title": "📊 Yangi limit miqdorini tanlang:",
        "custom_limit_prompt": "✍️ Guruh uchun yangi limit sonini raqamlarda yuboring:",
        "admin_list_title": "👑 **Guruh adminlari ro'yxati:**\n\n⭐ Superadmin: `{super_id}`\n",
        "add_admin_prompt": "👤 Admin qilmoqchi bo'lgan foydalanuvchining **Telegram ID raqamini** yuboring:",
        "status_changed": "✅ Holat o'zgartirildi: {val}",
        "access_allowed": "✅ Tabriklayman! Sizga yozish ruxsati berildi.",
        "not_enough": "❌ Hali yetarli odam qo'shmadingiz! Yana {rem} ta kerak.",
        "group_header": "🎛 **Guruh:** {title}\n━━━━━━━━━━━━━━━━━━━\n📊 Odam limiti: **{limit} ta**\n🛡️ Anti-reklama: **{antispam}**\n📞 Kontakt filtr: **{contact}**\n🔒 Moderatsiya: **{moderation}**\n🔇 Silent Mode: **{silent}**\n🤖 AI Rejim: **{ai}**\n🌐 Til: **{lang_name}**\n━━━━━━━━━━━━━━━━━━━"
    },
    "ru": {
        "start": "Здравствуйте, **{name}**! 👋",
        "admin_start": "Здравствуйте, **{name}**! 👑",
        "btn_add_group": "➕ Добавить бота в группу",
        "btn_admin_panel": "💎 Ultimate Админ Панель",
        "btn_manual": "📖 Руководство",
        "btn_lang": "🌐 Изменить язык",
        "btn_test_out": "🚶‍♂️ Выйти наружу (Обычный пользователь)",
        "btn_test_in": "📥 Войти внутрь (Вернуть админку)",
        "not_admin_test": "⚠️ **Вы находитесь вне системы (в тестовом режиме)!**",
        "back": "🔙 Назад",
        "panel_title": "💎 **ЦЕНТР УПРАВЛЕНИЯ**",
        "no_groups": "\n\n⚠️ Группы не найдены.",
        "manual_text": "📖 Руководство пользователя...",
        "lang_select": "🌐 Выберите язык:",
        "lang_changed": "✅ Язык изменен!",
        "limit_title": "📊 Выберите лимит:",
        "custom_limit_prompt": "✍️ Отправьте лимит цифрами:",
        "admin_list_title": "👑 **Список админов:**\n\n⭐ Супердмин: `{super_id}`\n",
        "add_admin_prompt": "👤 Отправьте Telegram ID:",
        "status_changed": "✅ Статус изменен: {val}",
        "access_allowed": "✅ Доступ разрешен!",
        "not_enough": "❌ Недостаточно людей!",
        "group_header": "🎛 **Группа:** {title}\n📊 Лимит: **{limit}**"
    },
    "en": {
        "start": "Hello, **{name}**! 👋",
        "admin_start": "Hello, **{name}**! 👑",
        "btn_add_group": "➕ Add bot to group",
        "btn_admin_panel": "💎 Ultimate Admin Panel",
        "btn_manual": "📖 Guide",
        "btn_lang": "🌐 Change Language",
        "btn_test_out": "🚶‍♂️ Step Outside (Be regular user)",
        "btn_test_in": "📥 Step Inside (Restore Admin)",
        "not_admin_test": "⚠️ **You are currently in outside/test mode!**",
        "back": "🔙 Back",
        "panel_title": "💎 **CONTROL CENTER**",
        "no_groups": "\n\n⚠️ No groups found.",
        "manual_text": "📖 Guide...",
        "lang_select": "🌐 Select language:",
        "lang_changed": "✅ Language changed!",
        "limit_title": "📊 Select limit:",
        "custom_limit_prompt": "✍️ Send limit:",
        "admin_list_title": "👑 **Admins:**\n\n⭐ Superadmin: `{super_id}`\n",
        "add_admin_prompt": "👤 Send Telegram ID:",
        "status_changed": "✅ Status changed: {val}",
        "access_allowed": "✅ Access granted!",
        "not_enough": "❌ Not enough people!",
        "group_header": "🎛 **Group:** {title}\n📊 Limit: **{limit}**"
    },
    "zh": {
        "start": "你好，**{name}**！ 👋",
        "admin_start": "你好，**{name}**！ 👑",
        "btn_add_group": "➕ 添加到群组",
        "btn_admin_panel": "💎 管理面板",
        "btn_manual": "📖 指南",
        "btn_lang": "🌐 语言",
        "btn_test_out": "🚶‍♂️ 外部模式",
        "btn_test_in": "📥 内部模式",
        "not_admin_test": "⚠️ **您目前处于外部测试模式！**",
        "back": "🔙 返回",
        "panel_title": "💎 **控制中心**",
        "no_groups": "\n\n⚠️ 未找到群组。",
        "manual_text": "📖 指南...",
        "lang_select": "🌐 选择语言：",
        "lang_changed": "✅ 已更改！",
        "limit_title": "📊 选择限制：",
        "custom_limit_prompt": "✍️ 发送限制：",
        "admin_list_title": "👑 **管理员：**\n\n⭐ 超管：`{super_id}`\n",
        "add_admin_prompt": "👤 发送 ID：",
        "status_changed": "✅ 更改：{val}",
        "access_allowed": "✅ 允许！",
        "not_enough": "❌ 不足！",
        "group_header": "🎛 **群组：** {title}"
    }
}

LANG_NAMES = {
    "uz": "O'zbekcha 🇺🇿",
    "ru": "Русский 🇷🇺",
    "en": "English 🇬🇧",
    "zh": "中文 🇨🇳"
}

# --- BAZA BILAN ISHLASH ---
def init_db():
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS groups (chat_id INTEGER PRIMARY KEY, chat_title TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER, chat_id INTEGER, invited_count INTEGER DEFAULT 0, is_allowed INTEGER DEFAULT 0, PRIMARY KEY (user_id, chat_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS invited_members (chat_id INTEGER, inviter_id INTEGER, new_user_id INTEGER, PRIMARY KEY (chat_id, new_user_id))")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS group_settings (
            chat_id INTEGER PRIMARY KEY,
            required_limit INTEGER DEFAULT 15,
            antispam_status TEXT DEFAULT "ON",
            moderation_status TEXT DEFAULT "ON",
            silent_mode TEXT DEFAULT "OFF",
            contact_filter TEXT DEFAULT "OFF",
            ai_mode TEXT DEFAULT "OFF",
            flood_limit INTEGER DEFAULT 500,
            required_channel TEXT DEFAULT "Yo'q",
            language TEXT DEFAULT "uz"
        )
    """)
    cursor.execute("CREATE TABLE IF NOT EXISTS user_global_lang (user_id INTEGER PRIMARY KEY, language TEXT DEFAULT 'uz')")
    cursor.execute("CREATE TABLE IF NOT EXISTS group_admins (chat_id INTEGER, admin_id INTEGER, admin_username TEXT, PRIMARY KEY (chat_id, admin_id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS test_modes (user_id INTEGER PRIMARY KEY, is_outside INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

init_db()

def get_user_lang(user_id: int) -> str:
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT language FROM user_global_lang WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else "uz"

def set_user_lang(user_id: int, lang: str):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_global_lang (user_id, language) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET language = ?", (user_id, lang, lang))
    conn.commit()
    conn.close()

def save_group(chat_id: int, chat_title: str):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groups (chat_id, chat_title) VALUES (?, ?) ON CONFLICT(chat_id) DO UPDATE SET chat_title = ?", (chat_id, chat_title, chat_title))
    conn.commit()
    conn.close()

def delete_group_from_db(chat_id: int):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groups WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM group_settings WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM group_admins WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM users WHERE chat_id = ?", (chat_id,))
    cursor.execute("DELETE FROM invited_members WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

def get_settings(chat_id: int):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT required_limit, antispam_status, moderation_status, silent_mode, contact_filter, ai_mode, flood_limit, required_channel, language FROM group_settings WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "limit": row[0], "antispam": row[1], "moderation": row[2],
            "silent": row[3], "contact": row[4], "ai": row[5], "flood": row[6], "channel": row[7], "lang": row[8]
        }
    return {"limit": 15, "antispam": "ON", "moderation": "ON", "silent": "OFF", "contact": "OFF", "ai": "OFF", "flood": 500, "channel": "Yo'q", "lang": "uz"}

def update_setting_db(chat_id: int, column: str, value):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT chat_id FROM group_settings WHERE chat_id = ?", (chat_id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO group_settings (chat_id) VALUES (?)", (chat_id,))
    cursor.execute(f"UPDATE group_settings SET {column} = ? WHERE chat_id = ?", (value, chat_id))
    conn.commit()
    conn.close()

# --- TEST REJIMI (TASHQARIDA / ICHKARIDA) FUNKSIYALARI ---
def is_user_outside(user_id: int) -> bool:
    if user_id != SUPERADMIN_ID:
        return False
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT is_outside FROM test_modes WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] == 1 if row else False

def set_test_mode(user_id: int, is_outside: int):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_modes (user_id, is_outside) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET is_outside = ?", (user_id, is_outside, is_outside))
    conn.commit()
    conn.close()

def is_global_admin(user_id: int) -> bool:
    if user_id == SUPERADMIN_ID:
        if is_user_outside(user_id):
            return False 
        return True
     
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM group_admins WHERE admin_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def is_admin(chat_id: int, user_id: int) -> bool:
    if user_id == SUPERADMIN_ID and is_user_outside(user_id):
        return False
         
    if user_id == SUPERADMIN_ID:
        return True
         
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM group_admins WHERE chat_id = ? AND admin_id = ?", (chat_id, user_id))
    row = cursor.fetchone()
    conn.close()
     
    return row is not None

def get_user_allowed_groups(user_id: int):
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    if user_id == SUPERADMIN_ID and not is_user_outside(user_id):
        cursor.execute("SELECT chat_id, chat_title FROM groups")
    else:
        cursor.execute("SELECT g.chat_id, g.chat_title FROM groups g JOIN group_admins a ON g.chat_id = a.chat_id WHERE a.admin_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_user_invited_count(user_id: int, chat_id: int) -> int:
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM invited_members WHERE chat_id = ? AND inviter_id = ?", (chat_id, user_id))
    count = cursor.fetchone()[0]
    conn.close()
    return count


# --- START VA ASOSIY MENYU ---
async def send_start_menu(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    lang = get_user_lang(user_id)
    t = LANGS.get(lang, LANGS["uz"])
    bot_info = await bot.get_me()
     
    if user_id == SUPERADMIN_ID and is_user_outside(user_id):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=t["btn_test_in"], callback_data="test_mode_inside")],
            [InlineKeyboardButton(text=t["btn_lang"], callback_data="global_lang_menu")]
        ])
        await message.answer(t["not_admin_test"], reply_markup=keyboard)
        return

    keyboard_buttons = [
        [InlineKeyboardButton(text=t["btn_add_group"], url=f"https://t.me/{bot_info.username}?startgroup=true")],
        [
            InlineKeyboardButton(text=t["btn_manual"], callback_data="help_manual"),
            InlineKeyboardButton(text=t["btn_lang"], callback_data="global_lang_menu")
        ]
    ]
     
    if is_global_admin(user_id):
        keyboard_buttons.insert(0, [InlineKeyboardButton(text=t["btn_admin_panel"], callback_data="open_admin_panel")])
        if user_id == SUPERADMIN_ID:
            keyboard_buttons.append([InlineKeyboardButton(text=t["btn_test_out"], callback_data="test_mode_outside")])
        text = t["admin_start"].format(name=message.from_user.first_name)
    else:
        text = t["start"].format(name=message.from_user.first_name)
         
    await message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))

@dp.message(F.chat.type == "private", Command("start"))
async def private_start_handler(message: Message, state: FSMContext):
    await send_start_menu(message, state)


# --- TEST REJIMINI BOSHQARISH (TASHQARIDA / ICHKARIDA) ---
@dp.callback_query(F.data == "test_mode_outside")
async def callback_test_outside(callback: CallbackQuery, state: FSMContext):
    set_test_mode(callback.from_user.id, 1)
    await callback.answer("🚶‍♂️ Siz hozir 'Tashqarida' (Test rejimi)ga chiqdingiz. Bot nazarida oddiy foydalanuvchisiz!", show_alert=True)
    await send_start_menu(callback.message, state)

@dp.callback_query(F.data == "test_mode_inside")
async def callback_test_inside(callback: CallbackQuery, state: FSMContext):
    set_test_mode(callback.from_user.id, 0)
    await callback.answer("📥 Xush kelibsiz! Superadmin huquqlari to'liq tiklandi.", show_alert=True)
    await send_start_menu(callback.message, state)


# --- GLOBAL TIL MENYUSI ---
@dp.callback_query(F.data == "global_lang_menu")
async def callback_global_lang_menu(callback: CallbackQuery):
    keyboard_buttons = []
    for code, name in LANG_NAMES.items():
        keyboard_buttons.append([InlineKeyboardButton(text=name, callback_data=f"set_glob_lang_{code}")])
    keyboard_buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_start")])
     
    await callback.message.edit_text("🌐 Tilni tanlang / Select language:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
    await callback.answer()

@dp.callback_query(F.data.startswith("set_glob_lang_"))
async def callback_set_global_lang(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[3]
    set_user_lang(callback.from_user.id, lang_code)
    await callback.answer("✅ Til o'zgartirildi!", show_alert=True)
    await send_start_menu(callback.message, state)


@dp.callback_query(F.data == "help_manual")
async def callback_help_manual(callback: CallbackQuery):
    lang = get_user_lang(callback.from_user.id)
    t = LANGS.get(lang, LANGS["uz"])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=t["back"], callback_data="back_to_start")]])
    await callback.message.edit_text(t["manual_text"], reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(F.data == "open_admin_panel")
async def callback_open_admin_panel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    lang = get_user_lang(user_id)
    t = LANGS.get(lang, LANGS["uz"])
     
    if not is_global_admin(user_id):
        await callback.answer("⚠️ Huquqingiz yo'q!", show_alert=True)
        return
         
    groups = get_user_allowed_groups(user_id)
    text = t["panel_title"]
    keyboard_buttons = []
     
    valid_groups = []
    for g_id, g_title in groups:
        try:
            member = await bot.get_chat_member(g_id, bot.id)
            if member.status in ("administrator", "member"):
                valid_groups.append((g_id, g_title))
        except:
            pass

    if valid_groups:
        for g_id, g_title in valid_groups:
            keyboard_buttons.append([InlineKeyboardButton(text=f"📌 {g_title}", callback_data=f"manage_group_{g_id}")])
    else:
        text += t["no_groups"]
         
    keyboard_buttons.append([InlineKeyboardButton(text=t["back"], callback_data="back_to_start")])
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
    await callback.answer()


@dp.callback_query(F.data == "back_to_start")
async def callback_back_to_start(callback: CallbackQuery, state: FSMContext):
    await send_start_menu(callback.message, state)
    await callback.answer()


# --- GURUH BOSHQARUVI ---
async def show_group_menu(callback: CallbackQuery, chat_id: int):
    st = get_settings(chat_id)
    lang = st['lang']
    t = LANGS.get(lang, LANGS["uz"])
     
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chat_title FROM groups WHERE chat_id = ?", (chat_id,))
    row = cursor.fetchone()
    title = row[0] if row else "Guruh"
    conn.close()
     
    lang_name = LANG_NAMES.get(lang, "O'zbekcha")
     
    text = t["group_header"].format(
        title=title, limit=st['limit'], antispam=st['antispam'],
        contact=st['contact'], moderation=st['moderation'],
        silent=st['silent'], ai=st['ai'], lang_name=lang_name
    )
     
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Limitni o'zgartirish", callback_data=f"setlimit_menu_{chat_id}")],
        [
            InlineKeyboardButton(text=f"🛡️ Reklama: {st['antispam']}", callback_data=f"tog_{chat_id}_antispam"),
            InlineKeyboardButton(text=f"📞 Kontakt: {st['contact']}", callback_data=f"tog_{chat_id}_contact")
        ],
        [
            InlineKeyboardButton(text=f"🔒 Moderatsiya: {st['moderation']}", callback_data=f"tog_{chat_id}_moderation"),
            InlineKeyboardButton(text=f"🔇 Mute: {st['silent']}", callback_data=f"tog_{chat_id}_silent")
        ],
        [
            InlineKeyboardButton(text=f"🤖 AI Rejim: {st['ai']}", callback_data=f"tog_{chat_id}_ai"),
            InlineKeyboardButton(text=f"🌐 Til: {lang_name}", callback_data=f"group_lang_menu_{chat_id}")
        ],
        [InlineKeyboardButton(text="👑 Adminlarni Boshqarish", callback_data=f"admins_menu_{chat_id}")],
        [InlineKeyboardButton(text="🚪 Guruhni botdan chiqarish", callback_data=f"leave_group_{chat_id}")],
        [InlineKeyboardButton(text=t["back"], callback_data="open_admin_panel")]
    ])
     
    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("manage_group_"))
async def callback_manage_group(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
     
    if not is_admin(chat_id, user_id):
        await callback.answer("⚠️ Ruxsat yo'q!", show_alert=True)
        return
         
    await show_group_menu(callback, chat_id)
    await callback.answer()


@dp.callback_query(F.data.startswith("leave_group_"))
async def callback_leave_group(callback: CallbackQuery, state: FSMContext):
    chat_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
     
    if not is_admin(chat_id, user_id):
        await callback.answer("⚠️ Ruxsat yo'q!", show_alert=True)
        return
         
    try:
        await bot.leave_chat(chat_id)
    except:
        pass
         
    delete_group_from_db(chat_id)
    await callback.answer("✅ Bot guruhdan chiqarib yuborildi!", show_alert=True)
     
    class DummyCallback:
        message = callback.message
        from_user = callback.from_user
        async def answer(self, *args, **kwargs): pass
         
    await callback_open_admin_panel(DummyCallback(), state)


@dp.callback_query(F.data.startswith("tog_"))
async def callback_toggle(callback: CallbackQuery):
    parts = callback.data.split("_")
    chat_id = int(parts[1])
    key_type = parts[2]
     
    st = get_settings(chat_id)
    column_map = {
        "antispam": "antispam_status",
        "contact": "contact_filter",
        "moderation": "moderation_status",
        "silent": "silent_mode",
        "ai": "ai_mode"
    }
     
    col_name = column_map[key_type]
    current_val = st[key_type]
    new_val = "OFF" if current_val == "ON" else "ON"
     
    update_setting_db(chat_id, col_name, new_val)
    await show_group_menu(callback, chat_id)
     
    t = LANGS.get(st['lang'], LANGS["uz"])
    await callback.answer(t["status_changed"].format(val=new_val), show_alert=True)


@dp.callback_query(F.data.startswith("group_lang_menu_"))
async def callback_group_lang_menu(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[3])
    keyboard_buttons = []
    for code, name in LANG_NAMES.items():
        keyboard_buttons.append([InlineKeyboardButton(text=name, callback_data=f"set_g_lang_{chat_id}_{code}")])
    keyboard_buttons.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"manage_group_{chat_id}")])
     
    await callback.message.edit_text("🌐 Guruh uchun tilni tanlang:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
    await callback.answer()

@dp.callback_query(F.data.startswith("set_g_lang_"))
async def callback_set_group_lang(callback: CallbackQuery):
    parts = callback.data.split("_")
    chat_id = int(parts[3])
    lang_code = parts[4]
     
    update_setting_db(chat_id, "language", lang_code)
    await show_group_menu(callback, chat_id)
    await callback.answer("✅ Guruh tili o'zgartirildi!", show_alert=True)


@dp.callback_query(F.data.startswith("setlimit_menu_"))
async def callback_setlimit_menu(callback: CallbackQuery):
    chat_id = int(callback.data.split("_")[2])
    st = get_settings(chat_id)
    t = LANGS.get(st['lang'], LANGS["uz"])
     
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="5", callback_data=f"changelimit_{chat_id}_5"),
            InlineKeyboardButton(text="10", callback_data=f"changelimit_{chat_id}_10"),
            InlineKeyboardButton(text="15", callback_data=f"changelimit_{chat_id}_15"),
            InlineKeyboardButton(text="20", callback_data=f"changelimit_{chat_id}_20"),
        ],
        [
            InlineKeyboardButton(text="30", callback_data=f"changelimit_{chat_id}_30"),
            InlineKeyboardButton(text="50", callback_data=f"changelimit_{chat_id}_50"),
            InlineKeyboardButton(text="100", callback_data=f"changelimit_{chat_id}_100"),
        ],
        [InlineKeyboardButton(text="✍️ Maxsus son kiritish", callback_data=f"custom_limit_{chat_id}")],
        [InlineKeyboardButton(text=t["back"], callback_data=f"manage_group_{chat_id}")]
    ])
    await callback.message.edit_text(t["limit_title"], reply_markup=keyboard)
    await callback.answer()

@dp.callback_query(F.data.startswith("changelimit_"))
async def callback_changelimit(callback: CallbackQuery):
    parts = callback.data.split("_")
    chat_id = int(parts[1])
    val = int(parts[2])
    update_setting_db(chat_id, "required_limit", val)
    await show_group_menu(callback, chat_id)
    await callback.answer(f"✅ Limit {val} taga o'zgartirildi!", show_alert=True)

@dp.callback_query(F.data.startswith("custom_limit_"))
async def callback_custom_limit(callback: CallbackQuery, state: FSMContext):
    chat_id = int(callback.data.split("_")[2])
    st = get_settings(chat_id)
    t = LANGS.get(st['lang'], LANGS["uz"])
     
    await state.set_state(AdminStates.waiting_for_custom_limit)
    await state.update_data(chat_id=chat_id)
    await callback.message.answer(t["custom_limit_prompt"])
    await callback.answer()

@dp.message(AdminStates.waiting_for_custom_limit, F.chat.type == "private")
async def process_custom_limit(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, raqam kiriting!")
        return
    data = await state.get_data()
    val = int(message.text)
    chat_id = data.get("chat_id")
    update_setting_db(chat_id, "required_limit", val)
    await state.clear()
    await message.answer(f"✅ Muvaffaqiyatli! Limit **{val} ta** qilindi.")


# --- ADMINLARNI BOSHQARISH ---
@dp.callback_query(F.data.startswith("admins_menu_"))
async def callback_admins_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = int(callback.data.split("_")[2])
    st = get_settings(chat_id)
    t = LANGS.get(st['lang'], LANGS["uz"])
     
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT admin_id, admin_username FROM group_admins WHERE chat_id = ?", (chat_id,))
    admins = cursor.fetchall()
    conn.close()
     
    text = t["admin_list_title"].format(super_id=SUPERADMIN_ID)
    keyboard_buttons = []
     
    if admins:
        for idx, adm in enumerate(admins, 1):
            text += f"{idx}. {adm[1]} (`{adm[0]}`)\n"
            keyboard_buttons.append([InlineKeyboardButton(text=f"🗑️ O'chirish: {adm[1]}", callback_data=f"del_adm_{chat_id}_{adm[0]}")])
    else:
        text += "\nQo'shimcha adminlar mavjud emas.\n"
         
    keyboard_buttons.append([InlineKeyboardButton(text="➕ Admin qo'shish", callback_data=f"add_adm_menu_{chat_id}")])
    keyboard_buttons.append([InlineKeyboardButton(text=t["back"], callback_data=f"manage_group_{chat_id}")])
     
    await callback.message.edit_text(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_buttons))
    await callback.answer()

@dp.callback_query(F.data.startswith("add_adm_menu_"))
async def callback_add_adm_menu(callback: CallbackQuery, state: FSMContext):
    chat_id = int(callback.data.split("_")[3])
    st = get_settings(chat_id)
    t = LANGS.get(st['lang'], LANGS["uz"])
     
    await state.set_state(AdminStates.waiting_for_admin_id)
    await state.update_data(chat_id=chat_id)
    await callback.message.answer(t["add_admin_prompt"])
    await callback.answer()

@dp.message(AdminStates.waiting_for_admin_id, F.chat.type == "private")
async def process_add_admin(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Faqat raqamli ID kiriting.")
        return
    new_id = int(message.text)
    data = await state.get_data()
    chat_id = data.get("chat_id")
     
    try:
        m = await bot.get_chat_member(chat_id, new_id)
        uname = f"@{m.user.username}" if m.user.username else m.user.first_name
    except:
        uname = f"ID: {new_id}"
         
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO group_admins (chat_id, admin_id, admin_username) VALUES (?, ?, ?)", (chat_id, new_id, uname))
        conn.commit()
        await message.answer(f"✅ Muvaffaqiyatli! **{uname}** (`{new_id}`) ushbu guruhga admin qilindi va endi u ham admin paneldan boshqara oladi.")
    except:
        await message.answer("⚠️ Bu foydalanuvchi allaqachon admin!")
    finally:
        conn.close()
        await state.clear()

@dp.callback_query(F.data.startswith("del_adm_"))
async def callback_del_admin(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    chat_id = int(parts[2])
    admin_id = int(parts[3])
     
    conn = sqlite3.connect("ultimate_bot_v3.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM group_admins WHERE chat_id = ? AND admin_id = ?", (chat_id, admin_id))
    conn.commit()
    conn.close()
     
    await callback.answer("✅ Admin o'chirildi!", show_alert=True)
    await callback_admins_menu(callback, state)


# --- GURUH FILTERLARI VA XABAR TEKSHIRUVI ---
@dp.chat_member()
async def member_added(event: ChatMemberUpdated):
    save_group(event.chat.id, event.chat.title)
    if event.new_chat_member.status == "member" and event.from_user:
        if not event.new_chat_member.user.is_bot and event.from_user.id != event.new_chat_member.user.id:
            conn = sqlite3.connect("ultimate_bot_v3.db")
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO invited_members (chat_id, inviter_id, new_user_id) VALUES (?, ?, ?)", (event.chat.id, event.from_user.id, event.new_chat_member.user.id))
                conn.commit()
            except sqlite3.IntegrityError:
                pass
            conn.close()


@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_filters(message: Message):
    if not message.from_user: return
    save_group(message.chat.id, message.chat.title)
    user_id = message.from_user.id
    chat_id = message.chat.id
    st = get_settings(chat_id)
    lang = st['lang']
     
    # Faqatgina bot bazasida rasmiy admin bo'lganlar erkin yoza oladi
    if is_admin(chat_id, user_id):
        return

    # Silent Mode
    if st["silent"] == "ON":
        try: await message.delete()
        except: pass
        return

    # Anti-reklama
    if st["antispam"] == "ON" and message.text and any(w in message.text.lower() for w in ["t.me/", "http://", "https://", "@"]):
        try:
            await message.delete()
            w = await message.answer(f"**{message.from_user.first_name}**, ⚠️ Reklama taqiqlangan!")
            await asyncio.sleep(4)
            await w.delete()
        except: pass
        return

    if st["moderation"] == "OFF":
        return

    # Odam qo'shish shartini tekshirish
    current_count = get_user_invited_count(user_id, chat_id)
    limit = st["limit"]

    if current_count >= limit:
        # Ruxsat berilganligini bazaga saqlab qo'yamiz
        conn = sqlite3.connect("ultimate_bot_v3.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, chat_id, invited_count, is_allowed) VALUES (?, ?, ?, 1) ON CONFLICT(user_id, chat_id) DO UPDATE SET is_allowed = 1, invited_count = ?", (user_id, chat_id, current_count, current_count))
        conn.commit()
        conn.close()
        return

    # Agar yetarli odam qo'shmagan bo'lsa, xabarni o'chiramiz va ogohlantiramiz
    try:
        await message.delete()
        rem = limit - current_count
        msg = await message.answer(f"❌ **{message.from_user.first_name}**, guruhga xabar yozish uchun yana **{rem} ta** odam qo'shishingiz kerak! (Hozirgi: {current_count}/{limit})")
        await asyncio.sleep(5)
        await msg.delete()
    except:
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())