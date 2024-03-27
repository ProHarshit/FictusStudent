import discord
import gspread
import google.generativeai as genai
from discord import app_commands
from discord.ext import commands, tasks
import discord.ui
from variables import var, vararray, ans
from arrays import paper
from keep_alive1 import keep_alive
from pathlib import Path
import time
import asyncio
import streamlit as st

key = st.secrets["key"]
genai.configure(api_key=key)
channel_id = 1215575801966108698
model = genai.GenerativeModel(model_name="gemini-pro")
list = str(var)
taskarray = vararray
anskey = str(ans)
file_path = Path("variables.py")
gc = gspread.service_account(filename='serviceAuth.json')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = st.secrets["TOKEN"]
paper = paper
answers = []
state = False

safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

def count(string1, string2):
  common_count = sum(char1 == char2 for char1, char2 in zip(string1, string2))
  return common_count
    
class Menu(discord.ui.View):
  @discord.ui.button(label="A",style=discord.ButtonStyle.primary)
  async def buttona(self,interaction: discord.Interaction,button:discord.ui.Button):
    global answers
    global state
    answers.append("a")
    await interaction.response.send_message("You Clicked **A**",ephemeral=True)
    await asyncio.sleep(2)
    await interaction.delete_original_response() 
    state = True
  @discord.ui.button(label="B",style=discord.ButtonStyle.primary)
  async def buttonb(self,interaction: discord.Interaction,button:discord.ui.Button):
    global answers
    global state
    answers.append("b")
    await interaction.response.send_message("You Clicked **B**",ephemeral=True)
    await asyncio.sleep(2)
    await interaction.delete_original_response() 
    state = True
  @discord.ui.button(label="C",style=discord.ButtonStyle.primary)
  async def buttonc(self,interaction: discord.Interaction,button:discord.ui.Button):
    global answers
    global state
    answers.append("c")
    await interaction.response.send_message("You Clicked **C**",ephemeral=True)
    await asyncio.sleep(2)
    await interaction.delete_original_response()
    state = True
  @discord.ui.button(label="D",style=discord.ButtonStyle.primary)
  async def buttond(self,interaction: discord.Interaction,button:discord.ui.Button):
    global answers
    global state
    answers.append("d")
    await interaction.response.send_message("You Clicked **D**",ephemeral=True)
    await asyncio.sleep(2)
    await interaction.delete_original_response() 
    state = True

@bot.event
async def on_ready():
  print("Bot is Up and Ready!")
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)
  check.start()

@tasks.loop(minutes=120)
async def check():
  t = time.localtime()
  current_hour = time.strftime("%H", t)
  if (current_hour=="12") or (current_hour=="13"):
    channel = bot.get_channel(channel_id)
    if channel:
      array = ["B1", "B2", "B3", "B4", "B5", "B6" ,"B7","B8"]
      for x in array:
        for task in taskarray:
          wks = gc.open(task).sheet1
          progress = str(wks.get(x))
          val = progress[3:-3]
          if x == "B1" and val != "Complete":
            await channel.send(f"**Harshit has not completed task {task}**")
          if x == "B2" and val != "Complete":
            await channel.send(f"**Shivansh has not completed task {task}**")
          if x == "B3" and val != "Complete":
            await channel.send(f"**Tushar has not completed task {task}**")
          if x == "B4" and val != "Complete":
            await channel.send(f"**Kalp has not completed task {task}**")
          if x == "B5" and val != "Complete":
            await channel.send(f"**Arpit has not completed task {task}**")
          if x == "B6" and val != "Complete":
            await channel.send(f"**Avneet has not completed task {task}**")
          if x == "B7" and val != "Complete":
            await channel.send(f"**Sasmit has not completed task {task}**")
          if x == "B8" and val != "Complete":
            await channel.send(f"**Vatsal has not completed task {task}**")
    else:
      print("Channel not found.")

@bot.tree.command(name="hello",description="Say hello to the bot")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name="say",description="Tell the bot to say something")
@app_commands.describe(thing_to_say="What should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
  await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`",ephemeral=True)

@bot.tree.command(name="task",description="Create, list or delete tasks")
@app_commands.describe(option="Create,list or delete")
@app_commands.describe(name="Name of task to create or delete")
async def say(interaction: discord.Interaction, option: str, name: str=None):
  global list
  global taskarray
  if option == "list":
    await interaction.response.send_message(f"Name of tasks are : {list}")
  if option == "delete":
    await interaction.response.defer()
    if name in list:
      wks = gc.create(name)
      list = list.replace(name, "")
      taskarray.remove(name)
      file_path.unlink()
      with open("variables.py", mode="w") as file:
        file.write(f"""var = \"\"\"{list}\"\"\"""")
        file.write(f"""\nvararray = {taskarray}""")
        file.write(f"""\nans = {anskey}""")
      await interaction.followup.send(f"**{name}** has been deleted")
    else:
      await interaction.followup.send(f"Task **{name}** not found")
  if option == "create":
    await interaction.response.defer()
    if name in list:
      await interaction.followup.send(f"**{name} **task has already been created")
    else:
      wks = gc.create(name)
      list = list + "\n" + name
      taskarray.append(name)
      file_path.unlink()
      with open("variables.py", mode="w") as file:
        file.write(f"""var = \"\"\"{list}\"\"\"""")
        file.write(f"""\nvararray = {taskarray}""")
        file.write(f"""\nans = {anskey}""")
      await interaction.followup.send(f"**{name} **task has been created")
  else:
    await interaction.response.send_message("**Invalid option**")

@bot.tree.command(name="update", description="Update Progress")
@app_commands.describe(task="Name of task")
@app_commands.describe(label="Complete, Pending etc.")
async def say(interaction: discord.Interaction, task: str, label: str):
  await interaction.response.defer()
  if task in list:
    wks = gc.open(f"{task}").sheet1
    if (interaction.user.name) == "proharshit.":
      wks.update([['Harshit', label]], 'A1')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
    if (interaction.user.name) == "ignoreme_sg":
      wks.update([['Shivansh', label]], 'A2')
      await interaction.followup.send(f"**{task} **has been updated to state **{label}**")
    if (interaction.user.name) == "tapster1510":
      wks.update([['Tushar', label]], 'A3')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
    if (interaction.user.name) == "helldevil69":
      wks.update([['Kalp', label]], 'A4')
      await interaction.followup.send(f"**{task} **has been updated to state **{label}**")
    if (interaction.user.name) == "":
      wks.update([['Arpit', label]], 'A5')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
    if (interaction.user.name) == "beluga3703":
      wks.update([['Avneet', label]], 'A6')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
    if (interaction.user.name) == "sasmit0509":
      wks.update([['Sasmit', label]], 'A7')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
    if (interaction.user.name) == "vatsaldgoyal":
      wks.update([['Vatsal', label]], 'A8')
      await interaction.followup.send(f"**{task}** has been updated to state **{label}**")
  else:
    await interaction.followup.send("Task not found")

@bot.tree.command(name="progress",description="Check Progress")
@app_commands.describe(task="Name of task")
@app_commands.describe(user="Name of user to check")
async def say(interaction: discord.Interaction, task: str, user: str):
  await interaction.response.defer()
  if task in list:
    wks = gc.open(task).sheet1
    if user == "Harshit":
      progress = str(wks.get('B1'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Shivansh":
      progress = str(wks.get('B2'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Tushar":
      progress = str(wks.get('B3'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Kalp":
      progress = str(wks.get('B4'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Arpit":
      progress = str(wks.get('B5'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Avneet":
      progress = str(wks.get('B6'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Sasmit":
      progress = str(wks.get('B7'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
    if user == "Vatsal":
      progress = str(wks.get('B8'))
      val = progress[3:-3]
      await interaction.followup.send(f"**{user} has completed task till state {val}**")
  else:
    await interaction.followup.send("**Task not found**")

@bot.tree.command(name="chat",description="Ask the bot")
@app_commands.describe(ques="Question which you want to ask")
async def say(interaction: discord.Interaction, ques: str):
  await interaction.response.defer()
  response = model.generate_content(f"Answer the question {ques}",safety_settings=safety_settings)
  if response.parts:
    await interaction.followup.send(f"Question is {ques} /nAnswer is:/n") 
    for part in response.parts:
      await interaction.followup.send(part.text)
  else:
    await interaction.followup.send(f"Question is {ques} \nAnswer is \n : " + response.text)

@bot.tree.command(name="key",description="Set the answer key")
@app_commands.describe(key="Type the answer key")
async def say(interaction: discord.Interaction, key :str):
  await interaction.response.defer()
  member = interaction.guild.get_member(interaction.user.id)
  if any(role.name != "Administrator" for role in member.roles):
    await interaction.followup.send("You don't have the permission to use this command.")
  else:
    global anskey
    key1 = key.replace(" ","")
    anskey = key1.lower()
    file_path.unlink()
    with open("variables.py", mode="w") as file:
      file.write(f"""var = \"\"\"{list}\"\"\"""")
      file.write(f"""\nvararray = {taskarray}""")
      file.write(f"""\nans = \"\"\"{anskey}\"\"\"""")
    await interaction.followup.send("**Answer key has been set**")

@bot.tree.command(name="smts",description="Attend the test")
async def say(interaction: discord.Interaction):
  await interaction.response.defer(ephemeral=True)
  global answers
  global state
  wks1 = gc.open("smts").sheet1
  answers = []
  view=Menu()
  usr = str(interaction.user.name)
  await interaction.edit_original_response(content = "**Welcome to SMTS**")
  await asyncio.sleep(5)
  if usr == "proharshit." and str(wks1.get('B1')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "ignoreme_sg" and str(wks1.get('B2')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "tapster1510" and str(wks1.get('B3')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "helldevil69" and str(wks1.get('B4')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "nemesis_killedrse3" and str(wks1.get('B5')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "beluga3703" and str(wks1.get('B6')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "sasmit0509" and str(wks1.get('B7')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
    return
  if usr == "vatsaldgoyal" and str(wks1.get('B8')) != "[[]]":
    await interaction.edit_original_response(content="**You have already submitted the test **")
  await interaction.edit_original_response(content="**The Paper consists of Buttons use them**") 
  await asyncio.sleep(5) 
  paper.append("")
  await interaction.edit_original_response(content=(f"{paper[0]}"),view=view)
  for ques in paper:
    if ques==paper[0]:
      continue
    while state is False:
      await asyncio.sleep(1)
      if state is True:
        await interaction.edit_original_response(content=(f"{ques}"),view=view)
        state = False
        break
  await interaction.edit_original_response(content=("**Submitted Test succesfully**"),view=None)
  await asyncio.sleep(5)
  await interaction.delete_original_response()
  channel = bot.get_channel(channel_id)
  if (interaction.user.name) == "proharshit.":
    wks1.update([['Harshit', str(answers)]], 'A1')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "ignoreme_sg":
    wks1.update([['Shivansh', str(answers)]], 'A2')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "tapster1510":
    wks1.update([['Tushar', str(answers)]], 'A3')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "helldevil69":
    wks1.update([['Kalp', str(answers)]], 'A4')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "nemesis_killedrse3":
    wks1.update([['Arpit', str(answers)]], 'A5')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "beluga3703":
    wks1.update([['Avneet', str(answers)]], 'A6')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "sasmit0509":
    wks1.update([['Sasmit', str(answers)]], 'A7')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  if (interaction.user.name) == "vatsaldgoyal":
    wks1.update([['Vatsal', str(answers)]], 'A8')
    await channel.send(f"**{interaction.user.mention } has submitted the test**")
  

@bot.tree.command(name="evaluate",description="Evaluate the marks")
async def say(interaction: discord.Interaction):
  await interaction.response.defer()
  member = interaction.guild.get_member(interaction.user.id)
  if any(role.name != "Administrator" for role in member.roles):
    await interaction.followup.send("You don't have the permission to use this command.")
  else:
    wks2 = gc.open("smts").sheet1
    cell = ["B1","B2","B3","B4","B5","B6","B7","B8"]
    cells1 = ["C1","C2","C3","C4","C5","C6","C7","C8"]
    names = ["Harshit","Shivansh","Tushar","Kalp","Arpit","Avneet","Sasmit","Vatsal"]
    await interaction.followup.send("Here are the results")
    for n in range(8):
      x = cell[n]
      cell1 = cells1[n]
      value = str(wks2.get(x)) 
      val2 = value[3:-3]
      val3 = val2.lower()
      val1 = val3.replace(" ","")
      scores = count(val1,anskey)
      wks2.update([[scores,'']], cell1)
      name = names[n]
      value1 = str(wks2.get(cell1))
      await interaction.followup.send(f"**{name} has scored {value1[3:-3]} out of {len(anskey)}**")


keep_alive()
bot.run(TOKEN)