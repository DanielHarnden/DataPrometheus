-- MySQL dump 10.13  Distrib 8.0.19, for osx10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: world_x
-- ------------------------------------------------------
-- Server version	8.0.19-debug

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @old_autocommit=@@autocommit;

--
-- Current Database: `world_x`
--

/*!40000 DROP DATABASE IF EXISTS `world_x`*/;

CREATE DATABASE `world_x` DEFAULT CHARACTER SET utf8mb4;

USE `world_x`;

--
-- Table structure for table `city`
--

DROP TABLE IF EXISTS `city`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `city` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` char(35) NOT NULL DEFAULT '',
  `CountryCode` char(3) NOT NULL DEFAULT '',
  `District` char(20) NOT NULL DEFAULT '',
  `Info` json DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `city`
--
-- ORDER BY:  `ID`

set autocommit=0;
INSERT INTO `city` VALUES (1,'Kabul','AFG','Kabol','{\"Population\": 1780000}');
INSERT INTO `city` VALUES (2,'Qandahar','AFG','Qandahar','{\"Population\": 237500}');
INSERT INTO `city` VALUES (3,'Herat','AFG','Herat','{\"Population\": 186800}');
INSERT INTO `city` VALUES (4,'Mazar-e-Sharif','AFG','Balkh','{\"Population\": 127800}');
INSERT INTO `city` VALUES (5,'Amsterdam','NLD','Noord-Holland','{\"Population\": 731200}');
INSERT INTO `city` VALUES (6,'Rotterdam','NLD','Zuid-Holland','{\"Population\": 593321}');
INSERT INTO `city` VALUES (7,'Haag','NLD','Zuid-Holland','{\"Population\": 440900}');
INSERT INTO `city` VALUES (8,'Utrecht','NLD','Utrecht','{\"Population\": 234323}');
INSERT INTO `city` VALUES (9,'Eindhoven','NLD','Noord-Brabant','{\"Population\": 201843}');
INSERT INTO `city` VALUES (10,'Tilburg','NLD','Noord-Brabant','{\"Population\": 193238}');
INSERT INTO `city` VALUES (11,'Groningen','NLD','Groningen','{\"Population\": 172701}');
INSERT INTO `city` VALUES (12,'Breda','NLD','Noord-Brabant','{\"Population\": 160398}');
INSERT INTO `city` VALUES (13,'Apeldoorn','NLD','Gelderland','{\"Population\": 153491}');
INSERT INTO `city` VALUES (14,'Nijmegen','NLD','Gelderland','{\"Population\": 152463}');
INSERT INTO `city` VALUES (15,'Enschede','NLD','Overijssel','{\"Population\": 149544}');
INSERT INTO `city` VALUES (16,'Haarlem','NLD','Noord-Holland','{\"Population\": 148772}');
INSERT INTO `city` VALUES (17,'Almere','NLD','Flevoland','{\"Population\": 142465}');
INSERT INTO `city` VALUES (18,'Arnhem','NLD','Gelderland','{\"Population\": 138020}');
INSERT INTO `city` VALUES (19,'Zaanstad','NLD','Noord-Holland','{\"Population\": 135621}');
INSERT INTO `city` VALUES (20,'´s-Hertogenbosch','NLD','Noord-Brabant','{\"Population\": 129170}');
INSERT INTO `city` VALUES (21,'Amersfoort','NLD','Utrecht','{\"Population\": 126270}');
INSERT INTO `city` VALUES (22,'Maastricht','NLD','Limburg','{\"Population\": 122087}');
INSERT INTO `city` VALUES (23,'Dordrecht','NLD','Zuid-Holland','{\"Population\": 119811}');
INSERT INTO `city` VALUES (24,'Leiden','NLD','Zuid-Holland','{\"Population\": 117196}');
commit;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `Code` char(3) NOT NULL DEFAULT '',
  `Name` char(52) NOT NULL DEFAULT '',
  `Capital` int DEFAULT NULL,
  `Code2` char(2) NOT NULL DEFAULT '',
  PRIMARY KEY (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--
-- ORDER BY:  `Code`

set autocommit=0;
INSERT INTO `country` VALUES ('ABW','Aruba',129,'AW');
INSERT INTO `country` VALUES ('AFG','Afghanistan',1,'AF');
INSERT INTO `country` VALUES ('AGO','Angola',56,'AO');
INSERT INTO `country` VALUES ('AIA','Anguilla',62,'AI');
INSERT INTO `country` VALUES ('ALB','Albania',34,'AL');
commit;

--
-- Table structure for table `countryinfo`
--

DROP TABLE IF EXISTS `countryinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countryinfo` (
  `doc` json DEFAULT NULL,
  `_id` varbinary(32) GENERATED ALWAYS AS (json_unquote(json_extract(`doc`,_utf8mb4'$._id'))) STORED NOT NULL,
  `_json_schema` json GENERATED ALWAYS AS (_utf8mb4'{"type":"object"}') VIRTUAL,
  PRIMARY KEY (`_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countryinfo`
--
-- ORDER BY:  `_id`

set autocommit=0;
INSERT INTO `countryinfo` (`doc`) VALUES ('{\"GNP\": 828, \"_id\": \"00005de917d80000000000000000\", \"Code\": \"ABW\", \"Name\": \"Aruba\", \"IndepYear\": null, \"geography\": {\"Region\": \"Caribbean\", \"Continent\": \"North America\", \"SurfaceArea\": 193}, \"government\": {\"HeadOfState\": \"Beatrix\", \"GovernmentForm\": \"Nonmetropolitan Territory of The Netherlands\"}, \"demographics\": {\"Population\": 103000, \"LifeExpectancy\": 78.4000015258789}}');
INSERT INTO `countryinfo` (`doc`) VALUES ('{\"GNP\": 5976, \"_id\": \"00005de917d80000000000000001\", \"Code\": \"AFG\", \"Name\": \"Afghanistan\", \"IndepYear\": 1919, \"geography\": {\"Region\": \"Southern and Central Asia\", \"Continent\": \"Asia\", \"SurfaceArea\": 652090}, \"government\": {\"HeadOfState\": \"Mohammad Omar\", \"GovernmentForm\": \"Islamic Emirate\"}, \"demographics\": {\"Population\": 22720000, \"LifeExpectancy\": 45.900001525878906}}');
INSERT INTO `countryinfo` (`doc`) VALUES ('{\"GNP\": 6648, \"_id\": \"00005de917d80000000000000002\", \"Code\": \"AGO\", \"Name\": \"Angola\", \"IndepYear\": 1975, \"geography\": {\"Region\": \"Central Africa\", \"Continent\": \"Africa\", \"SurfaceArea\": 1246700}, \"government\": {\"HeadOfState\": \"José Eduardo dos Santos\", \"GovernmentForm\": \"Republic\"}, \"demographics\": {\"Population\": 12878000, \"LifeExpectancy\": 38.29999923706055}}');
commit;

--
-- Table structure for table `countrylanguage`
--

DROP TABLE IF EXISTS `countrylanguage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `countrylanguage` (
  `CountryCode` char(3) NOT NULL DEFAULT '',
  `Language` char(30) NOT NULL DEFAULT '',
  `IsOfficial` enum('T','F') NOT NULL DEFAULT 'F',
  `Percentage` decimal(4,1) NOT NULL DEFAULT '0.0',
  PRIMARY KEY (`CountryCode`,`Language`),
  KEY `CountryCode` (`CountryCode`),
  CONSTRAINT `countrylanguage_ibfk_1` FOREIGN KEY (`CountryCode`) REFERENCES `country` (`Code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `countrylanguage`
--
-- ORDER BY:  `CountryCode`,`Language`

set autocommit=0;
INSERT INTO `countrylanguage` VALUES ('ABW','Dutch','T',5.3);
INSERT INTO `countrylanguage` VALUES ('ABW','English','F',9.5);
INSERT INTO `countrylanguage` VALUES ('ABW','Papiamento','F',76.7);
INSERT INTO `countrylanguage` VALUES ('ABW','Spanish','F',7.4);
INSERT INTO `countrylanguage` VALUES ('AFG','Balochi','F',0.9);
INSERT INTO `countrylanguage` VALUES ('AFG','Dari','T',32.1);
INSERT INTO `countrylanguage` VALUES ('AFG','Pashto','T',52.4);
INSERT INTO `countrylanguage` VALUES ('AFG','Turkmenian','F',1.9);
INSERT INTO `countrylanguage` VALUES ('AFG','Uzbek','F',8.8);
INSERT INTO `countrylanguage` VALUES ('AGO','Ambo','F',2.4);
INSERT INTO `countrylanguage` VALUES ('AGO','Chokwe','F',4.2);
INSERT INTO `countrylanguage` VALUES ('AGO','Kongo','F',13.2);
INSERT INTO `countrylanguage` VALUES ('AGO','Luchazi','F',2.4);
INSERT INTO `countrylanguage` VALUES ('AGO','Luimbe-nganguela','F',5.4);
INSERT INTO `countrylanguage` VALUES ('AGO','Luvale','F',3.6);
INSERT INTO `countrylanguage` VALUES ('AGO','Mbundu','F',21.6);
INSERT INTO `countrylanguage` VALUES ('AGO','Nyaneka-nkhumbi','F',5.4);
INSERT INTO `countrylanguage` VALUES ('AGO','Ovimbundu','F',37.2);
INSERT INTO `countrylanguage` VALUES ('AIA','English','T',0.0);
INSERT INTO `countrylanguage` VALUES ('ALB','Albaniana','T',97.9);
INSERT INTO `countrylanguage` VALUES ('ALB','Greek','F',1.8);
INSERT INTO `countrylanguage` VALUES ('ALB','Macedonian','F',0.1);
INSERT INTO `countrylanguage` VALUES ('AND','Catalan','T',32.3);
INSERT INTO `countrylanguage` VALUES ('AND','French','F',6.2);
commit;

--
-- Dumping events for database 'world_x'
--

--
-- Dumping routines for database 'world_x'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
SET autocommit=@old_autocommit;

-- Dump completed on 2020-01-22  9:58:16
