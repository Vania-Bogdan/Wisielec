Ivan Bogdan, s30929, UA

Це моя курсова робота з програмування на Python. Я вирішив зробити класичну гру «Шибениця», але з сучасним графічним інтерфейсом, збереженням статистики гравців і додатковим режимом «на час».

Користувач може зареєструватися або увійти у вже існуючий профіль. Після цього відкривається меню, де він може обрати, як саме хоче грати: звичайний режим (одне слово — одна гра) або режим «на час», де є 3 хвилини, щоб вгадати якнайбільше слів. Всі слова беруться з файлів — вони поділені на категорії: наприклад, тварини, країни, фрукти. Категорія слова показується під час гри.

Під час гри малюється шибениця — поступово, при кожній помилці додається частина тіла. Гра закінчується перемогою (всі літери відгадані) або поразкою (максимум помилок).

Уся статистика (кількість перемог і поразок) зберігається для кожного користувача. Крім того, в окремому вікні можна переглянути статистику всіх гравців і натиском кнопки зберегти її у вигляді PDF-файлу.

Я намагався зробити все максимально просто, зручно і зрозуміло. Якщо додати нові слова або навіть категорії — їх досить просто записати у текстовий файл у відповідну папку.

Гру можна запускати через файл main.py, може бути вимагане встановлення необхідних бібліотек.







Ivan Bogdan, s30929, PL

To jest moja praca zaliczeniowa z programowania w Pythonie. Postanowiłem zrobić klasyczną grę "Wisielec", ale w wersji z graficznym interfejsem, zapisywaniem statystyk i dodatkowym trybem na czas.

Gracz może się zarejestrować albo zalogować na swoje konto. Potem pojawia się menu, gdzie wybiera, czy chce grać w zwykłym trybie (jedno słowo na rundę), czy w trybie na czas — tam ma 3 minuty, żeby odgadnąć jak najwięcej słów. Słowa są podzielone na kategorie (zwierzęta, kraje, owoce itd.) i ładowane z plików tekstowych. Podczas gry wyświetla się też aktualna kategoria.

Gdy gracz się myli, rysowany jest wisielec — krok po kroku. Przegrywa się po 6 błędach, a wygrywa gdy uda się odgadnąć całe słowo.

Każdy użytkownik ma swoją historię — zapisywane są jego wygrane i przegrane. Jest też okno, w którym można podejrzeć statystyki wszystkich graczy i od razu wyeksportować je do pliku PDF jednym kliknięciem.

Chciałem, żeby ta gra była jak najbardziej przejrzysta i prosta w użyciu. Dodawanie nowych słów jest bardzo łatwe — wystarczy zapisać je do odpowiedniego pliku.

Grę można uruchomić przez plik main.py, może być wymagane zainstalowanie potrzebnych bibliotek.
