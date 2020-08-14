import psutil
import discord
import discord.ext.commands as commands
import asyncio
import time

class Proc(commands.Cog):
	def __init__(self, bot, config, features_toggle, functions, timeouts, command_log):
		self.bot = bot
		self.config = config
		self.features_toggle = features_toggle
		self.functions = functions
		self.timeouts = timeouts
		self.command_log = command_log

	@commands.command()
	async def proc(self, ctx):
		if self.timeouts.is_timeout("proc"):
			await ctx.message.add_reaction(self.bot.emoji.hourglass)
			return
		else:
			self.timeouts.add("proc", self.config["timeout"])

		if not self.features_toggle["proc"]:
			await ctx.message.add_reaction(self.bot.emoji.no_bell)
			return

		try:
			self.functions.notification(self.config["notifications_format"], "Process list", ctx)
			await self.functions.warning_sound()
			self.command_log.append((time.time(), ctx, "Process list"))

			ramlist = list()
			cpulist = list()
			cpu_cores = psutil.cpu_count()
			cpu_total = psutil.cpu_percent() # returns 0.0

			for proc in psutil.process_iter(attrs=["name", "memory_full_info"]):
				try:
					name = proc.info["name"]
					cpu = proc.cpu_percent() # returns 0 on first call
					ram = round(proc.info["memory_full_info"].uss / 1024 / 1024, 1) # Mibibytes

					ramlist.append((ram, name))
				except:
					pass

			await asyncio.sleep(2)

			# call for cpu usage a second time to get an actual value
			for proc in psutil.process_iter(attrs=["name"]):
				try:
					name = proc.info["name"]
					cpu = round(proc.cpu_percent() / cpu_cores, 1)
					cpulist.append((cpu, name))
				except:
					pass

			ramlist.sort()
			cpulist.sort()
			ramlist.reverse()
			cpulist.reverse()

			ramlist = ramlist[:10]
			cpulist = cpulist[:10]

			cpu_total = psutil.cpu_percent() # returns an actual value
			memory = psutil.virtual_memory()

			message = "**RAM** (" + str(round(memory.used / 1024 / 1024, 1))  + " MiB / " + str(round(memory.total / 1024 / 1024, 1)) + " MiB):\n```"
			for item in ramlist:
				message += str(item[0]) + " MiB | " + item[1] + "\n"

			message += "```\n**CPU** (" + str(round(cpu_total, 1)) + "%):\n```"
			for item in cpulist:
				message += str(item[0]) + "% | " + item[1] + "\n"

			message += "```"

			await ctx.send(message)

		except Exception as exc:
			await ctx.message.add_reaction(self.bot.emoji.cross_mark)
			await ctx.send("Error! " + str(type(exc)) + " " + str(exc))
