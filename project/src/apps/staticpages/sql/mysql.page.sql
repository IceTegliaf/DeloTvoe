-- phpMyAdmin SQL Dump
-- version 2.11.4
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Фев 03 2009 г., 17:33
-- Версия сервера: 5.0.51
-- Версия PHP: 5.2.4-2ubuntu5.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

--
-- База данных: `demo_mini`
--

--
-- Дамп данных таблицы `staticpages_page`
--

INSERT INTO `staticpages_page` (`id`, `language`, `title`, `address`, `content`, `published`, `seo_title`, `seo_keywords`, `seo_description`) VALUES
(1, 'ru', 'Контакты', 'contacts', 'Страница контактов компании<br />', 1,'', '', ''),
(2, 'ru', 'О компании', 'about', 'Страница о компании.<br />', 1,'', '', ''),
(3, 'en', 'Contacts', 'contacts', 'Contacts page.<br />', 1,'', '', ''),
(4, 'en', 'About company', 'about', 'Page about company.<br />', 1,'', '', '');
