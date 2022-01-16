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
            ]
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
