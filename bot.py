from re import match
from socket import timeout
from pyrogram.types import CallbackQuery,ReplyKeyboardMarkup,KeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from core import bot2 as bot, bot as app
from pyrogram.errors import UserNotParticipant,ChatAdminRequired
import requests
import random
import json
from main import *
from taskdb import *


from auth import lookupFollowing,api,extend

from pyrogram import filters,idle
withdrawchat= -1001543117486
import json
  
buttons=[[
      KeyboardButton("💰 Balance")
      
],
         
[KeyboardButton("🔗 Referral Link")],
[KeyboardButton("🚥 Withdraw Mcr")],
[KeyboardButton("💼 View Wallet Address")],
[KeyboardButton("🌐 Metacar Token")]
         
]  

f = open('tasks.json',)
  
data = json.load(f)

task = data
decrease=task.get("decrease")

try:
  
#  chets=os.environ.get("FORCESUB_CHATS_OR_CHANNEL").split(",")
 chets=['MetacarTokenChannel','MetacarToken']
except (KeyError,AttributeError):
    

  chets=[] 
chats=[]
for i in chets:
   if i:
      if i.startswith("-"):
            a=i.replace("-",'')
            if a.isnumeric():
                  chats.append(int("-" + a))
      else:
            chats.append(i)


try:
  
 admeme = os.environ.get("ADMINS").split(",")
except (KeyError,AttributeError):
  admeme=[]
ADMINS=[]
for i in admeme:
    if i: 
      if i.isnumeric():
                  ADMINS.append(int(i))
      else:
            ADMINS.append(i)



@app.on_message(filters.command(['start', "balance", "referal" ,"wallet"]) & filters.group  & ~filters.forwarded)
async def on(c,message):
      if not message.from_user.username:
              chat=message.from_user.id
      else:
          chat=message.from_user.username   
      user=(await app.get_users(message.from_user.id)).mention(style='md')
      if message.command[0] == "balance":
            blance=(await balance(chat))[-1]
            await app.send_message(message.chat.id, "{} You balance is : {}".format(user, blance))
      elif message.command[0] == "referal":
            await app.send_message(message.chat.id ,"Referal link of {} is:\n{}".format(user, "https://t.me/{}?start={}".format((await app.get_me()).username, message.from_user.id)))
      
      elif message.command[0] == "wallet":
            wall=(await wallet(chat))[-1]
            await app.send_message(message.chat.id ,f"{user} You Wallet address saved is:\n{wall}")
      else:
            await message.reply("This command is only made for me in PM")       
import concurrent.futures

@app.on_message(filters.command(['start']) & filters.private  & ~filters.forwarded)
async def on(c,message):
    if not message.from_user.username:
          name=message.from_user.id
    else:
          name=message.from_user.username
    print(name)
    try:
      r1=random.randint(50,100)
      r2=random.randint(50,100)
      try:
         refered=message.text.split()[1]

         r=refered
         refered= (await app.get_users(int(refered))).username
         if not refered:
                refered=r 
      except:
         refered=None
      chat=message.chat.id
      async with bot.conversation(message.chat.id) as conv:
          await conv.send_message(f"**Hello {message.from_user.first_name}, Please first prove me that you are a human by solving this simple math task **\n\n**what is: ** `{r1} + {r2}`=")
          answer=(await conv.get_response()).raw_text
          while not any(x.isnumeric() for x in answer):
               await conv.send_message("Please enter a numeric value")
               answer = (await conv.get_response()).raw_text
          a=r1 + r2
          answer=int(answer)
          while not answer == a:
         
           await conv.send_message("Incorrect answer.")
           answer=int((await conv.get_response()).raw_text)
           if answer == a:
               break
           else:
             continue  
          await app.send_message(message.chat.id,f"""Hello, {message.from_user.first_name}! 
✅Please complete all the tasks and submit details correctly to be eligible for the airdrop

🔸 For Completing the tasks - Get 200000000 MCR
👫 For Each Valid Refer - Get 200000000 MCR

📘 By Participating you are agreeing to the Metacar (Airdrop) Program Terms and Conditions.

Click "Continue" to proceed

""",
reply_markup=InlineKeyboardMarkup([[
    InlineKeyboardButton("Continue", callback_data="chat_{}_{}".format(name,refered))
    
]]))

    except concurrent.futures.TimeoutError:
          await message.reply("You took to long to respond try again!")
          
          
@app.on_callback_query(filters.regex(pattern="chat_(.*)_(.*)"))
async def detailed(client, message: CallbackQuery):    
        user=message.matches[0].group(1)
        ref=message.matches[0].group(2)
        l,p=(0,0)
        if user.isnumeric():
              chat=int(user)
        else:
              chat=user
        notpart=''
        channels=''
        for  i in chats:
              notpart+=f'🔹 [{(await app.get_chat(i)).title}](t.me/{i})' + "\n"
              
        a= "【1/3】Complete the tasks below:\n\n**Join our telegram group and channel**\n\n**" + notpart + "\n\n" + 'Click "✅ Done" to verify whether you completed these tasks or not.'
        await app.send_message(chat,a,disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done",callback_data="joined_{}_{}".format(chat,ref))]]))

async def createExcel():
    data=await dataframes()
    print(data)
    import pandas as pd
    df=pd.DataFrame(data)
    writer = pd.ExcelWriter('data.xlsx')
    df.to_excel(writer, sheet_name='Clients', index=False)


    extend(df,writer.sheets['Clients'])  
    new_filename="data.xlsx"
#     writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
#     if os.path.exists(new_filename):
#      writer.book = load_workbook(new_filename)
#     else:
#      writer.book = Workbook()
#     writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
#     reader = pd.read_excel(r'data.xlsx')
#     df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)
    writer.save()

    writer.close()
    return 'data.xlsx'
        

@app.on_message(filters.private)
async def k(c,message):
      if not message.from_user.username:
            chat=message.from_user.id
      else:
            chat=message.from_user.username
      print(chat)
      user=(await app.get_users(message.from_user.id)).mention(style='md')
      if message.text == "💰 Balance":
            b=await balance(chat)
            if not b:
              blance=400000000
            else:
              blance=b[-1]
            await app.send_message(message.from_user.id, "{} Your balance is : {}".format(user, blance))
      elif message.text == "🚥 Withdraw Mcr":
            blnce=0
            wallet_=0
            refers=0
            try:
                            blnce=(await balance(chat))[-1]
                            wallet_=(await wallet(chat))[-1]
                            refers=await getRefers(chat)
            except IndexError:
                           pass
            ids=[]
            async with bot.conversation(chat, timeout=300) as conv:
                msg6=await conv.send_message("**Compleate Secondary Task And Withdraw your mcr instantly** \n\n**FOLLOW YouTube:** \n\n**Link:** https://youtube.com/channel/UCt-kuAl66NJBgjuAKXM3DDg \n\n**subscribe to YouTube channel** \n\n**Enter your YouTube Id.**  ", link_preview =False )
                ids.append(msg6.id)
                youtube=(await conv.get_response()).raw_text
            async with bot.conversation(chat, timeout=300) as conv:
                  if await request_created(chat):
                        return await app.send_message(chat,"You already have created a request, Your request is pending , Please be patient and wait for the approval!!! , after you can withdraw again")
                  if not int(blnce) >= 400000000 :
                    return await app.send_message(chat,"You dont have sufficient balance to withdraw your mcr , need 400000000 mcr to withdraw , refer your one friend any withdraw your mcr instantly ")
                  await conv.send_message("**Are you sure you want to send withdraw request?**\n\n**TYPE** `yes` to procced\n**TYPE** `no` to go back")
                  ans=(await conv.get_response()).raw_text
                  ans=ans.lower()
                  while ans not in ['yes' , 'no']:
                      await conv.send_message("Please send response in amount `yes` or `no` format")

                      ans=(await conv.get_response()).raw_text
                      ans=ans.lower()
                      if ans in ['yes', 'no']:
                            break
                      else:
                            continue
                  if ans == "yes" :
                  	         watll=(await wallet(chat))[-1]
                  	         await app.send_message(chat,"**Your withdrawal is processing ...... will arive within 2 minutes** ")
                  	         r = requests.post('https://autopayment.up.railway.app/sendtoken', json ={'recipient': f'{watll}','token': '0xEbE790D96D02C3144C667643CD2Dce69d1EFc00B','amount': '400000000','private_key':'6597f19b4f3523afa7b5d361bc3d5105dcb6857d77dfc7c473ed41965a3b0c7b'})
                  	         print(r.json())
                  	         employee_dict = json.loads(r.text)
                  	         txid = employee_dict['transactionHash']
                  	         await app.send_message(chat,f"**Your withdrawal Proccessed successfully to your wallet =>** {watll} \n**Amount => 400000000** \n**TXID of Transfer =>** https://tomoscan.io/tx/{txid}")
                  	         await decrease_money(chat,400000000)
      elif message.text == "🔗 Referral Link":
            ref=await getRefers(chat)
            await app.send_message(message.from_user.id ,"For Each Valid Refer Get 200000000 MCR\n\nReferal link of {} is:\n{}\n\nTotal refers: {}".format(user, "https://t.me/{}?start={}".format((await app.get_me()).username, message.from_user.id),ref))
            
      elif message.text == "💼 View Wallet Address":
            wall=(await wallet(chat))[-1]
            await app.send_message(message.from_user.id ,f"{user} You Wallet address saved is:\n{wall}")
      elif message.text == "🌐 Metacar Token":
            await app.send_message(message.from_user.id ,f"🌐 [Website](https://metacartoken.com/) ")

      elif message.text == "Excel5505":
          await message.reply("Creating excel data of users ,Please wait!")
          c=await createExcel()
          await app.send_document(message.chat.id , c, caption="Data of our users")
          await message.delete()


 
@app.on_callback_query(filters.regex(pattern="deny_(.*)"))

async def detailed(client, message: CallbackQuery): 
       user: str=message.matches[0].group(1)
       await message.message.delete()
       await app.send_message(user if not user.isnumeric() else int(user) ," Your request has been not processed ,may be you entered wallet address invalid or any else  Please try to request withdraw Again!!!\n\n__Note__ : `Tokens are refunded` make again Mcr withdraw request ")
       await increase_money(user,400000000)
       await requestmade(False,user)




@app.on_callback_query(filters.regex(pattern="paid_(.*)"))
async def nothing(c,message):
       user: str=message.matches[0].group(1)
       await message.message.delete()
       user=user if not user.isnumeric() else int(user)

       await app.send_message(user,"**Congratulations! your transfer has processed** , Successfully transferred MCR In your wallet . It's been confirmed on the blockchain , Check Your wallet . Refer and earn more mcr before ending a airdrop ")


@app.on_callback_query(filters.regex(pattern="pay_(.*)"))

async def detailed(client, message: CallbackQuery):    
  user: str=message.matches[0].group(1)
  await message.message.delete()
  await requestmade(False,user)
  user=user if not user.isnumeric() else int(user)
  
  await app.send_message(withdrawchat,"അയച്ചു കൊടുത്തങ്കിൽ Paid Button നെക്ക് മലരേ ......",
reply_markup=InlineKeyboardMarkup(
      [

            [InlineKeyboardButton("Paid",f'paid_{user}')],
      ]
)

  )

@app.on_callback_query(filters.regex(pattern="joined_(.*)_(.*)"))

async def detailed(client, message: CallbackQuery):    
  user=message.matches[0].group(1)
  ref=message.matches[0].group(2)
  if   ref == "None":
      ref=None
  chat: str=user 
  if  user.isnumeric():
        user=int(user)
  try:
  
      l=0
      for i in chats:
       try:
         
         await app.get_chat_member(i, user)
       except UserNotParticipant:
       
        l+=1
       except ChatAdminRequired:
         pass
      if l>0:
             
        await message.answer("Please joining each and every channel!",show_alert=True)
      else:
             await message.message.delete()
             ids=[]
             async with bot.conversation(user, timeout=300) as conv:
                 msg=await conv.send_message("【2/3】Complete the tasks below :\n\n" + data['1'].format(emoji='🔹'), link_preview =False)
                 ids.append(msg.id)
                 username=(await conv.get_response()).raw_text
                 username = username.split("/")[-1]
                 while not lookupFollowing(username):
                     
                   msg2=await conv.send_message("Please follow our twitter and retweet our post , Yet you are not following")
                   ids.append(msg2.id)
                   username=(await conv.get_response()).raw_text
                   username = username.split("/")[-1]
                   if lookupFollowing(username):
                         break
                   else:
                         continue
                 await conv.send_message(data[
                       '3'
                 ])
                 tweetLink = (await conv.get_response()).raw_text
             async with  bot.conversation(user, timeout=300) as conv:
                 msg3=await conv.send_message("【3/3】Complete the tasks below:\n\n" + data['2'].format(emoji="🔹"), link_preview =False)
                 wallet=(await conv.get_response()).raw_text
                 while not len(wallet) == 42:
                       msg4=await conv.send_message("Please send a valid wallet address")
                       ids.append(msg4.id)
                       
                       wallet=(await conv.get_response()).raw_text
                       if len(wallet) == 42:
                             break
                           
                       else:
                             continue
                 w=await wallets()
                 while wallet in w:
                       msg5=await conv.send_message("This wallet is already in use")
                       ids.append(msg5.id)
                       wallet=(await conv.get_response()).raw_text
                       if not wallet in w:
                             break
                           
                       else:
                             continue
            
             await taskUpdate(user,username,wallet, tweetLink)
             await app.delete_messages(message.from_user.id, ids)



             await app.send_message(user,"Thanks for joining our bot:\nChoose one of the following options",reply_markup=ReplyKeyboardMarkup(buttons))
              
             if  ref.isnumeric():
                ref = int(ref)
             
             if ref:
                 
                  if ref != user:
                           if not check_user_already_referd(ref,user):
    
                               await update_user_points(ref)
                               update_user_refers(ref,user)
                               try:
                                  

                                await increase_money(ref ,data['amount increase'])
                               except TypeError:
                                  await app.send_message(ref,"Please register yourself before refering someone")
  except concurrent.futures.TimeoutError:
        await app.send_message(user, "You took to long to respond try again!")        

app.start()

idle()
from re import match
from pyrogram.types import CallbackQuery,ReplyKeyboardMarkup,KeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_button import InlineKeyboardButton
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import InlineKeyboardMarkup
from core import bot2 as bot, bot as app
from pyrogram.errors import UserNotParticipant,ChatAdminRequired

import random
from main import *
from taskdb import *


from auth import lookupFollowing,api,extend

from pyrogram import filters,idle
withdrawchat= -618086967
import json
  
buttons=[[
      KeyboardButton("💰 Balance")
      
],
         
[KeyboardButton("🔗 Referral Link")],
[KeyboardButton("💼 View Wallet Address")],
[KeyboardButton("🌐 Jaskom Website")],
[KeyboardButton("🚦 Transfer Nft")]
         
]  

f = open('tasks.json',)
  
data = json.load(f)

task = data
decrease=task.get("decrease")

try:
  
#  chets=os.environ.get("FORCESUB_CHATS_OR_CHANNEL").split(",")
 chets=['MetacarTokenChannel','MetacarToken']
except (KeyError,AttributeError):
    

  chets=[] 
chats=[]
for i in chets:
   if i:
      if i.startswith("-"):
            a=i.replace("-",'')
            if a.isnumeric():
                  chats.append(int("-" + a))
      else:
            chats.append(i)


try:
  
 admeme = os.environ.get("ADMINS").split(",")
except (KeyError,AttributeError):
  admeme=[]
ADMINS=[]
for i in admeme:
    if i: 
      if i.isnumeric():
                  ADMINS.append(int(i))
      else:
            ADMINS.append(i)



@app.on_message(filters.command(['start', "balance", "referal" ,"wallet"]) & filters.group  & ~filters.forwarded)
async def on(c,message):
      if not message.from_user.username:
              chat=message.from_user.id
      else:
          chat=message.from_user.username   
      user=(await app.get_users(message.from_user.id)).mention(style='md')
      if message.command[0] == "balance":
            blance=(await balance(chat))[-1]
            await app.send_message(message.chat.id, "{} You balance is : {}".format(user, blance))
      elif message.command[0] == "referal":
            await app.send_message(message.chat.id ,"Referal link of {} is:\n{}".format(user, "https://t.me/{}?start={}".format((await app.get_me()).username, message.from_user.id)))
      
      elif message.command[0] == "wallet":
            wall=(await wallet(chat))[-1]
            await app.send_message(message.chat.id ,f"{user} You Wallet address saved is:\n{wall}")
      else:
            await message.reply("This command is only made for me in PM")       
import concurrent.futures

@app.on_message(filters.command(['start']) & filters.private  & ~filters.forwarded)
async def on(c,message):
    if not message.from_user.username:
          name=message.from_user.id
    else:
          name=message.from_user.username
    print(name)
    try:
      r1=random.randint(50,100)
      r2=random.randint(50,100)
      try:
         refered=message.text.split()[1]

         r=refered
         refered= (await app.get_users(int(refered))).username
         if not refered:
                refered=r 
      except:
         refered=None
      chat=message.chat.id
      async with bot.conversation(message.chat.id) as conv:
          await conv.send_message(f"**Hello {message.from_user.first_name}, Please first prove me that you are a human by solving this simple math task **\n\n**what is: ** `{r1} + {r2}`=")
          answer=(await conv.get_response()).raw_text
          while not any(x.isnumeric() for x in answer):
               await conv.send_message("Please enter a numeric value")
               answer = (await conv.get_response()).raw_text
          a=r1 + r2
          answer=int(answer)
          while not answer == a:
         
           await conv.send_message("Incorrect answer.")
           answer=int((await conv.get_response()).raw_text)
           if answer == a:
               break
           else:
             continue  
          await app.send_message(message.chat.id,f"""Hello, {message.from_user.first_name}! 
✅Please complete all the tasks and submit details correctly to be eligible for the airdrop

🔸 For Completing the tasks - Get 20 point 
👫 For Each Valid Refer - Get 15 point
🔸 Tranfer your nft - 100 point

📘 By Participating you are agreeing to the Jaskom (Nft Airdrop) Program Terms and Conditions.

Click "Continue" to proceed

""",
reply_markup=InlineKeyboardMarkup([[
    InlineKeyboardButton("Continue", callback_data="chat_{}_{}".format(name,refered))
    
]]))

    except concurrent.futures.TimeoutError:
          await message.reply("You took to long to respond try again!")
          
          
@app.on_callback_query(filters.regex(pattern="chat_(.*)_(.*)"))
async def detailed(client, message: CallbackQuery):    
        user=message.matches[0].group(1)
        ref=message.matches[0].group(2)
        l,p=(0,0)
        if user.isnumeric():
              chat=int(user)
        else:
              chat=user
        notpart=''
        channels=''
        for  i in chats:
              notpart+=f'🔹 [{(await app.get_chat(i)).title}](t.me/{i})' + "\n"
              
        a= "【1/3】Complete the tasks below:\n\n**Join our telegram group and channel**\n\n**" + notpart + "\n\n" + 'Click "✅ Done" to verify whether you completed these tasks or not.'
        await app.send_message(chat,a,disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done",callback_data="joined_{}_{}".format(chat,ref))]]))

async def createExcel():
    data=await dataframes()
    print(data)
    import pandas as pd
    df=pd.DataFrame(data)
    writer = pd.ExcelWriter('data.xlsx')
    df.to_excel(writer, sheet_name='Clients', index=False)


    extend(df,writer.sheets['Clients'])  
    new_filename="data.xlsx"
#     writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
#     if os.path.exists(new_filename):
#      writer.book = load_workbook(new_filename)
#     else:
#      writer.book = Workbook()
#     writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)
#     reader = pd.read_excel(r'data.xlsx')
#     df.to_excel(writer,index=False,header=False,startrow=len(reader)+1)
    writer.save()

    writer.close()
    return 'data.xlsx'
        

@app.on_message(filters.private)
async def k(c,message):
      if not message.from_user.username:
            chat=message.from_user.id
      else:
            chat=message.from_user.username
      print(chat)
      user=(await app.get_users(message.from_user.id)).mention(style='md')
      if message.text == "💰 Balance":
            b=await balance(chat)
            if not b:
              blance=100
            else:
              blance=b[-1]
            await app.send_message(message.from_user.id, "{} Your balance is : {}".format(user, blance))
      elif message.text == "Withdraw":
            blnce=0
            wallet_=0
            refers=0
            try:
                            blnce=(await balance(chat))[-1]
                            wallet_=(await wallet(chat))[-1]
                            refers=await getRefers(chat)
            except IndexError:
                           pass
            async with bot.conversation(chat) as conv:
                  if await request_created(chat):
                        return await app.send_message(chat,"You already have created a request,Please be patient and wait for the approval!!!")
                  if not int(blnce) >= 100 :
                    return await app.send_message(chat,"You dont have sufficient balance to withdraw")
                  await conv.send_message("**Are you sure you want to send withdraw request?**\n\n**TYPE** `yes` to procced\n**TYPE** `no` to go back")
                  ans=(await conv.get_response()).raw_text
                  ans=ans.lower()
                  while ans not in ["yes", 'no']:
                      await conv.send_message("Please send response in `yes` or `no` format")

                      ans=(await conv.get_response()).raw_text
                      ans=ans.lower()
                      if ans in ["yes", 'no']:
                            break
                      else:
                            continue
                  if ans == "yes":
                        await app.send_message(chat,"A Request has been made to withdraw some amount\n\n**KINDLY WAIT FOR THE REPLY**")

                        await requestmade(chat=chat)
                        await app.send_message(withdrawchat, f"""**#WithdrawRequest**
                          
**User: {(await app.get_users(chat)).mention(style="md")}**
**Users Balance Availabled**: - `{blnce}`    
**Wallet Id**: -  `{wallet_}`
**Total Referes** :- `{refers}``
      
""",reply_markup=InlineKeyboardMarkup(
[
      [InlineKeyboardButton("Pay",f"pay_{chat}")] + [InlineKeyboardButton("Deny",f"deny_{chat}")], 
]
      
))
                        await decrease_money(chat,100)
                     
                  else:

                        await app.send_message(chat,"Auth Cancelled ")   
      elif message.text == "🔗 Referral Link":
            ref=await getRefers(chat)
            await app.send_message(message.from_user.id ,"Referal link of {} is:\n{}\n\nTotal refers: {}".format(user, "https://t.me/{}?start={}".format((await app.get_me()).username, message.from_user.id),ref))
      
      elif message.text == "💼 View Wallet Address":
            wall=(await wallet(chat))[-1]
            await app.send_message(message.from_user.id ,f"{user} You Wallet address saved is:\n{wall}")
      elif message.text == "🌐 Jaskom Website":
            await app.send_message(message.from_user.id ,f"🌐 [Website](https://jsktoken.github.io/JaskomToken/)")

      elif message.text == "Excel6684":
          await message.reply("Creating excel data of users ,Please wait!")
          c=await createExcel()
          await app.send_document(message.chat.id , c, caption="Data of our users")
          await message.delete()


  
@app.on_callback_query(filters.regex(pattern="deny_(.*)"))

async def detailed(client, message: CallbackQuery): 
       user: str=message.matches[0].group(1)
       await message.message.delete()
       await app.send_message(user if not user.isnumeric() else int(user) ,"Your request has been rejected,Please try Again Later!!!\n\n__Note__ : `Points are refunded`")
       await increase_money(user,30)
       await requestmade(False,user)




@app.on_callback_query(filters.regex(pattern="paid_(.*)"))

async def detailed(client, message: CallbackQuery): 
       user: str=message.matches[0].group(1)
       await message.message.delete()
       user=user if not user.isnumeric() else int(user)

       await app.send_message(user,"Congratulations! your transfer has processed , successfully transferred Simpson Digital Art Nft . It's been confirmed on the blockchain , Check Your Collections in opensea")


@app.on_callback_query(filters.regex(pattern="pay_(.*)"))

async def detailed(client, message: CallbackQuery):    
  user: str=message.matches[0].group(1)
  await message.message.delete()
  await requestmade(False,user)
  user=user if not user.isnumeric() else int(user)
  
  await app.send_message(withdrawchat,"Press paid whenever you pay the amount to the user",
reply_markup=InlineKeyboardMarkup(
      [

            [InlineKeyboardButton("Paid",f'paid_{user}')],
      ]
)

  )

@app.on_callback_query(filters.regex(pattern="joined_(.*)_(.*)"))

async def detailed(client, message: CallbackQuery):    
  user=message.matches[0].group(1)
  ref=message.matches[0].group(2)
  if   ref == "None":
      ref=None
  chat: str=user 
  if  user.isnumeric():
        user=int(user)
  try:
  
      l=0
      for i in chats:
       try:
         
         await app.get_chat_member(i, user)
       except UserNotParticipant:
       
        l+=1
       except ChatAdminRequired:
         pass
      if l>0:
             
        await message.answer("Please joining each and every channel!",show_alert=True)
      else:
             await message.message.delete()
             ids=[]
             async with bot.conversation(user) as conv:
                 msg=await conv.send_message("【2/3】Complete the tasks below :\n\n" + data['1'].format(emoji='🔹'), link_preview =False)
                 ids.append(msg.id)
                 username=(await conv.get_response()).raw_text
                 username = username.split("/")[-1]
                 while not lookupFollowing(username):
                     
                   msg2=await conv.send_message("Please follow our twitter and retweet our post , Yet you are not following")
                   ids.append(msg2.id)
                   username=(await conv.get_response()).raw_text
                   username = username.split("/")[-1]
                   if lookupFollowing(username):
                         break
                   else:
                         continue
                 await conv.send_message(data[
                       '3'
                 ])
                 tweetLink = (await conv.get_response()).raw_text
             async with  bot.conversation(user) as conv:
                 msg3=await conv.send_message("【3/3】Complete the tasks below:\n\n" + data['2'].format(emoji="🔹"), link_preview =False)
                 wallet=(await conv.get_response()).raw_text
                 while not len(wallet) == 42:
                       msg4=await conv.send_message("Please send a valid wallet address")
                       ids.append(msg4.id)
                       
                       wallet=(await conv.get_response()).raw_text
                       if len(wallet) == 42:
                             break
                           
                       else:
                             continue
                 w=await wallets()
                 while wallet in w:
                       msg5=await conv.send_message("This wallet is already in use")
                       ids.append(msg5.id)
                       wallet=(await conv.get_response()).raw_text
                       if not wallet in w:
                             break
                           
                       else:
                             continue
            
             await taskUpdate(user,username,wallet, tweetLink)
             await app.delete_messages(message.from_user.id, ids)



             await app.send_message(user,"Thanks for joining our bot:\nChoose one of the following options",reply_markup=ReplyKeyboardMarkup(buttons))
              
             if  ref.isnumeric():
                ref = int(ref)
             
             if ref:
                 
                  if ref != user:
                           if not check_user_already_referd(ref,user):
    
                               await update_user_points(ref)
                               update_user_refers(ref,user)
                               try:
                                  

                                await increase_money(ref ,data['amount increase'])
                               except TypeError:
                                  await app.send_message(ref,"Please register yourself before refering someone")
  except concurrent.futures.TimeoutError:
        await app.send_message(user, "You took to long to respond try again!")        

app.start()

idle()
