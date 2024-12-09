ambiente = 'desenvolvimento'

if ambiente == 'desenvolvimento':
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'senai'
    DB_NAME = 'emprego'

#CONFIG CHAVE SECRETA (SESSION)
SECRET_KEY = 'emprego'

#ACESSO DO ADM
MASTER_EMAIL = 'adm@adm'
MASTER_PASSWORD = 'adm'