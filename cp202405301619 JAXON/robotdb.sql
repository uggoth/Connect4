-- MySQL dump 10.17  Distrib 10.3.17-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: robotdb
-- ------------------------------------------------------
-- Server version	10.3.17-MariaDB-0+deb10u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `child_nets`
--

DROP TABLE IF EXISTS `child_nets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `child_nets` (
  `net_id` char(12) COLLATE latin1_general_cs NOT NULL,
  `score` decimal(10,0) DEFAULT NULL,
  `instance` longblob DEFAULT NULL,
  `session` char(12) COLLATE latin1_general_cs DEFAULT NULL,
  `method` varchar(55) COLLATE latin1_general_cs NOT NULL,
  `logic_count` int(11) NOT NULL,
  `memory_count` int(11) NOT NULL,
  `thresholds` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_nets`
--

LOCK TABLES `child_nets` WRITE;
/*!40000 ALTER TABLE `child_nets` DISABLE KEYS */;
/*!40000 ALTER TABLE `child_nets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `commands`
--

DROP TABLE IF EXISTS `commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `commands` (
  `command_id` char(12) NOT NULL,
  `command_target` char(12) NOT NULL,
  `command_text` varchar(255) NOT NULL,
  `command_active` tinyint(1) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `commands`
--

LOCK TABLES `commands` WRITE;
/*!40000 ALTER TABLE `commands` DISABLE KEYS */;
/*!40000 ALTER TABLE `commands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mazes`
--

DROP TABLE IF EXISTS `mazes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mazes` (
  `maze_id` char(12) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `maze_filename` varchar(55) DEFAULT NULL,
  `maze_width` int(11) DEFAULT NULL,
  `maze_depth` int(11) NOT NULL,
  `shortest_path` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mazes`
--

LOCK TABLES `mazes` WRITE;
/*!40000 ALTER TABLE `mazes` DISABLE KEYS */;
/*!40000 ALTER TABLE `mazes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nets`
--

DROP TABLE IF EXISTS `nets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nets` (
  `net_id` char(12) COLLATE latin1_general_ci NOT NULL,
  `score` decimal(10,0) DEFAULT NULL,
  `evolves` decimal(10,0) DEFAULT NULL,
  `filename` varchar(55) CHARACTER SET latin1 COLLATE latin1_general_cs DEFAULT NULL,
  `method` varchar(55) COLLATE latin1_general_ci DEFAULT NULL,
  `logic_count` int(11) DEFAULT NULL,
  `memory_count` int(11) DEFAULT NULL,
  `thresholds` tinyint(1) DEFAULT NULL,
  `species` char(63) COLLATE latin1_general_ci DEFAULT NULL,
  `instance` longblob DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`net_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nets`
--

LOCK TABLES `nets` WRITE;
/*!40000 ALTER TABLE `nets` DISABLE KEYS */;
/*!40000 ALTER TABLE `nets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `panellists`
--

DROP TABLE IF EXISTS `panellists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `panellists` (
  `panellist_id` char(12) NOT NULL,
  `panel_id` char(12) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `player_id` char(12) NOT NULL,
  `player_instance` longblob NOT NULL,
  PRIMARY KEY (`panellist_id`,`panel_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `panellists`
--

LOCK TABLES `panellists` WRITE;
/*!40000 ALTER TABLE `panellists` DISABLE KEYS */;
INSERT INTO `panellists` VALUES ('PNST00000003','PANL00000001',3,'RBOT00000003','€(crobots_v04\nRobotPlayerX\nq\0oq}q(UlevelqUAqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player XqU\nrobot_descq	UPlays in preferred slotq\nUidqURBOT00000003qub.'),('PNST00000004','PANL00000001',6,'RBOT00000004','€(crobots_v04\nRobotPlayerA\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player AqU\nrobot_descq	U/Plays in column with most consecutives for selfq\nUidqURBOT00000004qub.'),('PNST00000005','PANL00000001',7,'RBOT00000005','€(crobots_v04\nRobotPlayerB\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player BqU\nrobot_descq	U1Plays in column with most consecutives for eitherq\nUidqURBOT00000005qub.'),('PNST00000006','PANL00000001',9,'RBOT00000006','€(crobots_v04\nRobotPlayerC\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player CqU\nrobot_descq	U1Plays in column with most consecutives for eitherq\nUidqURBOT00000006qub.'),('PNST00000007','PANL00000001',4,'RBOT00000007','€(crobots_v04\nRobotPlayerT\nq\0oq}q(UlevelqUAqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player TqU\nrobot_descq	UPlays in column 4q\nUidqURBOT00000007qub.');
/*!40000 ALTER TABLE `panellists` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `panels`
--

DROP TABLE IF EXISTS `panels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `panels` (
  `panel_id` char(12) COLLATE latin1_general_ci NOT NULL,
  `panel_desc` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `survival_score` int(11) NOT NULL,
  `lowest_acceptable_score` int(11) NOT NULL,
  PRIMARY KEY (`panel_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `panels`
--

LOCK TABLES `panels` WRITE;
/*!40000 ALTER TABLE `panels` DISABLE KEYS */;
INSERT INTO `panels` VALUES ('PANL00000001','First Panel',1,3);
/*!40000 ALTER TABLE `panels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parameters`
--

DROP TABLE IF EXISTS `parameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parameters` (
  `parm_index` varchar(63) NOT NULL,
  `parm_value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`parm_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parameters`
--

LOCK TABLES `parameters` WRITE;
/*!40000 ALTER TABLE `parameters` DISABLE KEYS */;
INSERT INTO `parameters` VALUES ('CURRENT_PANEL','PANL00000001');
/*!40000 ALTER TABLE `parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `results` (
  `result_id` char(12) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `winner` varchar(65) DEFAULT NULL,
  `loser` varchar(65) DEFAULT NULL,
  `who_winner` int(11) DEFAULT NULL,
  `game_moves` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`result_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES ('RSLT00000001','2019-10-09 15:36:02','col','RBOT00000007',0,'443424441'),('RSLT00000002','2019-10-09 15:51:34','vczx','RBOT00000003',0,'54544363525'),('RSLT00000003','2019-10-09 15:52:00','RBOT00000003','vczx',1,'5454436352554545364636274'),('RSLT00000004','2019-10-09 16:09:30','Col','RBOT00000006',0,'4344322151356761122');
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `robots`
--

DROP TABLE IF EXISTS `robots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `robots` (
  `robot_id` char(12) COLLATE latin1_general_cs NOT NULL,
  `robot_name` varchar(63) COLLATE latin1_general_cs DEFAULT NULL,
  `robot_instance` blob DEFAULT NULL,
  `robot_desc` text COLLATE latin1_general_cs DEFAULT NULL,
  `robot_level` char(1) COLLATE latin1_general_cs DEFAULT NULL,
  `robot_score` int(11) DEFAULT NULL,
  PRIMARY KEY (`robot_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `robots`
--

LOCK TABLES `robots` WRITE;
/*!40000 ALTER TABLE `robots` DISABLE KEYS */;
INSERT INTO `robots` VALUES ('RBOT00000003','Robot Player X','€(crobots_v04\nRobotPlayerX\nq\0oq}q(UlevelqUAqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player XqU\nrobot_descq	UPlays in preferred slotq\nUidqURBOT00000003qub.','Plays in preferred slot','A',0),('RBOT00000004','Robot Player A','€(crobots_v04\nRobotPlayerA\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player AqU\nrobot_descq	U/Plays in column with most consecutives for selfq\nUidqURBOT00000004qub.','Plays in column with most consecutives for self','B',0),('RBOT00000005','Robot Player B','€(crobots_v04\nRobotPlayerB\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player BqU\nrobot_descq	U1Plays in column with most consecutives for eitherq\nUidqURBOT00000005qub.','Plays in column with most consecutives for either','B',0),('RBOT00000006','Robot Player C','€(crobots_v04\nRobotPlayerC\nq\0oq}q(UlevelqUBqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player CqU\nrobot_descq	U1Plays in column with most consecutives for eitherq\nUidqURBOT00000006qub.','Plays in column with most consecutives for either','B',0),('RBOT00000007','Robot Player T','€(crobots_v04\nRobotPlayerT\nq\0oq}q(UlevelqUAqUdefaultqKUscoreqK\0U\nrobot_nameqURobot Player TqU\nrobot_descq	UPlays in column 4q\nUidqURBOT00000007qub.','Plays in column 4','A',0);
/*!40000 ALTER TABLE `robots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `serial_nos`
--

DROP TABLE IF EXISTS `serial_nos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `serial_nos` (
  `object_type` char(4) COLLATE latin1_general_ci NOT NULL,
  `last_no_used` bigint(20) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `serial_nos`
--

LOCK TABLES `serial_nos` WRITE;
/*!40000 ALTER TABLE `serial_nos` DISABLE KEYS */;
INSERT INTO `serial_nos` VALUES ('RBOT',7),('GAME',9),('PNST',7),('RSLT',4);
/*!40000 ALTER TABLE `serial_nos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `switches`
--

DROP TABLE IF EXISTS `switches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `switches` (
  `switch_name` char(4) NOT NULL,
  `switch_state` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `switches`
--

LOCK TABLES `switches` WRITE;
/*!40000 ALTER TABLE `switches` DISABLE KEYS */;
/*!40000 ALTER TABLE `switches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `test` (
  `fdsfdsa` int(11) NOT NULL,
  `fdsfd` int(11) NOT NULL,
  `fdsaa` int(11) NOT NULL,
  `fdsaffff` int(11) NOT NULL,
  PRIMARY KEY (`fdsfdsa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
INSERT INTO `test` VALUES (43,43,23,23);
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `variegation_sessions`
--

DROP TABLE IF EXISTS `variegation_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variegation_sessions` (
  `session_id` char(12) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `available` tinyint(1) NOT NULL,
  `parent_net` char(12) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
  `parent_score` int(11) DEFAULT NULL,
  `species` char(63) NOT NULL,
  PRIMARY KEY (`session_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `variegation_sessions`
--

LOCK TABLES `variegation_sessions` WRITE;
/*!40000 ALTER TABLE `variegation_sessions` DISABLE KEYS */;
/*!40000 ALTER TABLE `variegation_sessions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-09 17:12:28
