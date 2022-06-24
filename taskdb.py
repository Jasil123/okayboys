from collections import OrderedDict
from re import I
import motor.motor_asyncio

import os
import logging
from pymongo import MongoClient
# t/ry:
MONGO = 'mongodb://jasilp:jasilp@ac-t5wsi2t-shard-00-00.esgifc8.mongodb.net:27017,ac-t5wsi2t-shard-00-01.esgifc8.mongodb.net:27017,ac-t5wsi2t-shard-00-02.esgifc8.mongodb.net:27017/?ssl=true&replicaSet=atlas-8phkkf-shard-0&authSource=admin&retryWrites=true&w=majority'
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO)
c2=MongoClient(MONGO)
c=c2.aca
cp=c['omk']
# except Exception as e:
#    logging.info("Failed Connection with mongo")
sed = client['Tasks']
db = sed['tasks']
Points=db.fer
points=Points

tasks=db.task
req=db.req
def string(arg):
    if not isinstance(arg, str):
        return str(arg)

async def taskUpdate(user ,username,wallet,retwett):
    db=tasks
    creds={"user": user, 'task': 0, 'money': 200000000, "twitterusername": username ,"walletaddress":wallet , "retweet": retwett}
    task=[i async for i in tasks.find({})]
    if not task:
        await db.insert_one(creds)
        return True
    p=False
    for i in task:
        if "user" in i:
            n=i['user']
            print(n)
            if n == user:
                p=True
                values={"user": user, "task":  i["task"],'money':  i['money'], "twitterusername": i['twitterusername'] ,"walletaddress":i['walletaddress'] ,"retweet": i['retweet']}
                
    print(p)
    if p:
         await db.update_one(values, {"$set": {"user": user, "task":  values.get("task") + 1 ,'money':  values.get("money")   , "twitterusername": values['twitterusername'],"walletaddress": values['walletaddress']  ,"retweet": values['retweet']}})
    else:
           await db.insert_one( creds) 
     


async def numberOFTaskDone(user):      
    async for i in tasks.find({}):
           if user == i.get('user'):
               return i.get("task") 
           
      
async def increase_money(user,amount):
    values={}
    async for i in tasks.find({}):
        
        if 'user' in i:
          if i['user'] == user:
              
            values.update(i)
    
    await tasks.update_one(values ,{"$set": {"user": user, "task": 9 ,'money':  values.get("money")  + amount , "twitterusername": values['twitterusername'],"walletaddress": values['walletaddress'] ,"retweet": values.get('retweet')}    }      )   
           
           
async def decrease_money(user,amount):
    values={}
    async for i in tasks.find({}):
        if 'user' in i:
          if i['user'] == user:
              
            values.update(i)
            
    await tasks.update_one(values ,{"$set": {"user": user, "task":  values.get("task") + 1 ,'money':  values.get("money")  - amount , "twitterusername": values['twitterusername'],"walletaddress": values['walletaddress'] ,"retweet": i['retweet']}})   
           
           

async def dataframes():
  w=[]
  link=[]
  retweet=[]
  twitt=[]
  user=[]    
  async for i in tasks.find({}):
    if 'user' in i:
        
     user.append(i.get("user"))
  user=list(OrderedDict.fromkeys(user))
  for i in user:
      link.append((await balance(i))[-1])
      w.append((await wallet(i))[-1])
      retweet.append((await retwett(i)) [-1])
      twitt.append( 
                   (await twitter(i)) [-1]
                   )
  data={
      "User": user,
      "Twitter Uername": twitt,
      "Retweet Link": retweet,
      "money":    link,
      "WalletAddr.": w
  }
  return data


async def wallets():
    wallet=[]
    async for i in tasks.find({}):
 
       if 'user' in i:
         wallet.append(i.get("walletaddress"))
    return wallet
async def twitter(user):
    twitterusername=[]
    async for i in tasks.find({}):
 
       if 'user' in i:
         if i['user'] == user:
             twitterusername.append(i.get("twitterusername"))
    return twitterusername

async def balance(user):
    money=[]
    async for i in tasks.find({}):
 
       if 'user' in i:
         if i['user'] == user:
             
          money.append(i.get("money"))
    
    return money
async def retwett(user):
    retweet=[]
    async for i in tasks.find({}):
 
       if 'user' in i:
         if i['user'] == user:
             
          retweet.append(i.get("retweet"))
    
    return retweet

async def requestmade(t=True,chat:str=None):
    if not isinstance(chat,str):
        chat=str(chat)
    await req.insert_one({chat:t})

async def request_created(chat):
    if not isinstance(chat,str):
        chat=str(chat)
    r=[]
    async for i in req.find({}):
     r.append(i.get(chat))
    if not r:
        return False

    return r[-1]        
async def wallet(user):
    wallet=[]
    async for i in tasks.find({}):
 
       if 'user' in i:
         if i['user'] == user:
             
          wallet.append(i.get("walletaddress"))
    return wallet



async def update_user_points(user,points =1 ):

    if not isinstance(user,str):
        user=str(user)
    db=Points
    i =i = [i async for i in db.find({})]
    if len(i) == 0:
      numb = {user:{"referal":1}}
      await db.insert_one(numb)
    else:
      for i in i:
          if user in i.keys():
           b=i[user]['referal']
           newvalues = { "$set": {user: {"referal":b+points} } }
           await db.update_one({user:{"referal":b}}, newvalues)
           return
          else:
              await db.insert_one({user:{"referal":1}})
              
              
              
        
def update_user_refers(user,referduser):
    if not isinstance(user,str):
        user=str(user)
    cp.insert_one({user:referduser})

async def getRefers(user):
    if not isinstance(user,str):
        user=str(user)
    async for i in points.find({}):
        if user in i:
            return i[user]['referal']


async def Stats():
  user=[]    
  async for i in tasks.find({}):
    if 'user' in i:
        
     user.append(i.get("user"))
    #  link.append( i.get('money')) ,
    #  username.append(i.get("twitterusername"))
    #  wallet.append(i.get("walletaddress"))
  user=list(OrderedDict.fromkeys(user))
  users={}
  for i in user:
      r=await getRefers(i)
      if not r:
          r=0
      users.update({i: r})
  return users

def all_referd_users(user):
    if not isinstance(user,str):
        user=str(user)
    
    u=[]
    p=[i for i in cp.find({})]
    for i in p:
      if user in i.keys():
         u.append(i[user])
    return list(OrderedDict.fromkeys(u))   


def check_user_already_referd(user,userid):
    b=False
    a=all_referd_users(user)
    if userid in a:
        b=True
    return b
