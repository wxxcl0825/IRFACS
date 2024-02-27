import os
import asyncio
import edge_tts
from pydub import AudioSegment
import simpleaudio as sa
from utils import constant


def mp32wav(fp):
    song = AudioSegment.from_mp3(fp)
    song.export(constant.PATH_WAV, format="wav")


async def generate(content, voice):
    communicate = edge_tts.Communicate(content, voice)
    await communicate.save(constant.PATH_MP3)


def speak(content, voice="zh-CN-YunxiNeural"):
    asyncio.run(generate(content, voice))
    mp32wav(constant.PATH_MP3)
    wave_obj = sa.WaveObject.from_wave_file(constant.PATH_WAV)
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove(constant.PATH_WAV)
    os.remove(constant.PATH_MP3)
