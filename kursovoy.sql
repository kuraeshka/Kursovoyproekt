-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Дек 25 2024 г., 18:08
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
  `COD_Admin` int(11) NOT NULL,
  `Name_Admin` varchar(11) NOT NULL,
  `Password_Admin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `authorization`
--

INSERT INTO `authorization` (`COD_Admin`, `Name_Admin`, `Password_Admin`) VALUES
(1, 'Admin', 12345);

-- --------------------------------------------------------

--
-- Структура таблицы `courses`
--

CREATE TABLE `courses` (
  `COD_Courses` int(128) NOT NULL,
  `Course_Name` varchar(128) NOT NULL,
  `COD_Teacher` int(128) DEFAULT NULL,
  `Language` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `courses`
--

INSERT INTO `courses` (`COD_Courses`, `Course_Name`, `COD_Teacher`, `Language`) VALUES
(1, 'Курсы для начинающих по английскому языку', 3, 'Английский');

-- --------------------------------------------------------

--
-- Структура таблицы `groups`
--

CREATE TABLE `groups` (
  `COD_Groups` int(11) NOT NULL,
  `COD_Courses` int(11) DEFAULT NULL,
  `COD_Student` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
(3, 'Рысев', 'Арсений', 'Сергеевич', '+78998987');

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
(4, 'Миклин', 'Илья', 'Анатольевич', '+79223239592', 'Tochno_neskam@ww.ru');

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
  ADD PRIMARY KEY (`COD_Courses`),
  ADD UNIQUE KEY `COD_Teacher` (`COD_Teacher`);

--
-- Индексы таблицы `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`COD_Groups`),
  ADD UNIQUE KEY `COD_Courses` (`COD_Courses`),
  ADD UNIQUE KEY `COD_Student` (`COD_Student`);

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
  MODIFY `COD_Admin` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `courses`
--
ALTER TABLE `courses`
  MODIFY `COD_Courses` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `groups`
--
ALTER TABLE `groups`
  MODIFY `COD_Groups` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `student`
--
ALTER TABLE `student`
  MODIFY `COD_Student` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `teachers`
--
ALTER TABLE `teachers`
  MODIFY `COD_Teacher` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  ADD CONSTRAINT `groups_ibfk_1` FOREIGN KEY (`COD_Student`) REFERENCES `student` (`COD_Student`),
  ADD CONSTRAINT `groups_ibfk_2` FOREIGN KEY (`COD_Courses`) REFERENCES `courses` (`COD_Courses`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
