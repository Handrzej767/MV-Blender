# MV-Blender

## Konfiguracja VS Code i Blender (najlepiej 5.0)
1. Instalacja rozszerzenia **Blender Development** (autor: Jacques Lucke) w VS Code.
2. Połączenie: `Ctrl+Shift+P` -> `Blender: Start`. Należy wskazać ścieżke do `blender.exe`.
3. Wykonanie skryptu: `Ctrl+Shift+P` -> `Blender: Run Script`. VS Code przesyła kod bezpośrednio do uruchomionej instancji Blendera.

## Nazewnictwo
Nazwa pliku .blend vs nazwa w outlinerze:
* **Ścieżka pliku:** Wykorzystywana wyłącznie w parametrze `filepath`.
* **Nazwa w Outlinerze:** Wykorzystywana w argumentach `name`, `obj_name` oraz `coll_name`.

## Funkcje:

### Transformacje
`transform_entity(name, loc, rot_deg, relative)`
* Obsługuje obiekty, światła, kamery oraz kolekcje.
* W przypadku kolekcji transformacja wykonywana na obiekcie typu *root*

| Argument | Opis |
| :--- | :--- |
| `name` | Nazwa obiektu lub kolekcji w Outlinerze. |
| `loc` | Krotka współrzędnych (X, Y, Z). |
| `rot_deg` | Rotacja w stopniach (X, Y, Z). |
| `relative` | `True` aby dodać wartości do obecnych; `False` aby ustawić na sztywno. |

### Import
* `import_object`: Import pojedynczego obiektu.
* `import_collection`: Import pełnej kolekcji z zachowaniem relacji między obiektami.

| Argument | Opis |
| :--- | :--- |
| `filepath` | Pełna ścieżka do pliku .blend. |
| `obj_name` / `coll_name` | Nazwa zasobu do zaimportowania z pliku źródłowego. |
| `main_obj_name` | (Tylko kolekcja) Nazwa głównego obiektu, który ma zostać przesunięty po imporcie. |
| `loc` | Docelowe położenie (X, Y, Z). |
| `rot_deg` | Docelowa rotacja w stopniach (X, Y, Z). |

### Światła
* `add_custom_light`: Tworzenie nowego źródła światła.
* `edit_light`: Edycja parametrów istniejącego światła.

| Argument | Opis |
| :--- | :--- |
| `l_type` | Typ światła: 'POINT', 'SUN', 'SPOT', 'AREA'. |
| `energy` | Moc światła. |
| `color` | Krotka RGB (0.0 do 1.0). |
| `name` | Nazwa obiektu światła w scenie. |

### Kamery - Dodawanie
* `add_camera`: Tworzy nową kamerę w określonym miejscu.

| Argument | Opis |
| :--- | :--- |
| `name` | Nazwa nowej kamery. |
| `loc` | Pozycja kamery (X, Y, Z). |
| `rot_deg` | Rotacja kamery w stopniach. |

### Kamery - Edycja i Ostrość
* `edit_camera`: Ustawienia soczewki i efektu Depth of Field.

| Argument | Opis |
| :--- | :--- |
| `focal_length` | Długość ogniskowej w mm. |
| `use_dof` | Włącza/wyłącza rozmycie tła. |
| `focus_obj_name` | Nazwa obiektu, na którym kamera ma trzymać ostrość. |
| `focus_dist` | Odległość ostrzenia w metrach (używane, gdy brak obiektu). |
| `fstop` | Wartość przysłony. |

---

### Mechanika Ostrości (DoF)
W Blenderze system Depth of Field działa według  hierarchii:

1. **Priorytet obiektu:** Jeśli podano `focus_obj_name`, Blender zignoruje `focus_dist`. Ostrość będzie "przyklejona" do tego obiektu, nawet jeśli się on porusza.
2. **Tryb Freehand (Dystans):** Aby użyć manualnego ustawienia odległości (`focus_dist`) ->  `focus_obj_name` = `None`.

## Project Controls
W zakładce modifiers (niebieski klucz) pod outlinerem:

- MaskOn - załącza maskę - zielone "podświetlenie"
- TrashDensity - zmienia gęstość śmieci na pasie
- BeltSpeed - zmienia prędkość ruchu śmieci
- SplatterPattern - zmienia wygląd zabrudzeń pasa (jest wyszarzony, ale funkcjonalny)
- Seed - zmienia losowane śmieci