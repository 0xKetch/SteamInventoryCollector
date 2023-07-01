# Steam Inventory Collector
Helps you to collect items from multiple accounts and farm steam sale cards (for watching recommendation list)
   
# Quick guide 
For using programs you need to install the necessary libraries.

   `pip install -r requirements.txt`
   
## Settings
### settings.json file
Basic info about your main account on which you want to collect items
```
{
  # These are the required parameters
  "steam_api_key": "",
  "trade_url": "main_trade_url",
  # If you need auto accept trades
  "login": "main_login",
  "password": "main_password",
  "maFile": "your_main_maFile.maFile",
  # You do not need to fill in these parameters if you are not going to use autoclaim
  "telegram_bot_token": "",
  "telegram_chat_id": 0,
  "telegram_api_id": 0,
  "telegram_api_hash": ""
}
```
Steam api key can be found at https://steamcommunity.com/dev/apikey

### accounts.txt file
Fill this file with your accounts in the format `login password` (space separator).

Don't forget to add your main account.

### maFiles
Trades in Steam require SteamGuard, so the bot needs maFiles. (Use **SDA** to get it)

Replace `your_main_maFile.maFile` at the root of the directory to your main. 

You can rename it as you wish, but don't forget to change the name in `settings.json`.
   
Put the maFiles of all accounts from which you need to collect items in the maFiles folder.

In SDA the names of the mafiles include steamid64, you need to rename it to logins. 

You can do this by running `rename_mafiles.py` in the `utils` folder.

## About the bot
After all the preparations above you can use the bot. 

### claim_all.py (accepts trades)
This program will allow you to collect items from all accounts from the maFiles folder to the main one.

The first time you use it, it will work slowly, since Steam does not allow you to log in to accounts more than once a minute.

But after the first use, cookies from all accounts will be saved in the `cookies` folder, and the next use will be much faster.

On line 13, you can change or add the game you want to collect items from
```python
games = [GameOptions.CS, ]
```

### claim_without_accept.py (does not accept trades)
The same as above, but you can not specify the data and the maFile from the main account.

### autoclaim.py
This bot will help those who receive notifications in telegram about a new drop of items.

You can collect items immediately after receiving a telegram notification.

In the message about the steam drop, the account login (not nickname) must match the name of the file in the `maFiles` folder and be in the first place.

On line 17, you can change or add the game you want to collect items from
```python
games = [GameOptions.CS, ]
```

### About choosing a game

List of predefined games ([Source](https://github.com/bukson/steampy/blob/master/steampy/models.py)): 
```python
STEAM = PredefinedOptions('753', '6')
DOTA2 = PredefinedOptions('570', '2')
CS = PredefinedOptions('730', '2')
TF2 = PredefinedOptions('440', '2')
PUBG = PredefinedOptions('578080', '2')
RUST = PredefinedOptions('252490', '2')
```

You can add your games, if they are not in the list, in the steampy library.

An example for collecting all items from CS:GO, Dota2, Steam inventory:
```python
games = [GameOptions.CS, GameOptions.DOTA2, GameOptions.STEAM]
```

### sale_recommendations_cards_farmer.py
**To use this you have to use steampy from [my fork](https://github.com/0xKetch/steampy)**

This script is needed to view the list of recommendations in automatic mode for all your accounts.

During the Steam sale you can receive cards for this.

Then you can collect your cards to one account with `claim_all.py`.

The first time you use it, it will work slowly, since Steam does not allow you to log in to accounts more than once a minute.

But after the first use, cookies from all accounts will be saved in the `cookies` folder, and the next use will be much faster.

### Some problems

If you get an JSONDecodeError when starting a programm try [this](https://github.com/bukson/steampy/issues/241) 

Or just copy library files from [my fork](https://github.com/0xKetch/steampy)
