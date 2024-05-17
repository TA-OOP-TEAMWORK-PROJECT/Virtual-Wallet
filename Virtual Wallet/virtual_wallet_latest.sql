CREATE DATABASE  IF NOT EXISTS `web_project` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `web_project`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: web_project
-- ------------------------------------------------------
-- Server version	11.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `description` text DEFAULT 'The title speaks for itself!',
  `last_topic` varchar(150) DEFAULT 'There are no topics on this category yet!',
  `topic_cnt` int(11) DEFAULT 0,
  `is_private` tinyint(4) NOT NULL DEFAULT 0,
  `is_locked` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'Sweet 16','attitude change',NULL,NULL,1,0),(2,'18+','adults only',NULL,NULL,1,0),(3,'Love & Robots','love in the era of ai',NULL,NULL,0,0),(4,'Misunderstood Teens','A category dedicated to parents seeking help.','There are no topics on this category yet!',0,0,0);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_access`
--

DROP TABLE IF EXISTS `category_access`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_access` (
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `can_read` tinyint(4) NOT NULL DEFAULT 1,
  `can_write` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`user_id`,`category_id`),
  KEY `fk_users_has_category_category1_idx` (`category_id`),
  KEY `fk_users_has_category_users1_idx` (`user_id`),
  CONSTRAINT `fk_users_has_category_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_category_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_access`
--

LOCK TABLES `category_access` WRITE;
/*!40000 ALTER TABLE `category_access` DISABLE KEYS */;
INSERT INTO `category_access` VALUES (2,1,1,0),(3,2,1,0),(4,1,0,0),(5,1,1,1),(6,1,1,0),(7,1,1,0);
/*!40000 ALTER TABLE `category_access` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`,`sender_id`,`receiver_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_message_users1_idx` (`sender_id`),
  KEY `fk_message_users2_idx` (`receiver_id`),
  CONSTRAINT `fk_message_users1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_message_users2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,'Nezabravke asl pls?',1,5,'2024-04-25 17:30:52'),(2,'Imash li prevoz za bala?',2,8,'2024-05-07 12:00:33'),(3,'Nqmam, kakvo predlagash?',8,2,'2024-05-07 13:22:22'),(4,'Ne razbiram kakvo me pitash?',5,1,'2024-04-25 19:00:00'),(5,'Petre, edno belotche?',1,2,'2024-03-05 20:00:43'),(6,'Utre dali shte vali, aa be mincho?',3,4,'2024-05-07 15:00:00');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reply`
--

DROP TABLE IF EXISTS `reply`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reply` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `content` text DEFAULT 'NO text',
  `likes_cnt` int(11) DEFAULT 0,
  `dislike_cnt` int(11) DEFAULT 0,
  `topic_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_Reply_Topic1_idx` (`topic_id`),
  CONSTRAINT `fk_Reply_Topic1` FOREIGN KEY (`topic_id`) REFERENCES `topic` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reply`
--

LOCK TABLES `reply` WRITE;
/*!40000 ALTER TABLE `reply` DISABLE KEYS */;
INSERT INTO `reply` VALUES (1,'2024-05-07 16:18:39','Nezabravka, what the hell dear?',NULL,NULL,3),(2,'2024-05-07 16:18:39','Petre, sina ti pak li te e vkaral v borch?',NULL,NULL,2),(3,'2024-05-07 16:18:39','Zashto, kakuv e problema? Kaji da pomognem neshu..',NULL,NULL,1);
/*!40000 ALTER TABLE `reply` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topic`
--

DROP TABLE IF EXISTS `topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `topic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(150) NOT NULL,
  `date` datetime DEFAULT NULL,
  `last_reply` longtext DEFAULT 'There are no replies, yet!',
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `best_reply` longtext DEFAULT NULL,
  `is_locked` tinyint(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `title_UNIQUE` (`title`),
  KEY `fk_Topic_Users1_idx` (`user_id`),
  KEY `fk_topic_category1_idx` (`category_id`),
  CONSTRAINT `fk_Topic_Users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_topic_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topic`
--

LOCK TABLES `topic` WRITE;
/*!40000 ALTER TABLE `topic` DISABLE KEYS */;
INSERT INTO `topic` VALUES (1,'I can\'t recognize my sister.','2023-05-22 19:00:35','There are no replies, yet!',8,1,'0',0),(2,'Effects of betting on youngsters.','2024-02-13 15:45:33','There are no replies, yet!',2,2,'0',0),(3,'Fake girlfriend or real AI partner?','2024-05-07 10:00:24','There are no replies, yet!',5,3,'0',0);
/*!40000 ALTER TABLE `topic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `email` varchar(150) NOT NULL,
  `date_of_birth` date NOT NULL,
  `hashed_password` varchar(5000) DEFAULT NULL,
  `role` varchar(10) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'gosho123','Georgi','Georgiev','georgi@teenproblem.bg','1970-01-01','$2b$12$hi6cp3C.gQVpMHsQnRe.6.Dk0A/LQzKC5IhGx36mL5cLK70trhJ0m','admin'),(2,'pesho5','Pesho','Peshev','pesho@teenproblem.bg','1980-02-02','$2b$12$5yT7mZ7R8fOAjENeY156geWWarfNKHl29plO.I8AMZK4pjyfRMSFS','user'),(3,'unufri34','Unufri','Dalgopolov','unufri@teenproblem.bg','1990-03-03','$2b$12$033En07rOs1EbE2tvsp2He2ba9x7wfQenhcnsLLAkKDKdArMGf3nm','user'),(4,'minko69','Minko','Praznikov','minko@teenproblem.bg','2000-04-04','$2b$12$C0/sFymjUscwnrCLs3CGxubxXLRg5PisdN40T0iPG0lF25EViMBdG','user'),(5,'nezabravka007','Nezabravka','Ivanov','nezabravka@teenproblem.bg','2010-05-05','$2b$12$g0Xm2o4EfzPdy1L79i57NelT2YCsJ4t/ljXxy93OOFcNjIDv0PUke','user'),(6,'evtim123','Evtim','Evtimov','evtim@teenproblem.bg','1990-05-06','$2b$12$MJXtvP9SYDv/ktilpGl1Oey0a52mOLWN1qYp8mxhzoxSUvi6ETz3y','user'),(7,'batgiorgi','Joromir','Popatanasov','joreto@teenproblem.bg','1992-08-10','$2b$12$lce9fLtzEkY5seTHrZoxB.e3U0bi6bjB8ZyYm1LCWDSXzdrR1J3tG','user'),(8,'lachena95','Luchezara','Parichkova','lucheto@teenproblem.bg','1995-11-01','$2b$12$4LyaWM5/XNzlh40hMdw9BOtPLwJ.gi6.NdWzVsqYRJy4qLqj4cBQi','user'),(16,'ikonata','Valeri','Bojinov','malkokote@teenproblem.com','1986-02-15','$2b$12$J/FOU0bI4dnS0scRswNrEud.1DvXd5TBmlMbS3.mQKE9ktfaOsdoi','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vote`
--

DROP TABLE IF EXISTS `vote`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vote` (
  `reply_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `vote` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`reply_id`,`user_id`),
  KEY `fk_reply_has_users_users1_idx` (`user_id`),
  KEY `fk_reply_has_users_reply1_idx` (`reply_id`),
  CONSTRAINT `fk_reply_has_users_reply1` FOREIGN KEY (`reply_id`) REFERENCES `reply` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_reply_has_users_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vote`
--

LOCK TABLES `vote` WRITE;
/*!40000 ALTER TABLE `vote` DISABLE KEYS */;
/*!40000 ALTER TABLE `vote` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-17 13:40:22
