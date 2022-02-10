import hikari
import lightbulb
import requests
from bs4 import BeautifulSoup

class Job:
    def __init__(self, title, company, location, salary, description):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.description = description

jobs = []

bot = lightbulb.BotApp(token = 'NzIzODQwMTI3MjE4MDkwMDE0.Xu3epg.ZrbfGgRWWUvAM5zRVu8GkvqxR-g', default_enabled_guilds=(822134565639815210))

response = requests.get('https://au.indeed.com/jobs?q=software+engineer&l=Perth+WA&radius=50&fromage=1')
soup = BeautifulSoup(response.content, 'html.parser')

divs = soup.find_all('div', class_= 'job_seen_beacon')

for item in divs:
    title = item.find('h2').find_next('span').find_next('span').text
    company = item.find('span', class_="companyName").text
    location = item.find('div', class_="companyLocation").text
    salaryDiv = item.find('div', class_='salary-snippet')
    desc = item.find('div', class_="job-snippet").li.text

    if salaryDiv is None:
        salary = ''
    elif salaryDiv is not None:
        salary = salaryDiv.span.text

    job = Job(title, company, location, salary, desc)
    jobs.append(job)

@bot.command
@lightbulb.command('hello', 'Says hello')
@lightbulb.implements(lightbulb.SlashCommand)
async def hello(ctx):
    await ctx.respond('Hello')

@bot.command
@lightbulb.command('cmd', 'Command group')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def commands(ctx):
    pass

@commands.child
@lightbulb.command('cmd1', 'First command')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def command1(ctx):
    await ctx.respond('G\'day matey!')

@bot.command
@lightbulb.option('number1', 'first number', type=int)
@lightbulb.option('number2', 'second number', type=int)
@lightbulb.command('add', 'do some math')
@lightbulb.implements(lightbulb.SlashCommand)
async def hello(ctx):
    await ctx.respond(ctx.options.number1 + ctx.options.number2)

@bot.command
@lightbulb.command("jobs", "Show most recently posted software jobs on Indeed")
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_command(ctx: lightbulb.Context) -> None:
    for i in jobs:
        embed = hikari.Embed(title=i.title, description="")
        embed.add_field(i.company, i.location)
        embed.add_field("Description", i.description)
        await ctx.respond(embed) 

bot.run()