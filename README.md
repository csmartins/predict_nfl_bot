# Esse é o bot pra ajudar nos palpites dos jogos da NFL.
Os jogos são atualizados toda semana usando os dados vindos do Fantasy NFL.

# Comandos:
/start - Inicializa o bot;

/predict - Mostra jogo por jogo para que o usuário dê seus palpites. Deve ser usado apenas numa conversa privada com o bot;

/show - Mostra todos os palpites de todos os usuários do grupo;

/help - Lista os comandos.

# Build

$ zip deploy.zip 2/ *.py requirements.txt 

Exporte as chaves para variáveis de ambiente.

$ sudo docker build --build-arg telegram_token=$TELEGRAM_TOKEN --build-arg subscription_key=$SUBSCRIPTION_KEY .



# To Do
Contar o resultado dos palpites dos usuários;

Comando para listar os resultados dos jogos.

