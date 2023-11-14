import PySimpleGUI as sg
from base import get_target_number

class GuessNumberGame:
    def __init__(self):
        self.target_number = get_target_number()
        self.attempts = 0
        self.player_name = ''
        self.history_file = 'game_history.txt'
        self.results_window = None
        self.window = None

    def is_even(self, number):
        return number % 2 == 0

    def run(self):
        layout = [
            [sg.Text('Введіть ваше ім\'я:'), sg.InputText(key='-NAME-')],
            [sg.Text('Вгадайте число від 1 до 20:')],
            [sg.InputText(key='-GUESS-')],
            [sg.Button('ОК'), sg.Button('Вивести результати'), sg.Button('Вихід')],
            [sg.Text('', size=(40, 2), key='-OUTPUT-')],
            [sg.Text('', size=(40, 2), key='-EVEN-')]
        ]

        self.window = sg.Window('ВГАДАЙ ЧИСЛО', layout, finalize=True)
        game_handler = GameHandler(self)

        while True:
            event, values = self.window.read()

            if event in (sg.WIN_CLOSED, 'Вихід'):
                break

            game_handler.handle_event(event, values)
            
        self.window.close()

    def save_game_history(self, result_message):
        with open(self.history_file, 'a') as file:
            file.write(f"{self.player_name}: {result_message}\n")

    def show_results(self):
        if self.results_window:
            self.results_window.close()

        layout = [
            [sg.Text('Результати гри')],
            [sg.Multiline(self.read_history(), size=(50, 10), key='-RESULTS-', disabled=True)],
            [sg.Button('Закрити')]
        ]

        self.results_window = sg.Window('Результати гри', layout, finalize=True)

        while True:
            event, values = self.results_window.read()

            if event in (sg.WIN_CLOSED, 'Закрити'):
                break

        self.results_window.close()

    def read_history(self):
        try:
            with open(self.history_file, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return 'Історія гри порожня.'

class GameHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event, values):
        if event == 'ОК':
            self.game.player_name = values['-NAME-']
            user_guess = values['-GUESS-']

            if user_guess.isdigit():
                user_guess = int(user_guess)
                self.game.attempts += 1
                self.process_guess(user_guess)

        elif event == 'Вивести результати':
            self.game.show_results()

    def process_guess(self, user_guess):
        if user_guess < self.game.target_number:
            self.game.window['-OUTPUT-'].update('Загадане число більше.')
        elif user_guess > self.game.target_number:
            self.game.window['-OUTPUT-'].update('Загадане число менше.')
        else:
            result_message = f"Вітаємо, {self.game.player_name}! Ви вгадали число {self.game.target_number} за {self.game.attempts} спроб."

            if self.game.is_even(self.game.target_number):
                self.game.window['-EVEN-'].update('Загадане число парне!')
                result_message += ' (парне)'
            else:
                self.game.window['-EVEN-'].update('Загадане число непарне!')
                result_message += ' (непарне)'

            self.game.window['-OUTPUT-'].update(result_message)
            self.game.save_game_history(result_message)

game = GuessNumberGame()
game.run()
