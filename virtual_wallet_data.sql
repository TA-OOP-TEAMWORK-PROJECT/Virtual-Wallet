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
-- Dumping data for table `cards`
--

LOCK TABLES `cards` WRITE;
/*!40000 ALTER TABLE `cards` DISABLE KEYS */;
INSERT INTO `cards` VALUES (1,'4001919257537193','2026-05-25','Valeri Bojinov',193,1,0),(2,'5425233430109903','2028-05-26','Georgi Georgiev',903,2,0),(3,'4242424242424242','2029-05-26','Georgi Georgiev',242,2,1),(4,'4880109182236949','2028-05-29','Evtim Evtimov',242,3,0),(5,'4652334578913812','2028-05-30','Valeri Bojinov',812,1,0),(6,'5191897109171774','2029-05-30','Valeri Bojinov',774,1,1),(7,'4111111111111111','2027-06-11','Manol Hristov',777,5,0);
/*!40000 ALTER TABLE `cards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Domestic',1),(2,'Shopping',2),(3,'Credit',5);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `contact_list`
--

LOCK TABLES `contact_list` WRITE;
/*!40000 ALTER TABLE `contact_list` DISABLE KEYS */;
INSERT INTO `contact_list` VALUES (1,1,4,1),(2,4,2,2),(3,4,1,3),(4,3,1,4),(5,1,5,NULL),(6,5,6,NULL),(7,5,NULL,14),(8,2,6,NULL),(9,2,7,NULL),(10,2,8,NULL),(11,2,NULL,15);
/*!40000 ALTER TABLE `contact_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `external_user`
--

LOCK TABLES `external_user` WRITE;
/*!40000 ALTER TABLE `external_user` DISABLE KEYS */;
INSERT INTO `external_user` VALUES (1,'KIRO1BREIKA','kiro@breika.com','BG18RZBB91550123456769'),(2,'NASA','NASA@usa.com','US18RZBB91550123456769'),(3,'VIK','vik@sofiiskaobshtina@.bg','BG18RZBB91550123456767'),(4,'NAP','nap@portal.bg','BG18RZBB91650123487667'),(14,'DSK','dsk@bank.com','BG123113455124562'),(15,'FIBANK','fibank@bank.com','BGFI1231134551245');
/*!40000 ALTER TABLE `external_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,0,1.1,'confirmed',NULL,NULL,NULL,'2024-06-11',1,4,NULL,NULL),(2,0,1.1,'confirmed',NULL,NULL,NULL,'2024-06-11',1,4,NULL,NULL),(3,0,300,'confirmed',NULL,NULL,NULL,'2024-06-11',5,6,NULL,NULL),(4,0,500,'confirmed',NULL,NULL,NULL,'2024-06-11',5,1,NULL,NULL),(5,0,200,'pending',NULL,NULL,NULL,'2024-06-11',5,4,NULL,NULL),(6,0,200,'confirmed',NULL,NULL,NULL,'2024-06-11',5,NULL,7,NULL),(7,0,300,'confirmed',NULL,NULL,NULL,'2024-06-11',1,4,NULL,NULL),(8,0,50,'confirmed',NULL,NULL,NULL,'2024-06-11',2,4,NULL,NULL),(9,0,50,'confirmed',NULL,NULL,NULL,'2024-06-11',2,7,NULL,NULL),(10,0,200,'confirmed',NULL,NULL,NULL,'2024-06-11',2,6,NULL,NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ikonata','Valeri','Bojinov','ikonatar@teenproblem.com','0888445567','$2b$12$P0MT1EnGG6XVv0zW27e8qOaGa2mdvcSNcxIMU8MQ8AuPuVv02lKo6',0,'admin'),(2,'gosho123','Georgi','Georgiev','gosho123@teenproblem.com','0888445566','$2b$12$Ax.zW4.inRmzZgbC6f1jKu1TURWzYnT5rtPq1byaMgyojzcE7Naz.',0,'user'),(3,'evtim_91','Evtim','Evtimov','evtim_91@teenproblem.com','0887665544','$2b$12$B56Dw2QxxBgYWfjKhUV5juY/v2OTf6dxfJ/tDLHpQur1Jhc2YWckG',0,'user'),(4,'kiro_91','Kiril','Petrov','bat_kire@teenproblem.com','0887665344','$2b$12$9X4cDdoyWvbgQDEMFEb/iOM0NUQ/8XhGk3vmOriUIgdqGzuwlgDZK',0,'user'),(5,'manol92','Manol','Hristov','manol@teenproblem.com','0877554433','$2b$12$MgY7QSVBBlkeM.vveyawOOCWS6ufqYMsyQbL1Iw6duQiZDNY3juze',0,'user'),(6,'lolita','Lola','Murat','lola98@teenproblem.com','0999225566','$2b$12$K0MOeSmRGfQccDO5TslUNuNss8zGxFnWWLVnEY1i6aZukmzkOi8MO',0,'user'),(7,'asparuh','Asparuh','Kostadinov','puhi96@teenproblem.com','0999225546','$2b$12$pLn8YlcdkbaWFt2ESL59KONUkLavHPpFYMVJQSUIZwlj3xO98t6Fm',0,'user'),(8,'stami_baby','Stamat','Peshev','mati@teenproblem.com','0881004022','$2b$12$SGnmFzS8UCFJ7ZyNjCMS4OZoDewmg8pCIkF.j3tnYH4Nb19uVGuqG',0,'user'),(9,'bebcho_99','Georgica','Dimitrov','bebcho_99@teenproblem.com','0886871873','$2b$12$TGRqxjiKwmr/BluhB.OhNeiXzRj8oUjA1yuuv3q4pdZ0/a8PUhff2',0,'user'),(10,'sila_92','Zdravko','Jelqzkov','zdravko@teenproblem.com','0886871875','$2b$12$22KzXPLqFOC8jf6GSn9GlubkStO2qS2A..svDnfvxC7ObmqjSRKZm',0,'user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `wallet`
--

LOCK TABLES `wallet` WRITE;
/*!40000 ALTER TABLE `wallet` DISABLE KEYS */;
INSERT INTO `wallet` VALUES (1,2397.8,1),(2,1198.9,2),(3,800,3),(4,752.2,4),(5,1020,5),(6,500,6),(7,252,7),(8,800,8),(9,300,9),(10,10000,10);
/*!40000 ALTER TABLE `wallet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-11 15:37:38
