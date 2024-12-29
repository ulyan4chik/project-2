import pygame
import math
import re

pygame.init()
screen_width, screen_height = 500, 600
white_color = (255, 255, 255)
black_color = (0, 0, 0)
grey_color = (200, 200, 200)
pink_color = (255, 182, 193)
purple_color = (238, 130, 238)
font = pygame.font.Font(None, 36)


class CalculatorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background = pygame.image.load('bg.jpg')
        pygame.display.set_caption("Калькулятор Ульяны Смирновой!")
        self.running = True
        self.mode = None
        self.calculator = None
        self.mode_buttons = [
            Button(screen_width // 4, 200, screen_width // 2, 50, "Обычный", pink_color, self.select_basic_mode),
            Button(screen_width // 4, 300, screen_width // 2, 50, "Уравнения", purple_color, self.select_smart_mode)
        ]

    def select_basic_mode(self):
        self.mode = 0
        self.calculator = BasicCalculator(self.screen, self.return_to_main_menu)

    def select_smart_mode(self):
        self.mode = 1
        self.calculator = SmartCalculator(self.screen, self.return_to_main_menu)

    def return_to_main_menu(self):
        self.mode = None
        self.calculator = None

    def run(self):
        while self.running:
            self.screen.fill(white_color)
            self.screen.blit(self.background, (0, 0))
            if self.mode is None:
                self.show_mode_selection()
            elif self.calculator:
                self.calculator.update()
                self.calculator.draw()
            pygame.display.flip()
            self.handle_events()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if self.mode is None:
                for button in self.mode_buttons:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button.rect.collidepoint(
                            event.pos):
                        button.click()
            elif self.calculator:
                self.calculator.handle_event(event)

    def show_mode_selection(self):
        title = font.render("Выберите свой калькулятор!", True, white_color)
        self.screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))
        for button in self.mode_buttons:
            button.draw(self.screen)


# Класс обычного калькулятора
class BasicCalculator:
    def __init__(self, screen, return_to_menu):
        self.screen = screen
        self.input_text = ""
        self.result = ""
        self.buttons = self.create_buttons()
        self.return_to_menu = return_to_menu
        self.back_button = Button(20, 520, 100, 50, "Назад", white_color, self.return_to_menu)

    def create_buttons(self):
        buttons = []
        button_texts = [
            "1", "2", "3", "/", "sin",
            "4", "5", "6", "*", "cos",
            "7", "8", "9", "-", "ln",
            "0", ".", "C", "+", "^2", "="
        ]
        x, y = 20, 100
        for text in button_texts:
            buttons.append(Button(x, y, 80, 50, text, grey_color, None))
            x += 90
            if x + 80 > screen_width:
                x = 20
                y += 60
        return buttons

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, white_color, (20, 20, screen_width - 40, 50))
        input_surface = font.render(self.input_text, True, black_color)
        self.screen.blit(input_surface, (30, 30))
        self.back_button.draw(self.screen)
        for button in self.buttons:
            button.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos):
                    self.handle_button_click(button.text)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.rect.collidepoint(event.pos):
                self.return_to_menu()

    def handle_button_click(self, text):
        if text == "C":
            self.input_text = ""
        elif text == "=":
            self.calculate_result()
        elif text == "Назад":
            self.return_to_menu()
        elif text in ["sin", "cos", "ln", "^2"]:
            self.apply_function(text)
        else:
            self.input_text += text

    def calculate_result(self):
        try:
            self.input_text = str(eval(self.input_text))
        except ZeroDivisionError:
            self.input_text = "На ноль делить нельзя"
        except:
            self.input_text = "Ошибка"

    def apply_function(self, func):
        try:
            num = float(self.input_text)
            if func == "sin":
                self.input_text = str(math.sin(num))
            elif func == "cos":
                self.input_text = str(math.cos(num))
            elif func == "ln":
                if num > 0:
                    self.input_text = str(math.log(num))
                else:
                    self.input_text = "Ошибка"
            elif func == "^2":
                self.input_text = str(num ** 2)
        except:
            self.input_text = "Ошибка"


# Класс калькулятора для уравнений
class SmartCalculator:
    def __init__(self, screen, return_to_menu):
        self.screen = screen
        self.input_text = ""
        self.result = ""
        self.return_to_menu = return_to_menu
        self.back_button = Button(20, 520, 100, 50, "Назад", white_color, self.return_to_menu)

    def update(self):
        pass

    def draw(self):
        pygame.draw.rect(self.screen, white_color, (20, 20, screen_width - 40, 50))
        input_surface = font.render(self.input_text, True, black_color)
        self.screen.blit(input_surface, (30, 30))
        solve_label = font.render("Введите уравнение вида ax+b=0", True, white_color)
        self.screen.blit(solve_label, (20, 100))
        self.back_button.draw(self.screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.rect.collidepoint(event.pos):
                self.return_to_menu()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.solve_equation()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode

    def solve_equation(self):
        try:
            match = re.match(r"([+-]?\d*\.?\d*)x([+-]\d*\.?\d*)=0", self.input_text.replace(" ", ""))
            if match:
                a, b = map(float, match.groups())
                self.result = f"x = {-b / a:.2f}"
            else:
                self.result = "Ошибка"
            self.input_text = self.result
        except:
            self.input_text = "Ошибка"


# Класс Кнопки
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        label = font.render(self.text, True, black_color)
        screen.blit(label, (self.rect.centerx - label.get_width() // 2, self.rect.centery - label.get_height() // 2))

    def click(self):
        if self.action:
            self.action()


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
