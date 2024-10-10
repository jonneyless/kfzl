from environs import Env

env = Env()
env.read_env()

# ----------------------------------------------------------------------------------------------------------------------

mysqlInfo = {
    "host": env.str("DB_HOST", "127.0.0.1"),
    "db": env.str("DB_DATABASE", "private"),
    "user": env.str("DB_USER", "root"),
    "passwd": env.str("DB_PASS", "f0f107a30386718b"),
    "port": env.int("DB_PORT", 3306),
}

bot_token = env.str("BOT_TOKEN", "6880694966:AAH1IbrJskJMvUwdHil6lGB63dJIrnmUK6M")
bot_id = env.int("BOT_TG_ID", 6880694966)

app_id = 22330058
app_hash = "c8c2f318a089aff99b7949d1092bfec2"

bot_url = "https://api.telegram.org/bot2094467068:AAEPpPFe2mxoT8eeWeg-rMBy-ArsQ3ER87Y/"
