import discord
from discord.ext import commands
import asyncio

TOKENLER = [
    '1', # token 1
    '12', # token 2
    '123'  # token 3
]

KANAL_ID = 1357293476575707399 # voice channel id
MP3_YOLU = '2.mp3' # mp3
FFMPEG_YOLU = r'/ffmpeg/bin/ffmpeg.exe' # ffmpeg

class SesBot(commands.Bot):
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.token = token
        self.voice_client = None

    async def on_ready(self):
        print(f' [{self.user}] - Token found.')
        kanal = self.get_channel(KANAL_ID)
        if kanal is None:
            print(' [{self.user}] - Not found!')
            return
        try:
            self.voice_client = await kanal.connect()
            print(f' [{self.user}] - Connected.')
            self.cal_mp3()
        except Exception as e:
            print(f' {self.user}] - Error: {e}')

    def cal_mp3(self):
        def tekrar_oynat(error=None):
            if error:
                print(f'[Bot] Hata: {error}')
            if self.voice_client:
                self.voice_client.play(
                    discord.FFmpegPCMAudio(MP3_YOLU, executable=FFMPEG_YOLU),
                    after=lambda e: tekrar_oynat(e)
                    
                )
        tekrar_oynat()
        print(f' [{self.user}] - Playing.')

    def run_bot(self):
        self.run(self.token)

async def baslat_butun_botlar():
    botlar = []
    for token in TOKENLER:
        bot = SesBot(token)
        botlar.append(bot)
        asyncio.create_task(bot.start(token))
    while True:
        await asyncio.sleep(10)

asyncio.run(baslat_butun_botlar())
