-- phpMyAdmin SQL Dump
-- version 5.2.1deb1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 30, 2024 at 03:35 PM
-- Server version: 10.11.6-MariaDB-0+deb12u1
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `robotdb`
--
CREATE DATABASE IF NOT EXISTS `robotdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `robotdb`;

-- --------------------------------------------------------

--
-- Table structure for table `child_nets`
--

CREATE TABLE `child_nets` (
  `net_id` char(12) NOT NULL,
  `score` decimal(10,0) DEFAULT NULL,
  `instance` longblob DEFAULT NULL,
  `session` char(12) DEFAULT NULL,
  `method` varchar(55) NOT NULL,
  `logic_count` int(11) NOT NULL,
  `memory_count` int(11) NOT NULL,
  `thresholds` tinyint(1) NOT NULL,
  `panel_id` char(12) DEFAULT NULL,
  `wins` int(11) DEFAULT NULL,
  `games` int(11) DEFAULT NULL,
  `genealogy` varchar(64000) DEFAULT NULL,
  `evolves` int(11) DEFAULT NULL,
  `species` varchar(64) DEFAULT NULL,
  `filename` varchar(64) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT current_timestamp(),
  `variability` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- --------------------------------------------------------

--
-- Table structure for table `nets`
--

CREATE TABLE `nets` (
  `net_id` char(12) NOT NULL,
  `score` decimal(10,0) DEFAULT NULL,
  `evolves` decimal(10,0) DEFAULT NULL,
  `filename` varchar(55) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `method` varchar(55) DEFAULT NULL,
  `logic_count` int(11) DEFAULT NULL,
  `memory_count` int(11) DEFAULT NULL,
  `thresholds` tinyint(1) DEFAULT NULL,
  `species` char(63) DEFAULT NULL,
  `instance` longblob DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `panel_id` char(12) DEFAULT NULL,
  `wins` int(11) DEFAULT NULL,
  `games` int(11) DEFAULT NULL,
  `session` char(12) DEFAULT NULL,
  `genealogy` varchar(63000) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `panellists`
--

CREATE TABLE `panellists` (
  `panellist_id` char(12) NOT NULL,
  `panel_id` char(12) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `player_id` char(12) NOT NULL,
  `player_name` varchar(64) DEFAULT NULL,
  `player_instance` longblob NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `panels`
--

CREATE TABLE `panels` (
  `panel_id` char(12) NOT NULL,
  `panel_desc` varchar(255) NOT NULL,
  `survival_score` int(11) NOT NULL,
  `lowest_acceptable_score` int(11) NOT NULL,
  `species` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `parameters`
--

CREATE TABLE `parameters` (
  `parm_index` varchar(63) NOT NULL,
  `parm_value` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `results`
--

CREATE TABLE `results` (
  `result_id` char(12) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `winner` varchar(65) DEFAULT NULL,
  `loser` varchar(65) DEFAULT NULL,
  `who_winner` int(11) DEFAULT NULL,
  `game_moves` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `robots`
--

CREATE TABLE `robots` (
  `robot_id` char(12) NOT NULL,
  `robot_name` varchar(63) DEFAULT NULL,
  `robot_instance` blob DEFAULT NULL,
  `robot_desc` text DEFAULT NULL,
  `robot_level` char(1) DEFAULT NULL,
  `robot_score` int(11) DEFAULT NULL,
  `species` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;

-- --------------------------------------------------------

--
-- Table structure for table `serial_nos`
--

CREATE TABLE `serial_nos` (
  `object_type` char(4) NOT NULL,
  `last_no_used` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `session_id` char(12) NOT NULL,
  `lowest_acceptable_score` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `test`
--

CREATE TABLE `test` (
  `fdsfdsa` int(11) NOT NULL,
  `fdsfd` int(11) NOT NULL,
  `fdsaa` int(11) NOT NULL,
  `fdsaffff` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `test_states`
--

CREATE TABLE `test_states` (
  `test_state_id` char(12) NOT NULL,
  `state_string` varchar(64) DEFAULT NULL,
  `state_desc` varchar(64) DEFAULT NULL,
  `selector` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `variegation_sessions`
--

CREATE TABLE `variegation_sessions` (
  `session_id` char(12) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `available` tinyint(1) NOT NULL,
  `parent_net` char(12) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `parent_score` int(11) DEFAULT NULL,
  `species` char(63) NOT NULL,
  `variability` float DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `nets`
--
ALTER TABLE `nets`
  ADD PRIMARY KEY (`net_id`);

--
-- Indexes for table `panellists`
--
ALTER TABLE `panellists`
  ADD PRIMARY KEY (`panellist_id`,`panel_id`) USING BTREE;

--
-- Indexes for table `panels`
--
ALTER TABLE `panels`
  ADD PRIMARY KEY (`panel_id`);

--
-- Indexes for table `parameters`
--
ALTER TABLE `parameters`
  ADD PRIMARY KEY (`parm_index`);

--
-- Indexes for table `results`
--
ALTER TABLE `results`
  ADD PRIMARY KEY (`result_id`);

--
-- Indexes for table `robots`
--
ALTER TABLE `robots`
  ADD PRIMARY KEY (`robot_id`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`session_id`);

--
-- Indexes for table `test`
--
ALTER TABLE `test`
  ADD PRIMARY KEY (`fdsfdsa`);

--
-- Indexes for table `test_states`
--
ALTER TABLE `test_states`
  ADD PRIMARY KEY (`test_state_id`);

--
-- Indexes for table `variegation_sessions`
--
ALTER TABLE `variegation_sessions`
  ADD PRIMARY KEY (`session_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
