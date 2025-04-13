

import pygame
import random
import os

pygame.init()  # Inicjalizowanie gry

# Stałe gry tj. Wielkość okna, kolory i kształty
BLOCK_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]


class Tetris:
    """Klasa obsługująca logikę, renderowanie i interakcje użytkownika w grze Tetris.

    Attributes:
        screen (pygame.Surface): Powierzchnia okna gry.
        clock (pygame.time.Clock): Obiekt do kontrolowania czasu w grze.
        font (pygame.font.Font): Czcionka do renderowania tekstu.
        player_name (str): Nazwa gracza wprowadzona przed rozpoczęciem gry.
        grid (list): Siatka gry przechowująca kolory klocków.
        current_piece (dict): Aktualny klocek w grze.
        game_over (bool): Flaga wskazująca koniec gry.
        score (int): Aktualny wynik gracza.
        highscore (int): Najwyższy zapisany wynik.
    """

    def __init__(self):
        """Inicjalizuje okno gry, czcionkę, nazwę gracza i stan gry."""
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 24)
        self.player_name = self.get_player_name()
        self.reset_game()
        self.highscore = self.load_highscore()

    def reset_game(self):
        """Resetuje stan gry do wartości początkowych."""
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0
        self.fast_fall = False
        self.move_left = False
        self.move_right = False
        self.move_time = 0
        self.move_delay = 100

    def load_highscore(self):
        """Wczytuje najwyższy wynik z pliku 'tetris_scores.txt'.

        Returns:
            int: Najwyższy wynik lub 0, jeśli plik jest pusty.
        """
        try:
            with open("tetris_scores.txt", "r") as file:
                scores = []
                for line in file:
                    if line.strip():
                        score = int(line.split(" - ")[0])
                        scores.append(score)
                return max(scores) if scores else 0
        except (FileNotFoundError, ValueError):
            return 0

    def get_player_name(self):
        """Pobiera nazwę gracza w oknie gry.

        Returns:
            str: Wprowadzona nazwa gracza lub 'Gracz', jeśli pusta.
        """
        name = ""
        input_active = True
        while input_active:
            self.screen.fill(BLACK)
            prompt = self.font.render("Podaj swoją nazwę:", True, WHITE)
            name_text = self.font.render(name, True, WHITE)
            instruction = self.font.render("Naciśnij Enter, aby potwierdzić", True, WHITE)
            self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and name.strip():
                        return name.strip() if name.strip() else "Gracz"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif len(name) < 20:
                        name += event.unicode if event.unicode.isprintable() else ""

    def new_piece(self):
        """Tworzy nowy klocek z losowym kształtem i kolorem.

        Returns:
            dict: Klocek z atrybutami shape, color, x, y.
        """
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color, "x": GRID_WIDTH // 2 - len(shape[0]) // 2, "y": 0}

    def valid_move(self, piece, x, y):
        """Sprawdza, czy ruch klocka jest możliwy.

        Args:
            piece (dict): Klocek do sprawdzenia.
            x (int): Pozycja x klocka.
            y (int): Pozycja y klocka.

        Returns:
            bool: True, jeśli ruch jest możliwy, False w przeciwnym razie.
        """
        for i in range(len(piece["shape"])):
            for j in range(len(piece["shape"][i])):
                if piece["shape"][i][j]:
                    if (x + j < 0 or x + j >= GRID_WIDTH or
                        y + i >= GRID_HEIGHT or
                        y + i >= 0 and self.grid[y + i][x + j] != BLACK):
                        return False
        return True

    def merge_piece(self):
        """Łączy klocek z siatką gry i sprawdza koniec gry."""
        for i in range(len(self.current_piece["shape"])):
            for j in range(len(self.current_piece["shape"][i])):
                if self.current_piece["shape"][i][j]:
                    self.grid[self.current_piece["y"] + i][self.current_piece["x"] + j] = self.current_piece["color"]
        self.clear_lines()
        self.current_piece = self.new_piece()
        if not self.valid_move(self.current_piece, self.current_piece["x"], self.current_piece["y"]):
            self.game_over = True

    def clear_lines(self):
        """Usuwa pełne linie z siatki i aktualizuje wynik."""
        new_grid = [row for row in self.grid if any(cell == BLACK for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        if lines_cleared == 1:
            self.score += 50
        elif lines_cleared == 2:
            self.score += 125
        elif lines_cleared == 3:
            self.score += 250
        elif lines_cleared == 4:
            self.score += 500
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_grid

    def rotate_piece(self):
        """Obraca aktualny klocek, jeśli ruch jest możliwy."""
        new_shape = [[self.current_piece["shape"][j][i] for j in range(len(self.current_piece["shape"]))]
                     for i in range(len(self.current_piece["shape"][0])-1, -1, -1)]
        temp_shape = self.current_piece["shape"]
        self.current_piece["shape"] = new_shape
        if not self.valid_move(self.current_piece, self.current_piece["x"], self.current_piece["y"]):
            self.current_piece["shape"] = temp_shape

    def save_score(self):
        """Zapisuje wynik gracza do pliku 'tetris_scores.txt'."""
        with open("tetris_scores.txt", "a") as file:
            file.write(f"{self.score} - {self.player_name}\n")
        self.highscore = max(self.highscore, self.score)

    def draw(self):
        """Rysuje siatkę gry, aktualny klocek oraz wyniki na ekranie."""
        self.screen.fill(BLACK)
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.grid[i][j] != BLACK:
                    pygame.draw.rect(self.screen, self.grid[i][j],
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                   (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
        for i in range(len(self.current_piece["shape"])):
            for j in range(len(self.current_piece["shape"][i])):
                if self.current_piece["shape"][i][j]:
                    pygame.draw.rect(self.screen, self.current_piece["color"],
                                   ((self.current_piece["x"] + j) * BLOCK_SIZE,
                                    (self.current_piece["y"] + i) * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE,
                                   ((self.current_piece["x"] + j) * BLOCK_SIZE,
                                    (self.current_piece["y"] + i) * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 1)
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(highscore_text, (10, 10))
        self.screen.blit(score_text, (10, 40))
        pygame.display.flip()

    def game_over_screen(self):
        """Wyświetla ekran końca gry i pozwala wybrać ponowną grę lub wyjście.

        Returns:
            bool: True, jeśli wybrano ponowną grę, False, jeśli wyjście.
        """
        self.save_score()
        selected = 0  # 0: Zagraj ponownie, 1: Wyjdź
        while True:
            self.screen.fill(BLACK)
            game_over_text = self.font.render("Game Over!", True, WHITE)
            score_text = self.font.render(f"Twój wynik: {self.score}", True, WHITE)
            play_again_text = self.font.render("Zagraj ponownie", True, GREEN if selected == 0 else WHITE)
            exit_text = self.font.render("Wyjdź", True, RED if selected == 1 else WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
            self.screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = 0
                    elif event.key == pygame.K_DOWN:
                        selected = 1
                    elif event.key == pygame.K_RETURN:
                        return selected == 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    play_again_rect = play_again_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                    if play_again_rect.collidepoint(mouse_pos):
                        return True
                    if exit_rect.collidepoint(mouse_pos):
                        return False

    def run(self):
        """Uruchamia główną pętlę gry, obsługując logikę i zdarzenia."""
        while True:
            fall_time = 0
            fall_speed = 500
            fast_fall_speed = 50
            while not self.game_over:
                fall_time += self.clock.get_rawtime()
                self.move_time += self.clock.get_rawtime()
                self.clock.tick()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.save_score()
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move_left = True
                            self.move_right = False
                            if self.valid_move(self.current_piece, self.current_piece["x"] - 1, self.current_piece["y"]):
                                self.current_piece["x"] -= 1
                            self.move_time = 0
                        if event.key == pygame.K_RIGHT:
                            self.move_right = True
                            self.move_left = False
                            if self.valid_move(self.current_piece, self.current_piece["x"] + 1, self.current_piece["y"]):
                                self.current_piece["x"] += 1
                            self.move_time = 0
                        if event.key == pygame.K_DOWN:
                            self.fast_fall = True
                        if event.key == pygame.K_UP:
                            self.rotate_piece()
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.move_left = False
                        if event.key == pygame.K_RIGHT:
                            self.move_right = False
                        if event.key == pygame.K_DOWN:
                            self.fast_fall = False

                if self.move_time >= self.move_delay:
                    if self.move_left and self.valid_move(self.current_piece, self.current_piece["x"] - 1, self.current_piece["y"]):
                        self.current_piece["x"] -= 1
                    if self.move_right and self.valid_move(self.current_piece, self.current_piece["x"] + 1, self.current_piece["y"]):
                        self.current_piece["x"] += 1
                    self.move_time = 0

                current_speed = fast_fall_speed if self.fast_fall else fall_speed
                if fall_time >= current_speed:
                    if self.valid_move(self.current_piece, self.current_piece["x"], self.current_piece["y"] + 1):
                        self.current_piece["y"] += 1
                    else:
                        self.merge_piece()
                    fall_time = 0

                self.draw()

            # Game Over
            if not self.game_over_screen():
                pygame.quit()
                return
            self.reset_game()

if __name__ == "__main__":
    game = Tetris()
    game.run()