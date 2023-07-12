import discord
import requests, random, json, base64
from textwrap import wrap

client = discord.Client()

def update_bot_activities(mode, username):
    try:
        if mode == 'start':
            data = {
                "mode":"update_activities",
                "nickname":username,
                "queue":"start"
            }
            response = requests.post('http://pvpbooster.pl/api/miner.php', data=data).text
            return True
        elif mode == 'stop':
            data = {
                "mode":"update_activities",
                "nickname":username,
                "queue":"stop"
            }
            response = requests.post('http://pvpbooster.pl/api/miner.php', data=data).text
            return True
        elif mode == 'check':
            data = {
                "mode":"get_activities",
                "nickname":username,
            }
            response = requests.post('http://pvpbooster.pl/api/miner.php', data=data).text
            response_json = json.loads(response)
            if response_json['status'] == 'success':
                return response_json['queue']
            return True
        elif mode == 'wyjdz':
            data = {
                "mode":"update_activities",
                "nickname":username,
                "queue":"exit"
            }
            response = requests.post('http://pvpbooster.pl/api/miner.php', data=data).text
            response_json = json.loads(response)
            return response_json
    except:
        return False

def user_connection(mode, username, discord_id):
    try:
        if mode == 'sprawdz':
            data = {
                "mode":"check_user",
                "username":username,
                "discord_id":discord_id
            }
            response = requests.post(f'http://pvpbooster.pl/api/dc_user.php', data=data).text
            if response == 'all data matches':
                return True
            return False
        elif mode == 'dodaj':
            data = {
                "mode":"insert_user",
                "username":username,
                "discord_id":discord_id
            }
            response = requests.post(f'http://srv46402.seohost.com.pl/api/dc_user.php', data=data).text
            if 'success' in response:
                return True
            else:
                return False
        elif mode == 'usun':
            data = {
                "mode":"delete_user",
                "username":username,
            }
            response = requests.post(f'http://srv46402.seohost.com.pl/api/dc_user.php', data=data).text
            if 'success' in response:
                return True
            else:
                return False
        elif mode == 'reset':
            data = {
                "mode":"update_user",
                "username":username,
                "discord_id":discord_id
            }
            response = requests.post(f'http://srv46402.seohost.com.pl/api/dc_user.php', data=data).text
            if response == 'success':
                return True
            else:
                return False
    except:
        return False

def send_stats(username, action):
    pass

def generate_key(type, time):
    try:
        st1 = ''.join(random.choice('abcdef0123456789') for _ in range(24))
        key = 'key-'+st1
        data = {
            "mode":"assert_key",
            "key":key,
            "key_type":type,
            "key_durability":time
        }
        response = requests.post(f'http://srv46402.seohost.com.pl/api/keys', data=data).text
        print(response)
        if "nie wstawiono parametrow klucza" in response:
            return False
        else:
            return [response, key]
    except:
        return False

def server_status():
    try:
        data = {
            "mode":"status"
        }
        response = requests.post('http://srv46402.seohost.com.pl/api/connection.php', data=data).text
        api_response = json.loads(response)
        if api_response['status'] == 'on going':
            return True
    except:
        return False

@client.event
async def on_ready():
    print(f'logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.guild_permissions.administrator:
        if message.content.startswith('$pomoc'):
            await message.channel.send(f"""Wszystkie obecne komendy do dyzpozycji! ```yaml\n$clear - czysci czat\n$generuj PLAN(premium,standard,trial) DNI - generuje klucz licencyjny\n$dc TRYB(sprawdz,dodaj,usun,reset) NICK - akcje zwiazane z podpiętym kontem dc użytkownika\n$hwid TRYB(sprawdz,dodaj,usun,reset) - zmiany hwid uzytkownika\n$status TRYB(start,stop,sprawdz,wyjdz) NICK - sprawdza status kopacza\n$serwer - zwraca status serwera```""", reference=message)
        
        elif message.content.startswith('$clear'):
            await message.channel.purge()

        elif message.content.startswith('$tete'):
            await message.channel.send("""```ini
[test] dwad
```""", reference=message)

        elif message.content.startswith('$2tete'):
            await message.channel.send("""```css
[test] dwad
```""", reference=message)

        elif message.content.startswith('$generuj'):
            args = str(message.content).split(' ')
            status = generate_key(args[1], args[2])
            if status == False:
                #await message.channel.send(f'Błąd!', reference=message)
                await message.channel.send("""```css
[ERROR] Błąd!
```""", reference=message)
            else:
                await message.channel.send(f"""```ini
[SUCCESS] - {status[1]}
```""", reference=message)
                #await message.channel.send(f'[SUCCESS] - {status[1]}')
        
        elif message.content.startswith('$hwid'):
            args = str(message.content).split(' ')
            if args[1] == 'check':
                status = user_connection(args[1], args[2], message.author.id)
                if status == True:
                    await message.channel.send('[SUCCESS] - Znaleziono użytkownika!', reference=message)
                else:
                    await message.channel.send('[ERROR] - Nie znaleziono użytkownika!', reference=message)
            elif args[1] == 'add':
                status = user_connection(args[1], args[2], message.author.id)
                if status == True:
                    await message.channel.send('[SUCCESS] - Dodano użytkownika!', reference=message)
                else:
                    await message.channel.send('[ERROR] - Nie dodano użytkownika!', reference=message)
            elif args[1] == 'delete':
                status = user_connection(args[1], args[2], message.author.id)
                if status == True:
                    await message.channel.send('[SUCCESS] - Usunięto użytkownika!', reference=message)
                else:
                    await message.channel.send('[ERROR] - Nie usunięto użytkownika!', reference=message)
            elif args[1] == 'reset':
                status = user_connection(args[1], args[2], message.author.id)
                if status == True:
                    await message.channel.send('[SUCCESS] - Zresetowano hwid!', reference=message)
                else:
                    await message.channel.send('[ERROR] - Nie zresetowano hwid!', reference=message)
            else:
                await message.channel.send('[ERROR] - Wpisz $pomoc!', reference=message)
        
        elif message.content.startswith('$status'):
            args = str(message.content).split(' ')
            if args[1] == 'start':
                if update_bot_activities('start', args[2]) == True:
                    await message.channel.send('[SUCCESS] - Uruchomiono kopacza!', reference=message)
                else:
                    await message.channel.send('error start false')
            elif args[1] == 'stop':
                if update_bot_activities('stop', args[2]) == True:
                    await message.channel.send('[SUCCESS] - Zatrzymano kopacza!', reference=message)
                else:
                    await message.channel.send('error stop false')
            elif args[1] == 'sprawdz':
                status = update_bot_activities('check', args[2])
                if status != False:
                    await message.channel.send(f'[SUCCESS] - Status kopacza: {status}', reference=message)
                else:
                    await message.channel.send('[ERROR] Kopacz wyłączony!')
            elif args[1] == 'wyjdz':
                status = update_bot_activities('wyjdz', args[2])
                await message.channel.send(status)
                #if update_bot_activities('wyjdz', args[2]) == True:
                #    await message.channel.send('[SUCCESS] - Zamknięto okna!', reference=message)
                #else:
                #    await message.channel.send('error start false')
            else:
                await message.channel.send('error type')
        
        elif message.content.startswith('$serwer'):
            status = server_status()
            if status == True:
                await message.channel.send(f"""```ini
[SUCCESS] - Serwer działa!
```""", reference=message)
            else:
                await message.channel.send("""```css
[ERROR] - Serwer nie działa!
```""", reference=message)
        
        else:
            if message.content.startswith('$'):
                await message.channel.send('[ERROR] - Wpisz $pomoc!', reference=message)

client.run('TOKEN')