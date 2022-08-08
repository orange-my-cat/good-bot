import wave
import wavelink
from discord.ext import commands

class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        self.node = await wavelink.NodePool.create_node(bot=self.bot,
                                            host='lava.link',
                                            port=80,
                                            password='',
                                            region='singapore')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'WAVELINK NODE <{node.identifier}> READY!')

    @commands.command(name='connect', aliases=['join'])
    async def connect_command(self, ctx: commands.Context):
        try:
            if ctx.voice_client:
                vc: wavelink.Player = await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        except AttributeError:
            return await ctx.send('Did you join a channel yet?')
        return vc

    @commands.command(name='disconnect', aliases=['leave'])
    async def disconnect_command(self, ctx: commands.Context):
        if ctx.voice_client:
            vc: wavelink.Player = await ctx.voice_client.disconnect()
        else:
            await ctx.send('Am I in a channel? Are you blind?')

    @commands.command(name='play')
    async def play_command(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        vc = await self.connect_command(ctx)
        await vc.play(search)

    @play_command.error
    async def play_command_error(self, ctx, exc):
        print(str(exc))

    @commands.command(name='stop')
    async def stop_command(self, ctx: commands.Context):
        try:
            vc = ctx.voice_client
            await vc.stop()
        except:
            await ctx.send('???')

def setup(bot):
  bot.add_cog(Music(bot))