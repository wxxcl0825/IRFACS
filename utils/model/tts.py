import os
import asyncio
import edge_tts
from pydub import AudioSegment
import simpleaudio as sa
from utils.paths import *


def mp32wav(fp):
    song = AudioSegment.from_mp3(fp)
    song.export(PATH_WAV, format="wav")


async def generate(content, voice):
    communicate = edge_tts.Communicate(content, voice)
    await communicate.save(PATH_MP3)


def speak(content, voice="zh-CN-YunxiNeural"):
    asyncio.run(generate(content, voice))
    mp32wav(PATH_MP3)
    wave_obj = sa.WaveObject.from_wave_file(PATH_WAV)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove(PATH_WAV)
    os.remove(PATH_MP3)
