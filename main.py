import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re , socket , threading , ssl , pytz , aiohttp , asyncio
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import * ; from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from Pb2 import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from cfonts import render, say

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# Enhanced Configuration Variables
ADMIN_UID = "1249734385"
server2 = "IND"
key2 = "JWAXPRIME"
BYPASS_TOKEN = "your_bypass_token_here"

# Optimized Global Variables
online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
is_muted = False
mute_until = 0
spam_requests_sent = 0
bot_start_time = time.time()

# Enhanced Performance Optimizations
connection_pool = None
command_cache = {}
last_request_time = {}
RATE_LIMIT_DELAY = 0.1  # 100ms delay between requests
MAX_CACHE_SIZE = 50
CLEANUP_INTERVAL = 300  # 5 minutes

# Command Performance Tracking
command_stats = {}

# --------------------------------------------------

def cleanup_cache():
    """Clean old cached data to maintain performance"""
    current_time = time.time()
    # Clean last_request_time
    to_remove = [k for k, v in last_request_time.items() 
                 if current_time - v > CLEANUP_INTERVAL]
    for k in to_remove:
        last_request_time.pop(k, None)
    
    # Clean command_cache if too large
    if len(command_cache) > MAX_CACHE_SIZE:
        oldest_keys = sorted(command_cache.keys())[:len(command_cache)//2]
        for key in oldest_keys:
            command_cache.pop(key, None)

def get_rate_limited_response(user_id):
    """Implement rate limiting to reduce server load"""
    user_key = str(user_id)
    current_time = time.time()
    
    if user_key in last_request_time:
        time_since_last = current_time - last_request_time[user_key]
        if time_since_last < RATE_LIMIT_DELAY:
            return False
    
    last_request_time[user_key] = current_time
    return True

# Optimized Clan Info Function with Caching
def Get_clan_info(clan_id):
    cache_key = f"clan_{clan_id}"
    if cache_key in command_cache:
        return command_cache[cache_key]
    
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            # Shortened response for better performance
            result = f"""[11EAFD][b][c]°°°°GUILD°°°°
[00FF00]Name: {data['clan_name']}
[00FF00]Lvl: {data['level']} | Rank: {data['rank']}
[00FF00]Members: {data['guild_details']['total_members']}/{data['guild_details']['members_online']} online
[11EAFD]°°°°EH MUNNA BOT°°°°
[FFB300]DEV: APPLE GAMING FF"""
            command_cache[cache_key] = result
            cleanup_cache()
            return result
        else:
            return "[FF0000]Failed to get clan info"
    except:
        return "[FF0000]Error fetching clan data"

# Enhanced Player Info Function with Caching
def get_player_info(player_id):
    cache_key = f"player_{player_id}"
    if cache_key in command_cache:
        return command_cache[cache_key]
        
    url = f"https://danger-info-alpha.vercel.app/accinfo?uid={player_id}&key=DANGERxINFO"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            r = response.json()
            result = {
                "Name": r.get('nickname', 'N/A'),
                "UID": r.get('accountId', 'N/A'), 
                "Level": r.get('level', 'N/A'),
                "Likes": r.get('likes', 'N/A'),
                "Region": r.get('region', 'N/A'),
                "Booyah Pass": r.get('booyah_pass_level', 'N/A'),
            }
            command_cache[cache_key] = result
            cleanup_cache()
            return result
    except:
        pass
    return {"error": "Failed to fetch data"}

# Optimized Spam Function - Now sends group requests
def spam_requests(player_id):
    global spam_requests_sent
    cache_key = f"spam_{player_id}"
    
    if cache_key in command_cache:
        return command_cache[cache_key]
    
    try:
        # Enhanced spam API call for group requests
        url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
        res = requests.get(url, timeout=15)
        
        if res.status_code == 200:
            data = res.json()
            spam_requests_sent += 1
            success_count = data.get('success_count', 0)
            failed_count = data.get('failed_count', 0)
            
            result = f"[FF6347]Group Requests Sent!\n[00FF00]✅ Success: {success_count}\n[FF0000]❌ Failed: {failed_count}"
            command_cache[cache_key] = result
            cleanup_cache()
            return result
        else:
            # Try alternative spam API
            try:
                alt_url = f"https://danger-info-alpha.vercel.app/spam?uid={player_id}&server={server2}&key={key2}"
                alt_res = requests.get(alt_url, timeout=15)
                if alt_res.status_code == 200:
                    alt_data = alt_res.json()
                    spam_requests_sent += 1
                    result = f"[FF6347]Group Requests Sent!\n[00FF00]✅ Success: {alt_data.get('success', 0)}\n[FF0000]❌ Failed: {alt_data.get('failed', 0)}"
                    command_cache[cache_key] = result
                    cleanup_cache()
                    return result
            except:
                pass
            return f"[FF0000]API Error: {res.status_code}"
    except:
        return "[FF0000]Spam API connection failed"

# Simple AI Chat Function
async def talk_with_ai(question):
    try:
        # Simple response for AI (you can enhance this later)
        responses = [
            "Hello! How can I help you today?",
            "I'm here to assist you with any questions.",
            "That's an interesting point! Tell me more.",
            "I understand your concern. What would you like to know?",
            "Thanks for sharing that with me!",
            "I appreciate you reaching out. How can I assist?"
        ]
        import random
        return random.choice(responses)
    except:
        return "AI service temporarily unavailable"

# Enhanced Info Function
def newinfo(uid):
    cache_key = f"info_{uid}"
    if cache_key in command_cache:
        return command_cache[cache_key]
        
    url = f"https://danger-info-alpha.vercel.app/accinfo?uid={uid}&key=DANGERxINFO"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            result = {"status": "ok", "data": data}
            command_cache[cache_key] = result
            cleanup_cache()
            return result
        return {"status": "error", "message": f"API Error: {response.status_code}"}
    except:
        return {"status": "error", "message": "Network error"}

# Optimized Likes Function
def send_likes(uid):
    try:
        likes_api_response = requests.get(
            f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
            timeout=10
        )
        
        if likes_api_response.status_code != 200:
            return f"[FF0000]Like API Error: {likes_api_response.status_code}"

        api_json_response = likes_api_response.json()
        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)

        if status == 1 and likes_added > 0:
            # Shortened response
            return f"""[C][B][11EAFD]━━━━━
[00FF00]✅ Likes Sent!
[FFFFFF]Player: {player_name}
[FFFFFF]Likes: {likes_added}
[11EAFD]━━━━━
[FFB300]EH MUNNA BOT"""
        else:
            return f"""[C][B][FF0000]━━━━━
[FFFFFF]❌ No Likes Sent!
[FF6347]Player may have already claimed
[FF0000]━━━━━"""

    except:
        return "[FF0000]Like API connection failed"

# --------------------------------------------------
# Headers
Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': 'v1 1',
    'ReleaseVersion': "OB51"
}

# Random Color Function
def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]", "[7CFC00]", "[B22222]",
        "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]", "[DDA0DD]", "[E6E6FA]",
        "[2E8B57]", "[3CB371]", "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]"
    ]
    return random.choice(colors)

# Helper Functions
def is_admin(uid):
    return str(uid) == ADMIN_UID

def is_bot_muted():
    global is_muted, mute_until
    if is_muted and time.time() < mute_until:
        return True
    elif is_muted and time.time() >= mute_until:
        is_muted = False
        mute_until = 0
        return False
    return False

def update_command_stats(command):
    """Track command usage for optimization"""
    if command not in command_stats:
        command_stats[command] = 0
    command_stats[command] += 1

# --------------------------------------------------
# Crypto Functions (unchanged)
async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload
    
async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    try:
        async with connection_pool.post(url, headers=Hr, data=data) as response:
            if response.status != 200: 
                return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)
    except:
        return (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWAUOUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    try:
        async with connection_pool.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: 
                return await response.read()
            return None
    except:
        return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    try:
        async with connection_pool.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: 
                return await response.read()
            return None
    except:
        return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto
    
async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto
    
async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: 
        headers = '0000000'
    elif uid_length == 8: 
        headers = '00000000'
    elif uid_length == 10: 
        headers = '000000'
    elif uid_length == 7: 
        headers = '000000000'
    else: 
        print('Unexpected length') 
        headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"
     
async def cHTypE(H):
    if not H: 
        return 'Squid'
    elif H == 1: 
        return 'CLan'
    elif H == 2: 
        return 'PrivaTe'
    
async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': 
        msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': 
        msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': 
        msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: 
        whisper_writer.write(PacKeT) 
        await whisper_writer.drain()
    elif TypE == 'OnLine': 
        online_writer.write(PacKeT) 
        await online_writer.drain()
    else: 
        return 'UnsoPorTed TypE ! >> ErrrroR (:():)' 
           

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer , spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , XX , uid , Spy,data2, Chat_Leave
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            while True:
                data2 = await reader.read(9999)
                if not data2: 
                    break
                
                if data2.hex().startswith('0500') and len(data2.hex()) > 1000:
                    try:
                        packet = await DeCode_PackEt(data2.hex()[10:])
                        packet = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet)

                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)

                        message = f'[B][C]{get_random_color()}\n🎯 EH MUNNA BOT Online!\n{B}[C][00FF00]Commands: Use /help'
                        P = await SEndMsG(0 , message , OwNer_UiD , OwNer_UiD , key , iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , P)

                    except Exception as e:
                        pass

            online_writer.close() 
            await online_writer.wait_closed() 
            online_writer = None

        except Exception as e: 
            print(f"- ErroR With {ip}:{port} - {e}") 
            online_writer = None
        await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')

    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, is_muted, mute_until
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: 
                    whisper_writer.write(pK) 
                    await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: 
                    break
                
                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                    except:
                        response = None

                    if response:
                        # Rate limiting check
                        if not get_rate_limited_response(uid):
                            continue

                        # Check if bot is muted
                        if is_bot_muted():
                            continue

                        # ENHANCED COMMAND PROCESSING - WORKS EVERYWHERE
                        # Priority 1: Fast response commands
                        
                        # DEBUG COMMAND - Always responds first
                        if inPuTMsG.strip() == "/debug":
                            update_command_stats("debug")
                            debug_msg = f"[FF0000]✅ EH MUNNA BOT ONLINE! UID: {uid}"
                            P = await SEndMsG(response.Data.chat_type, debug_msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            continue
                            
                        # HELP COMMAND - Short version for all chat types
                        if inPuTMsG.startswith("/help"):
                            update_command_stats("help")
                            print(f"Help triggered by {uid}")
                            if is_admin(uid):
                                message = f"""[C][B][2E8B57]EH MUNNA BOT
━━━━━━━━━━━━━━━━━
[00CED1]/like/[UID] → 100 likes
[87CEEB]/x/[CODE] → Join squad  
[FF6347]/e [UID] [EMOTE] → Single emote
[FF6347]/e [UID1] [UID2] [UID3] [UID4] [EMOTE] → Multi emote
[FFD700]/3,/5,/6 → Create squad
[98FB98]/solo → Leave squad
[F0E68C]/s → Speed boost
[20B2AA]/info [UID] → Player info
[7FFF00]/clan [ID] → Clan info
[00FF7F]/visit [UID] → Send visits
[F0E68C]/ai [Q] → AI chat
[B22222]/spam [UID/UIDs] → Group req
[FFA500]/ee [TEAM] [UIDs] [E] → Join+Emote+Leave
━━━━━━━━━━━━━━━━━
[DC143C]/stop,/mute,/unmute
━━━━━━━━━━━━━━━━━
[00CED1]DEV: APPLE GAMING FF"""
                            else:
                                message = f"""[C][B][2E8B57]EH MUNNA BOT
━━━━━━━━━━━━━━━━━
[00CED1]/like/[UID] → 100 likes
[87CEEB]/x/[CODE] → Join squad
[FF6347]/e [UID] [EMOTE] → Single emote  
[FF6347]/e [UIDs] [EMOTE] → Multi emote
[FFD700]/3,/5,/6 → Create squad
[98FB98]/solo → Leave squad
[F0E68C]/s → Speed boost
[20B2AA]/info [UID] → Player info
[7FFF00]/clan [ID] → Clan info
[00FF7F]/visit [UID] → Send visits
[F0E68C]/ai [Q] → AI chat
[FFA500]/ee [TEAM] [UIDs] [E] → Join+Emote+Leave
━━━━━━━━━━━━━━━━━
[00CED1]DEV: EH PROGRAMAR X"""
                            
                            try:
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                fallback_msg = "[FF0000]EH MUNNA BOT online! Use /help"
                                P = await SEndMsG(response.Data.chat_type, fallback_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            continue
                        
                        # NEW: /ee COMMAND - Team Code + Multi-UID Emote
                        if inPuTMsG.startswith('/ee '):
                            update_command_stats("ee")
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) >= 4:  # Minimum: /ee team_code uid1 uid2 emote_id
                                    team_code = parts[1]  # First parameter is team code
                                    uids = []
                                    emote_id = None
                                    
                                    # Middle parameters are UIDs, last parameter is emote_id
                                    for i, part in enumerate(parts[2:], 2):  # Start from index 2 (after team code)
                                        if i < len(parts) - 1:  # All except last parameter are UIDs
                                            if part.isdigit():
                                                uids.append(int(part))
                                        else:  # Last parameter is emote ID
                                            if part.isdigit():
                                                emote_id = int(part)
                                    
                                    if len(uids) >= 1 and emote_id:
                                        # Send processing message
                                        processing_msg = f"[FFD700][B]━━━━━━━\n[FFFFFF]Joining: {team_code}\n[FFFFFF]UIDs: {len(uids)}\n[FFFFFF]🎭 Emote: {emote_id}\n[FFD700]━━━━━━━"
                                        P = await SEndMsG(response.Data.chat_type, processing_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        
                                        # Step 1: Join the team using team code
                                        try:
                                            join_msg = f"[FF6347][B]🎯 Joining Team: {team_code}"
                                            P_join = await SEndMsG(response.Data.chat_type, join_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_join)
                                            
                                            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            await asyncio.sleep(2)  # Wait for join to complete
                                        except:
                                            pass
                                        
                                        # Step 2: Send emotes to all UIDs
                                        success_count = 0
                                        for target_uid in uids:
                                            try:
                                                H = await Emote_k(target_uid, emote_id, key, iv, region)
                                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                                success_count += 1
                                                await asyncio.sleep(0.3)  # Delay between emotes
                                            except:
                                                pass
                                        
                                        # Step 3: Immediately leave the team
                                        try:
                                            leave_msg = f"[FF0000][B]🚪 Leaving Team: {team_code}"
                                            P_leave = await SEndMsG(response.Data.chat_type, leave_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_leave)
                                            
                                            leave_packet = await ExiT(None, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
                                        except:
                                            pass
                                        
                                        # Confirmation
                                        confirm_msg = f"[00FF00][B]━━━━━━━\n[FFFFFF]✅ Team Emote Complete!\n[FFFFFF]Success: {success_count}/{len(uids)}\n[FFFFFF]Team: {team_code}\n[FFFFFF]🔄 Auto-Leave: ✅\n[FFD700]━━━━━━━"
                                        P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                                    else:
                                        error_msg = f"[FF0000]Usage: /ee [TEAM_CODE] [UID1] [UID2] [UID3] [EMOTE]\nExample: /ee FAST123 1234 5678 9012 1\n[B22222]Will auto-join team and leave after emotes"
                                        P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /ee [TEAM_CODE] [UID1] [UID2] [UID3] [EMOTE]\nExample: /ee FAST123 1234 5678 9012 1\n[B22222]Will auto-join team and leave after emotes"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                error_msg = f"[FF0000]/ee command error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            continue
                        
                        # ADMIN COMMANDS (enhanced and shortened)
                        if inPuTMsG.startswith('/stop') and is_admin(uid):
                            update_command_stats("stop")
                            stop_msg = f"[FF0000]EH MUNNA BOT stopping..."
                            P = await SEndMsG(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            await connection_pool.close()
                            os._exit(0)
                            
                        elif inPuTMsG.startswith('/mute') and is_admin(uid):
                            update_command_stats("mute")
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2:
                                    time_str = parts[1]
                                    if time_str.endswith('s'):
                                        duration = int(time_str[:-1])
                                    elif time_str.endswith('m'):
                                        duration = int(time_str[:-1]) * 60
                                    elif time_str.endswith('h'):
                                        duration = int(time_str[:-1]) * 3600
                                    else:
                                        duration = int(time_str) * 60
                                    
                                    is_muted = True
                                    mute_until = time.time() + duration
                                    mute_msg = f"[FFB300]AP BOT muted {time_str}"
                                else:
                                    mute_msg = f"[FF0000]Usage: /mute 30s/5m/1h"
                                    
                                P = await SEndMsG(response.Data.chat_type, mute_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Invalid time format"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                        elif inPuTMsG.startswith('/unmute') and is_admin(uid):
                            update_command_stats("unmute")
                            is_muted = False
                            mute_until = 0
                            unmute_msg = f"[00FF00]AP BOT unmuted"
                            P = await SEndMsG(response.Data.chat_type, unmute_msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            
                        elif inPuTMsG.startswith('/spam') and is_admin(uid):
                            update_command_stats("spam")
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2:
                                    uids = []
                                    for part in parts[1:]:
                                        if part.isdigit():
                                            uids.append(part)
                                    
                                    if uids:
                                        # Send processing message
                                        processing_msg = f"[FF6347][B]━━━━━━━\n[FFFFFF]Group Requests: {len(uids)} UIDs\n[FF6347]━━━━━━━"
                                        P = await SEndMsG(response.Data.chat_type, processing_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        
                                        # Send spam to each UID
                                        total_success = 0
                                        total_failed = 0
                                        
                                        for target_uid in uids:
                                            try:
                                                spam_result = spam_requests(target_uid)
                                                # Parse result to count success/failed
                                                if "Success:" in spam_result:
                                                    success_count = int(spam_result.split("Success:")[1].split("\n")[0].split()[0])
                                                    failed_count = int(spam_result.split("Failed:")[1].split("\n")[0].split()[0])
                                                    total_success += success_count
                                                    total_failed += failed_count
                                                await asyncio.sleep(0.3)  # Small delay between requests
                                            except:
                                                total_failed += 1
                                        
                                        # Final result
                                        final_result = f"[FF6347][B]━━━━━━━\n[00FF00]✅ Total Success: {total_success}\n[FF0000]❌ Total Failed: {total_failed}\n[FF6347]━━━━━━━\n[FFB300]EH MUNNA BOT"
                                        P = await SEndMsG(response.Data.chat_type, final_result, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    else:
                                        error_msg = f"[FF0000]Usage: /spam [UID] or /spam [UID1] [UID2] [UID3] [UID4]"
                                        P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /spam [UID] or /spam [UID1] [UID2] [UID3] [UID4]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Spam error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                        
                        # ENHANCED COMMANDS - WORK EVERYWHERE
                        elif inPuTMsG.startswith('/like/'):
                            update_command_stats("like")
                            try:
                                target_uid = inPuTMsG.split('/like/')[1].strip()
                                if target_uid.isdigit():
                                    processing_msg = f"[FFD700]Processing... UID: {target_uid}"
                                    P = await SEndMsG(response.Data.chat_type, processing_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                    
                                    like_result = send_likes(target_uid)
                                    P = await SEndMsG(response.Data.chat_type, like_result, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Invalid UID"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Like error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                        elif inPuTMsG.startswith('/visit'):
                            update_command_stats("visit")
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2 and parts[1].isdigit():
                                    visit_url = f"https://api-visit-ag-team-alliff.vercel.app/visit?uid={parts[1]}"
                                    visit_response = requests.get(visit_url, timeout=5)
                                    
                                    if visit_response.status_code == 200:
                                        visit_data = visit_response.json()
                                        visit_result = f"""[C][B][00CED1]━━━━━━━
[FFFFFF]Visit: ✅ Success
[FFFFFF]Player: {parts[1]}
[C][B][00CED1]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                    else:
                                        visit_result = f"[FF0000]Visit failed: {visit_response.status_code}"
                                        
                                    P = await SEndMsG(response.Data.chat_type, visit_result, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /visit [UID]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Visit error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                        elif inPuTMsG.startswith('/info'):
                            update_command_stats("info")
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2 and parts[1].isdigit():
                                    info_result = newinfo(parts[1])
                                    if info_result.get('status') == 'ok':
                                        data = info_result.get('data', {})
                                        info_msg = f"""[C][B][11EAFD]━━━━━━━
[00FF00]Name: {data.get('nickname', 'N/A')}
[00FF00]UID: {data.get('accountId', 'N/A')}
[00FF00]Level: {data.get('level', 'N/A')}
[00FF00]Likes: {data.get('likes', 'N/A')}
[11EAFD]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                    else:
                                        info_msg = f"[FF0000]Error: {info_result.get('message', 'Failed')}"
                                        
                                    P = await SEndMsG(response.Data.chat_type, info_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /info [UID]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Info error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                        elif inPuTMsG.startswith('/clan'):
                            update_command_stats("clan")
                            try:
                                parts = inPuTMsG.split()
                                if len(parts) >= 2:
                                    clan_result = Get_clan_info(parts[1])
                                    P = await SEndMsG(response.Data.chat_type, clan_result, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /clan [CLAN_ID]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except:
                                error_msg = f"[FF0000]Clan error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                        # /ai COMMAND REMOVED - NO LONGER AVAILABLE

                        # SQUAD COMMANDS (enhanced)
                        elif inPuTMsG.startswith('/3') or inPuTMsG.startswith('/5') or inPuTMsG.startswith('/6'):
                            update_command_stats("squad_create")
                            try:
                                # Check if user is in squad (available everywhere)
                                squad_size = int(inPuTMsG[1])
                                
                                message = f"[B][C]{get_random_color()}\n🎯 {squad_size}-Player Squad!\nAccept Fast"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                
                                PAc = await OpEnSq(key, iv, region)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                C = await cHSq(squad_size, uid, key, iv, region)
                                await asyncio.sleep(0.3)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                V = await SEnd_InV(squad_size, uid, key, iv, region)
                                await asyncio.sleep(0.3)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                E = await ExiT(None, key, iv)
                                await asyncio.sleep(2)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                                
                                confirm_msg = f"[00FF00][B]✅ {squad_size}-Player Squad!"
                                P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                            except Exception as e:
                                print(f'Error in {inPuTMsG} command')
                                
                        elif inPuTMsG.startswith('/solo'):
                            update_command_stats("solo")
                            try:
                                message = f"[FF6347][B]Leaving Squad..."
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                leave = await ExiT(uid, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave)
                                
                                confirm_msg = f"[00FF00][B]✅ Left Squad!"
                                P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                            except:
                                pass
                                
                        elif inPuTMsG.strip().startswith('/s'):
                            update_command_stats("speed")
                            try:
                                message = f"[FFD700][B]🚀 Speed Boost!"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                EM = await FS(key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                
                                confirm_msg = f"[00FF00][B]✅ Speed Boosted!"
                                P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                            except:
                                pass

                        # /e EMOTE COMMAND - Both Single and Multi-UID Support
                        elif inPuTMsG.strip().startswith('/e '):
                            update_command_stats("emote")
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) >= 3:  # Minimum /e uid emote_id
                                    try:
                                        # Check if it's single or multi-UID format
                                        if len(parts) == 3:  # /e {uid} {emote_id}
                                            target_uid = int(parts[1])
                                            emote_id = int(parts[2])
                                            
                                            # Send processing message
                                            message = f'[B][C]{get_random_color()}\n🎭 Emote: {emote_id} → {target_uid}'
                                            P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            
                                            # Send emote
                                            H = await Emote_k(target_uid, emote_id, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                            
                                            confirm_msg = f"[00FF00][B]✅ Emote Sent!"
                                            P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                                            
                                        elif len(parts) >= 4:  # Multi-UID: /e {uid1} {uid2} {...} {emote_id}
                                            uids = []
                                            emote_id = None
                                            
                                            # All parameters except last one are UIDs, last one is emote_id
                                            for i, part in enumerate(parts[1:], 1):
                                                if i < len(parts) - 1:  # All except last parameter are UIDs
                                                    if part.isdigit():
                                                        uids.append(int(part))
                                                else:  # Last parameter is emote ID
                                                    if part.isdigit():
                                                        emote_id = int(part)
                                            
                                            if len(uids) >= 1 and emote_id:
                                                # Send processing message
                                                message = f'[B][C]{get_random_color()}\n🎭 Multi-Emote: {len(uids)} UIDs\nEmote ID: {emote_id}'
                                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                                
                                                # Send emotes to all UIDs
                                                success_count = 0
                                                for target_uid in uids:
                                                    try:
                                                        H = await Emote_k(target_uid, emote_id, key, iv, region)
                                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                                        success_count += 1
                                                        await asyncio.sleep(0.2)  # Small delay between emotes
                                                    except:
                                                        pass
                                                
                                                confirm_msg = f"[00FF00][B]✅ Multi-Emote Sent! {success_count}/{len(uids)}"
                                                P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                                            else:
                                                error_msg = f"[FF0000]Invalid format. Use:\n/e [UID] [EMOTE]\n/e [UID1] [UID2] [UID3] [UID4] [EMOTE]"
                                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        else:
                                            error_msg = f"[FF0000]Usage: /e [UID] [EMOTE] or /e [UID1] [UID2] [UID3] [UID4] [EMOTE]"
                                            P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            
                                    except ValueError:
                                        error_msg = f"[FF0000]Invalid UID or Emote ID. Use numbers only."
                                        P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /e [UID] [EMOTE] or /e [UID1] [UID2] [UID3] [UID4] [EMOTE]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                            except Exception as e:
                                print(f"Error in /e command: {e}")

                        # /x/ JOIN SQUAD COMMAND (enhanced)
                        elif inPuTMsG.startswith('/x/'):
                            update_command_stats("join_squad")
                            try:
                                Code = inPuTMsG.split('/x/')[1]
                                message = f"[B][C]{get_random_color()}\n🎯 Joining: {Code}"
                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                EM = await GenJoinSquadsPacket(Code, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                
                                confirm_msg = f"[00FF00][B]✅ Join Request! Code: {Code}"
                                P_confirm = await SEndMsG(response.Data.chat_type, confirm_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P_confirm)
                            except:
                                print("Error in /x command")

                        # AI COMMAND - Flexible parameter handling
                        if inPuTMsG.strip().startswith('/ai '):
                            update_command_stats("ai")
                            try:
                                parts = inPuTMsG.strip().split()
                                if len(parts) >= 2:  # Minimum: /ai question
                                    try:
                                        # Check if it's single or multi-format
                                        if len(parts) == 2:  # /ai [question]
                                            question = parts[1]
                                            
                                            # Send processing message
                                            message = f'[B][C]{get_random_color()}\n🤖 AI Chat: {question[:50]}{"..." if len(question) > 50 else ""}'
                                            P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            
                                            # Get AI response
                                            ai_response = await talk_with_ai(question)
                                            
                                            ai_msg = f"""[C][B][00CED1]━━━━━━━
[FFFFFF]AI: {ai_response}
[00CED1]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                            P = await SEndMsG(response.Data.chat_type, ai_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            
                                        elif len(parts) >= 3:  # Multi-format: /ai [something] [message]
                                            uids = []
                                            question = None
                                            
                                            # Check if first few parts are UIDs, last is message
                                            for i, part in enumerate(parts[1:], 1):
                                                if part.isdigit() and len(part) >= 8:  # Likely a UID (8+ digits)
                                                    uids.append(int(part))
                                                else:  # This is the message
                                                    question = ' '.join(parts[i:])
                                                    break
                                            
                                            if question:
                                                # Send processing message
                                                if uids:
                                                    message = f'[B][C]{get_random_color()}\n🤖 AI Chat: {len(uids)} UIDs\nMessage: {question[:30]}{"..." if len(question) > 30 else ""}'
                                                else:
                                                    message = f'[B][C]{get_random_color()}\n🤖 AI Chat: {question[:50]}{"..." if len(question) > 50 else ""}'
                                                P = await SEndMsG(response.Data.chat_type, message, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                                
                                                # Get AI response
                                                ai_response = await talk_with_ai(question)
                                                
                                                ai_msg = f"""[C][B][00CED1]━━━━━━━
[FFFFFF]AI: {ai_response}
[00CED1]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                                P = await SEndMsG(response.Data.chat_type, ai_msg, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            else:
                                                # If no valid message found, use all parts as message
                                                question = ' '.join(parts[1:])
                                                ai_response = await talk_with_ai(question)
                                                ai_msg = f"""[C][B][00CED1]━━━━━━━
[FFFFFF]AI: {ai_response}
[00CED1]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                                P = await SEndMsG(response.Data.chat_type, ai_msg, uid, chat_id, key, iv)
                                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                        else:
                                            error_msg = f"[FF0000]Usage: /ai [question] or /ai [UIDs] [message]"
                                            P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                            
                                    except Exception as e:
                                        # Fallback to simple question handling
                                        question = ' '.join(parts[1:])
                                        ai_response = await talk_with_ai(question)
                                        ai_msg = f"""[C][B][00CED1]━━━━━━━
[FFFFFF]AI: {ai_response}
[00CED1]━━━━━━━
[FFB300]EH MUNNA BOT"""
                                        P = await SEndMsG(response.Data.chat_type, ai_msg, uid, chat_id, key, iv)
                                        await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                                else:
                                    error_msg = f"[FF0000]Usage: /ai [question]"
                                    P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            except Exception as e:
                                error_msg = f"[FF0000]AI service error"
                                P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)

                        # UNKNOWN COMMAND (enhanced)
                        elif inPuTMsG.startswith('/'):
                            update_command_stats("unknown")
                            error_msg = f"[FF0000]Unknown command. Use /help\n[FFB300]EH MUNNA BOT"
                            P = await SEndMsG(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
                            
                        response = None
                        
            whisper_writer.close() 
            await whisper_writer.wait_closed() 
            whisper_writer = None
                    	
        except Exception as e: 
            print(f"ErroR {ip}:{port} - {e}") 
            whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    global connection_pool
    # Enhanced connection pool configuration
    connection_pool = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=20),
        connector=aiohttp.TCPConnector(limit=20, limit_per_host=10)
    )
    
    Uid , Pw = '4350805021','071D800512E554B460FE06725F76E9E8E14D9E19E9E54FB055C178EF58534D96'

    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: 
        print("ErroR - InvaLid AccounT") 
        return None
    
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: 
        print("TarGeT AccounT => BannEd / NoT ReGisTeReD ! ") 
        return None
    
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    print(UrL)
    region = MajoRLoGinauTh.region

    ToKen = MajoRLoGinauTh.token
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: 
        print("ErroR - GeTinG PorTs From LoGin DaTa !") 
        return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    print(ToKen)
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
     
    await ready_event.wait()
    await asyncio.sleep(1)
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    os.system('clear')
    print(render('EH MUNNA BOT', colors=['white', 'green'], align='center'))
    print('')
    print(f" - EH MUNNA BOT STarTinG And OnLine on TarGet : {TarGeT} | BOT NAME : {acc_name}\n")
    print(f" - BoT sTaTus > GooD | OnLinE ! (:")    
    print(f" - DEV: EH PROGRAMAR X| Bot Uptime: {time.strftime('%H:%M:%S', time.gmtime(time.time() - bot_start_time))}")    
    await asyncio.gather(task1 , task2)
    
async def StarTinG():
    while True:
        try: 
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except asyncio.TimeoutError: 
            print("Token ExpiRed ! , ResTartinG")
        except Exception as e: 
            print(f"ErroR TcP - {e} => ResTarTinG ...")

if __name__ == '__main__':
    asyncio.run(StarTinG())