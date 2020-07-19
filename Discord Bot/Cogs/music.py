import discord
import os
import json
import random
import asyncio
import youtube_dl
import shutil
from discord.ext import commands
from discord.utils import get

class musiccogs(commands.Cog):
    def __init__(self,client):
        self.client = client
    ##Music player

    #Join server
    @commands.command(pass_context=True)
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f'Joined {channel}')

    #Leave server
    @commands.command(pass_context=True)
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f'Left {channel}')

    #Play command
    @commands.command(pass_context=True, aliases=['p', 'pl', 'pla'])
    async def play(self, ctx, url: str):

        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR =  os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("Queue is empty\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Playing next song\n")
                    print(f'Songs still in queue: {still_q}')
                    song_there = os.path.isfile('song.mp3')
                    if song_there:
                        os.remove('song.mp3')
                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith('.mp3'):
                            os.rename(file, 'song.mp3')
                    
                    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.07

                else:
                    queues.clear()
                    return
            
            else:
                queues.clear()
                print('No song queued\n')
        
        song_there = os.path.isfile('song.mp3')
        try:
            if song_there:
                os.remove('song.mp3')
                queues.clear()
                print('Removed old song file')
        except PermissionError:
            print("Trying to delete old song file, but it's being played")
            await ctx.send("Error: Music playing")
            return

        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old queue folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder")
        
        await ctx.send("getting everything ready now")

        voice = get(client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
        
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[0]}")
        print("Playing\n")

    #Pause music
    @commands.command(pass_context=True, aliases=['pa', 'pau'])
    async def pause(self, ctx):

        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Music paused")
            voice.pause()
            await ctx.send("Music paused")
        else:
            print("Music is not playing, cant pause dumbass")
            await ctx.send("Cant pause nothing fool")

    #Resume music
    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):

        voice = get(client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("resusmed music")
            voice.resume()
            await ctx.send("Resumed music")
        else:
            print("Music isnt paused")
            await ctx.send("Shit still playin")

    #Skip Music
    @commands.command(pass_context=True, aliases=['s', 'ski'])
    async def skip(self, ctx):
        voice = get(client.voice_clients, guild=ctx.guild)

        queues.clear()

        if voice and voice.is_playing():
            print("Music skipped")
            voice.stop()
            await ctx.send("Skipped")
        else:
            print("Nothing to skip")
            await ctx.send("Skip yourself, motherfucker")

    queues = {}

    #Queue
    @commands.command(pass_context=True, aliases=['q', 'que'])
    async def queue(self, ctx, url: str):
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR =  os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num

        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'outtmpl': queue_path,
            'postprocessor': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now \n")
            ydl.downlaod([url])
        await ctx.send(f"Adding song {str(q_num)} to the queue")

        print("Song added to queue\n")


def setup(client):
    client.add_cog(musiccogs(client))