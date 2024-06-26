CREATE DATABASE  IF NOT EXISTS `virtual_wallet` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `virtual_wallet`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: virtual_wallet
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
-- Table structure for table `cards`
--

DROP TABLE IF EXISTS `cards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `number` varchar(16) DEFAULT NULL,
  `exp_date` date DEFAULT NULL,
  `cardholder_name` varchar(30) DEFAULT NULL,
  `cvv` int(11) DEFAULT NULL,
  `wallet_id` int(11) NOT NULL,
  `is_virtual` tinyint(4) DEFAULT 0,
  PRIMARY KEY (`id`,`wallet_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_cards_wallet1_idx` (`wallet_id`),
  CONSTRAINT `fk_cards_wallet1` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(45) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`user_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_categories_users1_idx` (`user_id`),
  CONSTRAINT `fk_categories_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contact_list`
--

DROP TABLE IF EXISTS `contact_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `contact_id` int(11) DEFAULT NULL,
  `external_user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`,`user_id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_contact_list_users1_idx` (`user_id`),
  KEY `fk_contact_list_users2_idx1` (`contact_id`),
  KEY `fk_contact_list_external_user1_idx` (`external_user_id`),
  CONSTRAINT `fk_contact_list_external_user1` FOREIGN KEY (`external_user_id`) REFERENCES `external_user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_contact_list_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_contact_list_users2` FOREIGN KEY (`contact_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `external_user`
--

DROP TABLE IF EXISTS `external_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `external_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `contact_name` varchar(100) NOT NULL,
  `contact_email` varchar(150) DEFAULT NULL,
  `iban` varchar(34) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_recurring` tinyint(4) DEFAULT 0,
  `amount` float NOT NULL,
  `status` varchar(45) DEFAULT 'pending',
  `message` text DEFAULT NULL,
  `recurring_period` int(11) DEFAULT NULL,
  `recurring_date` date DEFAULT NULL,
  `transaction_date` date DEFAULT NULL,
  `wallet_id` int(11) NOT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `contact_list_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_transactions_wallet1_idx` (`wallet_id`),
  KEY `fk_transactions_users1_idx` (`receiver_id`),
  KEY `fk_transactions_contact_list1_idx` (`contact_list_id`),
  KEY `fk_transactions_categories1_idx` (`category_id`),
  CONSTRAINT `fk_transactions_categories1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_transactions_contact_list1` FOREIGN KEY (`contact_list_id`) REFERENCES `contact_list` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_transactions_users1` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_transactions_wallet1` FOREIGN KEY (`wallet_id`) REFERENCES `wallet` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

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
  `phone_number` varchar(45) NOT NULL,
  `hashed_password` varchar(5000) DEFAULT NULL,
  `is_blocked` tinyint(4) DEFAULT 1,
  `role` varchar(10) NOT NULL DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `phone_number_UNIQUE` (`phone_number`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wallet`
--

DROP TABLE IF EXISTS `wallet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` float DEFAULT 0,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `fk_wallet_users1_idx` (`user_id`),
  CONSTRAINT `fk_wallet_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-11 11:08:20
