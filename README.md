<div align="center">
  <a href="https://github.com/FixerBlur/PenPen-QuoteBot">
    <img src="file_readme/background.jpg" alt="Logo">
  </a>

<h3 align="center">😺 PenPen</h3>

  <p align="center">
    Your favorite quote in photo😊
    <br />
  </p>
</div>

## ℹ️ About The Project

<img src="file_readme/screen.jph"></img>

This bot can turn the text of your interlocutor in a chat or group into a quote on a photo. 
You need to press "reply" to the desired message and send it with the text "/c" and then the bot will send a photo with the text of the message you have chosen 

<hr>

## 🧧 Getting Started

1. Install the libraries and module you need

 ```sh
pip install aiogram==2.25.1
pip install aiofiles==23.2.1
pip install aiosqlite==0.19.0
pip install python-dotenv==1.0.0
pip install pillow==10.2.0
```
2. Create an .env file in the main project folder and place your bot's token in it in this form: 
```sh
BOT_TOKEN='your token her'
```
3. In the notify_admins.py file, insert the telegram id of your account into the admins variable so that you receive notifications about the bot startup and shutdown
 ```sh
admins = [your telegram id here]
 ```

