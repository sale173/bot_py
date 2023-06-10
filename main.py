import telebot

close_options = ['Да', 'Нет']
questions = [
    {'text': 'Выходите ли вы из себя по малейшему поводу?', 'type': 'closed', 'options': close_options},
    {'text': 'Боитесь ли вы разозлить человека, который заведомо физически сильнее вас?', 'type': 'closed', 'options': close_options},
]

other_types = [
    {'text': 'Как вас зовут?', 'type': 'opened'},
    {'text': 'Сколько вам лет?', 'type': 'number'},
    {'text': 'Как звали зайца из смешариков?', 'type': 'multiple_choice', 
    'options': ['Ежик', 'Крош', 'Нюша', 'Копатыч'], 'right_answer': ['Крош']}, 
]

questions = other_types + questions

class Anket:
    def __init__(self, config):
        self.config = config
        self.length = len(config)
        self.answers = None
        self.scores = 0
    def add_answers(self, answers: list):
        self.score = 0
        self.answers = answers
        self._counter()
        return self.scores
    def _counter(self):
        for i in range(self.length):
            qtype = self.config[i].get('type')
            qoptions = self.config[i].get('options')
            right_answer = self.config[i].get('right_answer')
            qanswer = self.answers[i]
            if qtype == 'closed':
                self.scores += 1 if qanswer == 'Да' else + 0
            if qtype == 'multiple_choice':
                if qanswer == right_answer:
                    self.scores += 2
                else:
                    self.scores -= 1
            if qtype == 'number':
                if qanswer > '5':
                    self.scores += 1
                else:
                    self.scores += 0       
    def get_question(self, k):
        self.k = k
        
        for key, value in questions[k].items():
            if key == 'text':
                return value
        
anket = Anket(questions)

TOKEN = '6100290797:AAHgu7R1ajGpgmTm0sOXkIxOL79dz_Wbez8'
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Привет, я бот! Ответь на мои вопросы")
    global answers
    answers = []
    k = 0
    bot.register_next_step_handler(message, new_text, k, answers)

def new_text(message, k, answers):
    if k == anket.length:
        score = anket.add_answers(answers)
        bot.send_message(chat_id=message.chat.id, text=f'спасибо за ответы, вы набрали: {score} баллов')
    else:
        answers.append(message.text)
        bot.send_message(chat_id=message.chat.id, text=anket.get_question(k))
        k += 1
        bot.register_next_step_handler(message, new_text, k, answers)
        
bot.polling()