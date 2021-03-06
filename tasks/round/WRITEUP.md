# Вокруг да около: Write-up

Таск — реверс с поиском строки в приложении.

Видим приложение под Windows на Qt. Запускаем приложение, и видим круглые часы — ничего больше. Нам говорят о некоем секретном послании в часах, а значит, придётся открывать отладчик. В разборе мы используем Cutter. Про реверс-инжиниринг с самых азов можно почитать [у нас в курсе](https://course.ugractf.ru/reverse/nightmare.html).

Запукаем Cutter, и видим некоторое количество функций в программе. Давайте осмотримся, просматривая функции по одной, и грубо разделяя их на следующие категории:

* Бизнес-логика: в таких функциях много вызовов других функций и внешних библиотек;
* Вычислительные: в таких функциях много разнообразных инструкций, в том числе с использованием векторных операций (MMX/SSE), и мало вызовов библиотек;
* Другие: короткие функции с парой вызовов. Иногда такие генерируются компилятором, иногда это — короткие процедуры-обёртки.

Во время изучения можно сразу переименовывать функции по их примерному содержанию. Например, если сверху вы увидите упоминание какого-то внешнего вызова, вы можете примерно догадаться о назначении функции. Неизвестные внешние функции (в основном, из Qt) лучше сразу искать в документации на библиотеку. Итого выделим интересные функции, сконцентрировавшись на функциях с внешними вызовами (здесь и далее адреса даются по расположению в исходном файле; при запущенном отладчике они будут различаться);

* `0x00401020`: Функция, где фигурирует `QWidget::constructor`, и `AnalogClock`: должно быть, компонент часов;
* `0x00401520`: Функция, где упоминается `QApplication::constructor`: начало работы программы;
* `0x00401cf0`: Функция с упоминанием `QMainWindow::constructor`, то есть создание главного окна программы;
* `0x00402240`: Интересная функция, в которой вызываются memset и memcpy;
* `0x004035e0`: Ещё одна функиця с memcpy;
* `0x004037f0`: Функция, которая явно делает что-то со шрифтами: в ней вызываются методы `QFontMetrics`;
* `0x00403dd0`: Ещё одна функция, выполняющая действия со шрифтами. В ней также вызывается `QLabel::constructor`, то есть создаются надписи где-то в интерфейсе программы;

Ниже последней находятся в основном функици, сгенерированные компилятором; нам они не так интересны.

В самой программе при этом мы не наблюдали никаких текстовых строк — это наводит на мысль, что у неё есть скрытые элементы интерфейса (возможно, открывающиеся по какому-то событию).

Проверим, что функция `0x00403dd0` вызывается: поставим на неё точку останова и запустим отладчик. Спустя несколько нажатий «Continue» мы попадаем в эту функцию, что означает, что метки и правда создаются во время создания главного окна. Изучая документацию, находим, что текст в QLabel устанавливается через вызов `setText`. Ищем его (он находится по адресу `0x004040e2`) и устанавливаем туда точку останова. Запускаем программу, и снова видим попадание — получается, каким-то меткам и правда присваивается текст.

Дальше было несколько вариантов размышления. Первый заключался в том, чтобы найти, где эти метки отрисовываются на форме. Тут поможет знание, что в современных интерфейсах круглые (и вообще фигурные) окна на самом деле не являются круглыми — это прямоугольные окна с заданной маской. Поискав, можно сразу же найти метод `setMask`, который позволяет задать такую маску в приложении на Qt. Находим вызов этого метода в Cutter (он находится по аресу `0x00401dca`) и отключаем его, заполняя NOPами (правая кнопка мыши ⟶ Edit ⟶ Nop instruction). Закрываем Radare, открываем приложение, и видим флаг вокруг часов в прямоугольном окне. На это решение намекает название и легенда к заданию.

![Окно с отключённой маской](writeup/window.png)

Второе решение заключается в извлечении самого текста. Метод `setText` принимает `QString`. Смотрим выше, и находим метод `fromAscii_helper`, а ещё выше — несколько вызовов `memcpy`. Первый метод явно намекает на преобразование строк из классического формата Си (указатель на нуль-терминированную строку); на это указывают и его аргументы. Остановим программу перед его вызовом (адрес `0x00404072`). Запускаем программу, и смотрим значение вверху стека: им оказывается искомый флаг.

![Стек во время остановки на вызове `fromAscii_helper`](writeup/stack.png)

Флаг: **ugra_look_around_df1618156b8e15aff626250605d718f9793907ce8**
