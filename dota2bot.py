from liquipedia import Dota2
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler
import os

token = os.environ.get('TelegramBot')
dota_obj = Dota2("ScoresBot/2.0 (http://www.moyu.life/; hibrick713@gmail.com)")


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="搜索比赛信息: /match <teamname>  \n\n查看最近比赛信息: /info")

def match(update: Update, context: CallbackContext):
    games = dota_obj.get_upcoming_and_ongoing_games()
    info = ''
    try:
        if context.args:
            teamname = context.args[0]
            for i in games:
                if i.get('team-left').lower() == teamname.lower() or i.get('team-right').lower() == teamname.lower():
                    info = info + '\n' + i.get('start_time') + ' ' + i.get('team-left') + ' vs ' + i.get('team-right') + ' [' + i.get('league') + ']\n'
            if len(info) ==0:
                update.effective_message.reply_text("未查询到相关队伍的比赛信息!")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=info)
        else:
            update.effective_message.reply_text('请使用 /match <teamname> 匹配比赛信息')
    except IOError as e: 
        print(e)
        update.effective_message.reply_text('请使用 /match <teamname> 匹配比赛信息')

def info(update: Update, context: CallbackContext):
    games = dota_obj.get_upcoming_and_ongoing_games()
    info = ''
    count = 0
    if games:
        try:
            while count < 5:
                info = info + games[count].get('start_time') + ' ' + games[count].get('team-left') + ' vs ' + games[count].get('team-right') + ' [' + games[count].get('league') + ']\n'
                count = count + 1
            context.bot.send_message(chat_id=update.effective_chat.id, text=info)
        except IOError as e:
            print(e)
            update.effective_message.reply_text('请使用 /info 查看最近比赛信息')
    else:
        update.effective_message.reply_text('最近无比赛信息')


if __name__ == "__main__":
    updater = Updater(token=token, use_context=True)
    start_handler = CommandHandler('start', start)
    match_handler = CommandHandler('match', match)
    info_handler = CommandHandler('info', info)
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(match_handler)
    updater.dispatcher.add_handler(info_handler)
    updater.start_polling()
    updater.idle()
