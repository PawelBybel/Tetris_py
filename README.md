
# Tetris

Klasyczna gra Tetris zaimplementowana w Pythonie przy użyciu biblioteki Pygame. Gra pozwala na sterowanie klockami, zdobywanie punktów za oczyszczanie linii, zapisywanie wyników oraz obsługę ekranu końca gry z opcją ponownego rozpoczęcia.

## Funkcjonalności

- **Sterowanie klockami**: Przesuwanie w lewo/prawo (strzałki), przyspieszanie opadania (strzałka w dół), obracanie (strzałka w górę).
- **System punktacji**: Punkty za oczyszczanie linii (50 za 1 linię, 125 za 2, 250 za 3, 500 za 4).
- **Najwyższy wynik**: Wczytywanie i zapisywanie wyników do pliku `tetris_scores.txt`.
- **Nazwa gracza**: Wprowadzanie nazwy przed rozpoczęciem gry.
- **Ekran końca gry**: Opcje "Zagraj ponownie" lub "Wyjdź" obsługiwane klawiaturą i myszą.

## Wymagania

- Python 3.6+
- Biblioteka Pygame (`pip install pygame`)

## Instalacja

1. Sklonuj repozytorium lub pobierz pliki projektu:
   ```bash
   git clone <(https://github.com/PawelBybel/Tetris_py)>
