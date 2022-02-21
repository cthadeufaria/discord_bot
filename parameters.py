from boludito import blackjack


class Parameters:

    def __init__(self):
        self.boludos = {
            'DonHabraone#2093' : ['Victor', 0],
            'J Cresta#1514' : ['Tonê', 0],
            'carlosfaria#3773' : ['Charles', 0]
        }

        self.messages = {
            'hola' : [
                '¡Hola! ¿Qué tal, {}?', 
                'No hablo con boludos, manito.',
                'Entra al canal de voz para escucharme, manito.'
            ],
            'erro' : [
                'No recordaré esta canción. Fumé mucha marihuana.',
                'Ya estoy tocando una canción, puto.',
                '¡No entiendo, cabrón! Solo hablo español.'
            ],
            'musica' : [
                'Tocando {}.'
            ], 'blackjack' : [
                'Vamos a jugar blackjack, chiquito!',
                "\nOs ganhos dos jogadores ficam em ",
                'Gracias por jugar!',
                'Jogador para. Dealer jogando',
                'Desculpe, digite uma resposta válida',
                'Desculpe, uma aposta precisa ser um numero inteiro',
                "Desculpe, sua aposta nao pode exceder ",
                "\nMao do Dealer",
                "<carta escondida>",
                "Jogardor estoura!",
                "Jogador vence!",
                "Dealer estoura!",
                "Dealer vence!",
                "Dealer Jogardor empatam!",
                'Distribuindo cartas!',
                "Quer jugar de novo? Digite 's' or 'n'",
                'Quer comprar outra carta ou parar? Enter "c" or "p" ',
                'Quantas fichas quer apostar? '
            ]
            # 'blackjack': [
            #     'Vamos a jugar blackjack, chiquito!',
            #     "\nPlayers winnings stand at ",
            #     'Thanks for playing!',
            #     'player stands. Dealer is playing',
            #     'Sorry, please enter a valid response',
            #     'Sorry, a bet must be an integer',
            #     "Sorry, your bet cannot exceed ",
            #     "\nDealer's Hand",
            #     "<card hidden>",
            #     "Player busts!",
            #     "Player wins!",
            #     "Dealer busts!",
            #     "Dealer wins!",
            #     "Dealer and Player tie! It's a push.",
            #     'Hitting deck!',
            #     "Would you like to play again? Enter 'y' or 'n'",
            #     'Would you like to hit or stand? Enter "h" or "s" ',
            #     'How many chips would you like to bet? '
            # ]
        }
        self.cucaracha = ['https://www.youtube.com/watch?v=jp9vFhyhNd8', 'La Cucaracha']

        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 4', 
            'options': '-vn'
        }

        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(title)s.%(etx)s',
            'quiet': False
        }

        self.ayuda_dict = {
            'add_file' : {
                'ayuda' : 'Lista comandos',
                'hola' : '¡Hola, manitos!',
                'tocar <nome da música>' : 'Toca música do Youtube.',
                'para' : 'Para de tocar música e disconecta do canal de áudio.'
            },
            'title' : {
                'ayuda' : [
                    '¡Ayuda, manitos!', '''LISTA DE COMANDOS DO BOLUDITO. Executar com "$<nome do comando>".'''
                ]
            }
        }
