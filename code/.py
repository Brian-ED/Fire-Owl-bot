import youtube_dl as ytdl
import discord

YTDL_OPTS = {
    "default_search": "ytsearch",
    "format": "bestaudio/best",
    "quiet": True,
    "extract_flat": "in_playlist"
}
class Video:
    """Class containing information about a particular video."""

    def __init__(self, url_or_search, requested_by):
        """Plays audio from (or searches for) a URL."""
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            video = self._get_info(url_or_search)
            video_format = video["formats"][0]
            self.stream_url = video_format["url"]
            self.video_url = video["webpage_url"]
            self.title = video["title"]
            self.uploader = video["uploader"] if "uploader" in video else ""
            self.thumbnail = video["thumbnail"] if "thumbnail" in video else None
            self.requested_by = requested_by

    def _get_info(self, video_url):
        with ytdl.YoutubeDL(YTDL_OPTS) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video = None
            if "_type" in info and info["_type"] == "playlist":
                return self._get_info(
                    info["entries"][0]["url"])  # get info for first video
            else:
                video = info
            return video

    def get_embed(self):
        """Makes an embed out of this Video's information."""
        embed = discord.Embed(
            title=self.title, description=self.uploader, url=self.video_url)
        embed.set_footer(
            text=f"Requested by {self.requested_by.name}",
            icon_url=self.requested_by.avatar_url)
        if self.thumbnail:
            embed.set_thumbnail(url=self.thumbnail)
        return embed
Video.get_embed


import discord
import asyncio
import youtube_dl
import logging
import math

FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
"""
Command line options to pass to `ffmpeg` before the `-i`.
See https://stackoverflow.com/questions/43218292/youtubedl-read-error-with-discord-py/44490434#44490434 for more information.
Also, https://ffmpeg.org/ffmpeg-protocols.html for command line option reference.
"""

async def play(self, ctx, *, url):
    """Plays audio hosted at <url> (or performs a search for <url> and plays the first result)."""

    client = ctx.guild.voice_client
    state = self.get_state(ctx.guild)  # get the guild's state

    if client and client.channel:
        try:
            video = Video(url, ctx.author)
        except youtube_dl.DownloadError as e:
            logging.warn(f"Error downloading video: {e}")
            await ctx.send(
                "There was an error downloading your video, sorry.")
            return
        state.playlist.append(video)
        message = await ctx.send(
            "Added to queue.", embed=video.get_embed())
        await self._add_reaction_controls(message)
    else:
        if ctx.author.voice is not None and ctx.author.voice.channel is not None:
            channel = ctx.author.voice.channel
            try:
                video = Video(url, ctx.author)
            except youtube_dl.DownloadError as e:
                await ctx.send(
                    "There was an error downloading your video, sorry.")
                return
            client = await channel.connect()
            self._play_song(client, state, video)
            message = await ctx.send("", embed=video.get_embed())
            await self._add_reaction_controls(message)
            logging.info(f"Now playing '{video.title}'")
        else:
            raise commands.CommandError(
                "You need to be in a voice channel to do that.")