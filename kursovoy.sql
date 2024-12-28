-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 28 2024 г., 02:14
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `kursovoy`
--

-- --------------------------------------------------------

--
-- Структура таблицы `authorization`
--

CREATE TABLE `authorization` (
  `COD_Admin` int(128) NOT NULL,
  `Password_Admin` varchar(128) NOT NULL,
  `Name_Admin` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `authorization`
--

INSERT INTO `authorization` (`COD_Admin`, `Password_Admin`, `Name_Admin`) VALUES
(1, '12345', 'Admin');

-- --------------------------------------------------------

--
-- Структура таблицы `courses`
--

CREATE TABLE `courses` (
  `COD_Courses` int(11) NOT NULL,
  `COD_Teacher` int(11) NOT NULL,
  `Language` varchar(100) NOT NULL,
  `Course_Name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `courses`
--

INSERT INTO `courses` (`COD_Courses`, `COD_Teacher`, `Language`, `Course_Name`) VALUES
(27, 2, 'Английский', 'Английский для начинающих'),
(28, 2, 'Английский', 'Английский для любителей'),
(29, 2, 'Английский', 'Английский для проффесионалов'),
(30, 2, 'Английский', 'Разговорный английский'),
(31, 3, 'Итальянский', 'Итальянский для начинающих'),
(32, 3, 'Итальянский', 'Итальянский для любителей'),
(33, 3, 'Итальянский', 'Итальянский для проффесионалов'),
(34, 3, 'Итальянский', 'Разговорный итальянский'),
(35, 5, 'Немецкий', 'Немецкий для начинающих'),
(36, 5, 'Немецкий', 'Немецкий для любителей'),
(37, 5, 'Немецкий', 'Немецкий для проффесионалов'),
(38, 5, 'Немецкий', 'Разговорный немецкий'),
(39, 4, 'Французский ', 'Французский для начинающих'),
(40, 4, 'Французский ', 'Французский для любителей'),
(42, 4, 'Французский ', 'Французский для проффесионалов'),
(43, 4, 'Французский ', 'Разговорный французский '),
(44, 4, 'Арабский', 'Арабский для начинающих'),
(45, 4, 'Арабский', 'Арабский для любителей'),
(46, 4, 'Арабский', 'Арабский для проффесионалов'),
(47, 4, 'Арабский', 'Разговорный арабский');

-- --------------------------------------------------------

--
-- Структура таблицы `groups`
--

CREATE TABLE `groups` (
  `COD_Groups` int(11) NOT NULL,
  `COD_Courses` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `groups`
--

INSERT INTO `groups` (`COD_Groups`, `COD_Courses`) VALUES
(7, 27),
(8, 27),
(9, 28),
(14, 32),
(10, 44),
(11, 45),
(12, 46),
(13, 47);

-- --------------------------------------------------------

--
-- Структура таблицы `group_students`
--

CREATE TABLE `group_students` (
  `COD_Groups` int(11) NOT NULL,
  `COD_Student` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `group_students`
--

INSERT INTO `group_students` (`COD_Groups`, `COD_Student`) VALUES
(7, 13),
(7, 18),
(7, 19),
(7, 24),
(8, 2),
(8, 8),
(8, 9),
(8, 19),
(8, 20),
(9, 2),
(9, 14),
(9, 16),
(10, 14),
(10, 17),
(10, 26),
(11, 8),
(11, 13),
(11, 19),
(12, 2),
(12, 4),
(12, 25),
(13, 12),
(13, 14),
(13, 15),
(14, 13),
(14, 15),
(14, 26);

-- --------------------------------------------------------

--
-- Структура таблицы `student`
--

CREATE TABLE `student` (
  `COD_Student` int(128) NOT NULL,
  `Surname` varchar(128) NOT NULL,
  `Name` varchar(128) NOT NULL,
  `Midlname` varchar(128) NOT NULL,
  `Phone_number` varchar(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `student`
--

INSERT INTO `student` (`COD_Student`, `Surname`, `Name`, `Midlname`, `Phone_number`) VALUES
(2, 'Арбузов', 'Ваня', 'Владимирович', '+4567890356'),
(3, 'Рысев', 'Арсений', 'Сергеевич', '+78998987'),
(4, 'Семанов', 'Даниил', 'Андреевич', '+725325252'),
(8, 'Семаков', 'Антон', 'Валерьевич', '+798908909'),
(9, 'Сосискова', 'Ульяна', 'Владимировна', '+78247239532'),
(10, 'Хуршав', 'Олег', 'Монголович', '+7986756999'),
(11, 'Нурбиков', 'Илья', 'Семенович', '+787768999'),
(12, 'Морпехов', 'Владимир', 'Сергеевич', '+777777777'),
(13, 'Порохов', 'Илья', 'Дмитриевич', '+7899523953'),
(14, 'Гниенко', 'Григорий', 'Сергеевич', '+79589895345'),
(15, 'Рапулов', 'Сергей', 'Дмитриевич', '+9964386096'),
(16, 'Калов', 'Сергей', 'Дмитриевич', '+4354366'),
(17, 'Петросянов', 'Тимофей', 'Александрович', '+8788998'),
(18, 'Олегов', 'Семен', 'Владимирович', '+78979897'),
(19, 'Зарбеков', 'Илья', 'Владиславович', '+776878678'),
(20, 'Валетов', 'Бухмин', 'Сергеевич', '+86767686'),
(24, 'Жопов', 'Семён', 'Валентинович', '+7788998698'),
(25, 'Заиребгов', 'Валерий', 'Леонтьевич', '+79532555'),
(26, 'Лысов', 'Валерий', 'Семенович', '+788998896');

-- --------------------------------------------------------

--
-- Структура таблицы `teachers`
--

CREATE TABLE `teachers` (
  `COD_Teacher` int(128) NOT NULL,
  `Surname` varchar(128) NOT NULL,
  `Name` varchar(128) NOT NULL,
  `Midlname` varchar(128) NOT NULL,
  `Phone_number` varchar(12) NOT NULL,
  `Work_email` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `teachers`
--

INSERT INTO `teachers` (`COD_Teacher`, `Surname`, `Name`, `Midlname`, `Phone_number`, `Work_email`) VALUES
(2, 'Порошин', 'Андрей', 'Анатольевич', '+79229357069', 'Kurae99@yandex.ru'),
(3, 'Ильин', 'Тимофей', 'Генадьевич', '+43848856298', 'Timik9l@ruspatriot.ru'),
(4, 'Миклин', 'Илья', 'Анатольевич', '+79223239592', 'Tochno_neskam@ww.ru'),
(5, 'Огнев', 'Григорий', 'Сергеевич', '+78248984848', 'winoven@rupatriot.su');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `authorization`
--
ALTER TABLE `authorization`
  ADD PRIMARY KEY (`COD_Admin`);

--
-- Индексы таблицы `courses`
--
ALTER TABLE `courses`
  ADD PRIMARY KEY (`COD_Courses`,`COD_Teacher`,`Language`),
  ADD KEY `COD_Teacher` (`COD_Teacher`);

--
-- Индексы таблицы `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`COD_Groups`),
  ADD KEY `COD_Courses` (`COD_Courses`);

--
-- Индексы таблицы `group_students`
--
ALTER TABLE `group_students`
  ADD PRIMARY KEY (`COD_Groups`,`COD_Student`),
  ADD KEY `COD_Student` (`COD_Student`);

--
-- Индексы таблицы `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`COD_Student`);

--
-- Индексы таблицы `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`COD_Teacher`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `authorization`
--
ALTER TABLE `authorization`
  MODIFY `COD_Admin` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `courses`
--
ALTER TABLE `courses`
  MODIFY `COD_Courses` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT для таблицы `groups`
--
ALTER TABLE `groups`
  MODIFY `COD_Groups` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT для таблицы `student`
--
ALTER TABLE `student`
  MODIFY `COD_Student` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT для таблицы `teachers`
--
ALTER TABLE `teachers`
  MODIFY `COD_Teacher` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`COD_Teacher`) REFERENCES `teachers` (`COD_Teacher`);

--
-- Ограничения внешнего ключа таблицы `groups`
--
ALTER TABLE `groups`
  ADD CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`COD_Courses`) REFERENCES `courses` (`COD_Courses`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `group_students`
--
ALTER TABLE `group_students`
  ADD CONSTRAINT `group_students_ibfk_2` FOREIGN KEY (`COD_Student`) REFERENCES `student` (`COD_Student`),
  ADD CONSTRAINT `group_students_ibfk_3` FOREIGN KEY (`COD_Groups`) REFERENCES `groups` (`COD_Groups`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
