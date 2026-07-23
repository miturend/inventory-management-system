-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: BusinessMs
-- ------------------------------------------------------
-- Server version	8.0.46

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

--
-- Table structure for table `activitylogs`
--

DROP TABLE IF EXISTS `activitylogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activitylogs` (
  `LogID` int NOT NULL AUTO_INCREMENT,
  `UserID` int DEFAULT NULL,
  `Action` varchar(255) DEFAULT NULL,
  `CreatedDate` datetime DEFAULT CURRENT_TIMESTAMP,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`LogID`),
  KEY `UserID` (`UserID`),
  CONSTRAINT `activitylogs_ibfk_1` FOREIGN KEY (`UserID`) REFERENCES `users` (`UserID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activitylogs`
--

LOCK TABLES `activitylogs` WRITE;
/*!40000 ALTER TABLE `activitylogs` DISABLE KEYS */;
INSERT INTO `activitylogs` VALUES (1,1,'ADD PRODUCT','2026-07-21 23:54:18','Added product: Milk stick'),(2,1,'EDIT PRODUCT','2026-07-21 23:54:39','Updated product: Milk stick'),(3,1,'DELETE PRODUCT','2026-07-21 23:54:45','Deleted product: Milk stick'),(4,1,'DATABASE BACKUP','2026-07-22 00:48:44','Created backup: backup_20260722_004843.sql'),(5,1,'DELETE BACKUP','2026-07-22 00:54:41','Deleted backup: backup_20260722_004843.sql'),(6,1,'DATABASE BACKUP','2026-07-22 01:02:57','Created backup: backup_20260722_010256.sql'),(7,1,'RESTORE DATABASE','2026-07-22 01:05:41','Restored backup: backup_20260722_003929.sql');
/*!40000 ALTER TABLE `activitylogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `companysettings`
--

DROP TABLE IF EXISTS `companysettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `companysettings` (
  `SettingID` int NOT NULL AUTO_INCREMENT,
  `BusinessName` varchar(150) DEFAULT NULL,
  `Address` text,
  `Phone` varchar(30) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Logo` varchar(255) DEFAULT NULL,
  `Currency` varchar(10) DEFAULT '₦',
  `LowStockLevel` int DEFAULT '10',
  `ReceiptFooter` text,
  PRIMARY KEY (`SettingID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `companysettings`
--

LOCK TABLES `companysettings` WRITE;
/*!40000 ALTER TABLE `companysettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `companysettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `currentstock`
--

DROP TABLE IF EXISTS `currentstock`;
/*!50001 DROP VIEW IF EXISTS `currentstock`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `currentstock` AS SELECT 
 1 AS `ProductID`,
 1 AS `ProductName`,
 1 AS `Stock`,
 1 AS `SellingPrice`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `CustomerName` varchar(100) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Mary','08011111111','Abuja'),(2,'Emmanuel Samuel','91160134185','Lagos');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `expensereport`
--

DROP TABLE IF EXISTS `expensereport`;
/*!50001 DROP VIEW IF EXISTS `expensereport`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `expensereport` AS SELECT 
 1 AS `ExpenseID`,
 1 AS `ExpenseDate`,
 1 AS `Description`,
 1 AS `Category`,
 1 AS `Amount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `ExpenseID` int NOT NULL AUTO_INCREMENT,
  `ExpenseDate` date NOT NULL,
  `Description` varchar(255) NOT NULL,
  `Category` varchar(100) DEFAULT NULL,
  `Amount` decimal(12,2) NOT NULL,
  PRIMARY KEY (`ExpenseID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `productid` int NOT NULL AUTO_INCREMENT,
  `productname` varchar(100) NOT NULL,
  `sellingprice` decimal(10,2) NOT NULL,
  `stock` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Milk Biscuit',35000.00,108.00),(2,'Soda Cracker',33000.00,70.00),(3,'Chocolate Biscuite',4000.00,113.00),(4,'Milk stick',25000.00,20.00);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `profitreport`
--

DROP TABLE IF EXISTS `profitreport`;
/*!50001 DROP VIEW IF EXISTS `profitreport`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `profitreport` AS SELECT 
 1 AS `ProductName`,
 1 AS `Quantity`,
 1 AS `SellingPrice`,
 1 AS `CostPrice`,
 1 AS `Profit`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `purchaseitems`
--

DROP TABLE IF EXISTS `purchaseitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchaseitems` (
  `PurchaseItemID` int NOT NULL AUTO_INCREMENT,
  `PurchaseID` int NOT NULL,
  `ProductID` int NOT NULL,
  `Quantity` decimal(10,1) NOT NULL,
  `UnitCost` decimal(10,2) NOT NULL,
  `TotalAmount` decimal(12,2) GENERATED ALWAYS AS ((`Quantity` * `UnitCost`)) STORED,
  PRIMARY KEY (`PurchaseItemID`),
  KEY `PurchaseID` (`PurchaseID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `purchaseitems_ibfk_1` FOREIGN KEY (`PurchaseID`) REFERENCES `purchases` (`PurchaseID`),
  CONSTRAINT `purchaseitems_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchaseitems`
--

LOCK TABLES `purchaseitems` WRITE;
/*!40000 ALTER TABLE `purchaseitems` DISABLE KEYS */;
INSERT INTO `purchaseitems` (`PurchaseItemID`, `PurchaseID`, `ProductID`, `Quantity`, `UnitCost`) VALUES (7,2,1,60.0,30000.00),(8,2,2,40.0,28500.00),(9,4,2,30.0,30000.00),(10,4,1,50.0,42000.00),(11,5,3,55.0,3000.00),(12,5,1,5.0,30000.00);
/*!40000 ALTER TABLE `purchaseitems` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_AfterPurchaseItem` AFTER INSERT ON `purchaseitems` FOR EACH ROW BEGIN
    UPDATE products
    SET Stock = Stock + NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Temporary view structure for view `purchasereport`
--

DROP TABLE IF EXISTS `purchasereport`;
/*!50001 DROP VIEW IF EXISTS `purchasereport`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `purchasereport` AS SELECT 
 1 AS `PurchaseID`,
 1 AS `PurchaseDate`,
 1 AS `InvoiceNumber`,
 1 AS `SupplierName`,
 1 AS `ProductName`,
 1 AS `Quantity`,
 1 AS `UnitCost`,
 1 AS `TotalAmount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `PurchaseID` int NOT NULL AUTO_INCREMENT,
  `SupplierID` int NOT NULL,
  `PurchaseDate` date NOT NULL,
  `InvoiceNumber` varchar(50) DEFAULT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PurchaseID`),
  KEY `SupplierID` (`SupplierID`),
  CONSTRAINT `purchases_ibfk_1` FOREIGN KEY (`SupplierID`) REFERENCES `suppliers` (`SupplierID`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
INSERT INTO `purchases` VALUES (2,1,'2026-07-20','INV-002','Test Purchase'),(3,1,'2026-07-21','asdlhcbLJBH','not paid fully yet'),(4,1,'2026-07-21','inv 003','omo men'),(5,1,'2026-07-21','inv 004','testing');
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saleitems`
--

DROP TABLE IF EXISTS `saleitems`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saleitems` (
  `SaleItemID` int NOT NULL AUTO_INCREMENT,
  `SaleID` int NOT NULL,
  `ProductID` int NOT NULL,
  `Quantity` decimal(10,1) NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  `TotalAmount` decimal(12,2) GENERATED ALWAYS AS ((`Quantity` * `UnitPrice`)) STORED,
  PRIMARY KEY (`SaleItemID`),
  KEY `SaleID` (`SaleID`),
  KEY `ProductID` (`ProductID`),
  CONSTRAINT `saleitems_ibfk_1` FOREIGN KEY (`SaleID`) REFERENCES `sales` (`SaleID`),
  CONSTRAINT `saleitems_ibfk_2` FOREIGN KEY (`ProductID`) REFERENCES `products` (`productid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saleitems`
--

LOCK TABLES `saleitems` WRITE;
/*!40000 ALTER TABLE `saleitems` DISABLE KEYS */;
INSERT INTO `saleitems` (`SaleItemID`, `SaleID`, `ProductID`, `Quantity`, `UnitPrice`) VALUES (1,1,1,2.0,35000.00),(3,1,1,5.0,35000.00),(4,2,3,30.0,4000.00),(5,2,3,1.0,4000.00);
/*!40000 ALTER TABLE `saleitems` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_CheckStockBeforeSale` BEFORE INSERT ON `saleitems` FOR EACH ROW BEGIN
    DECLARE currentStock DECIMAL(10,2);

    SELECT Stock
    INTO currentStock
    FROM products
    WHERE ProductID = NEW.ProductID;

    IF currentStock < NEW.Quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Not enough stock available';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_AfterSaleItem` AFTER INSERT ON `saleitems` FOR EACH ROW BEGIN
    UPDATE products
    SET Stock = Stock - NEW.Quantity
    WHERE ProductID = NEW.ProductID;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `SaleID` int NOT NULL AUTO_INCREMENT,
  `CustomerID` int NOT NULL,
  `SaleDate` date NOT NULL,
  `Notes` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SaleID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `customers` (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,1,'2026-07-20','First sale'),(2,2,'2026-07-21',''),(3,2,'2026-07-21','');
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `salesreport`
--

DROP TABLE IF EXISTS `salesreport`;
/*!50001 DROP VIEW IF EXISTS `salesreport`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `salesreport` AS SELECT 
 1 AS `SaleID`,
 1 AS `SaleDate`,
 1 AS `CustomerName`,
 1 AS `ProductName`,
 1 AS `Quantity`,
 1 AS `UnitPrice`,
 1 AS `TotalAmount`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `SupplierID` int NOT NULL AUTO_INCREMENT,
  `SupplierName` varchar(100) NOT NULL,
  `Phone` varchar(20) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'olam distributors','9160134185','lagos');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(50) NOT NULL,
  `PasswordHash` varchar(255) NOT NULL,
  `Role` enum('Admin','Manager','Cashier') DEFAULT 'Cashier',
  `CreatedDate` date DEFAULT (curdate()),
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$IDsQvtOodPvWDDKI$9578a75255a699f5bab4f854e32f0dd87bf7e3d8aba010c1b47d5591d0c030e0f0930b3568211e5dcd27bcbb1d47ce5fb53a94b7b8665ba7c27abef3adab7b4a','Admin','2026-07-21'),(2,'Eze','scrypt:32768:8:1$0eo5QQTFX6GO0ekm$fd07bce33c6bbc861d420130a33a7f9b9cf45026da19d1b11743d21210178b468f94d246e285ff56f8d76eea4dd054f45781f0ce157414573f7676db88363f9f','Manager','2026-07-21'),(3,'john','scrypt:32768:8:1$K8gHs0CUeLQDQXZE$9040e04fbb89d2c6f204e4a053ac2a680b5a3165b7ea495c19cebf9a67a82d442c642e144efb42e7b15d916e01426af2ef0268eb4e19a00867910da925245432','Manager','2026-07-21'),(4,'Lavish','scrypt:32768:8:1$XN1PhBE3aVqu8Zah$1230b4f6b050f45686622585deb5678496ef9f4c3efb78b202771f8928d371abf4b5b9a65c15bb548e3b753ddfb67e134427fd6b23d4712ca1e1369704c2ee11','Manager','2026-07-21');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `currentstock`
--

/*!50001 DROP VIEW IF EXISTS `currentstock`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `currentstock` AS select `products`.`productid` AS `ProductID`,`products`.`productname` AS `ProductName`,`products`.`stock` AS `Stock`,`products`.`sellingprice` AS `SellingPrice` from `products` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `expensereport`
--

/*!50001 DROP VIEW IF EXISTS `expensereport`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `expensereport` AS select `expenses`.`ExpenseID` AS `ExpenseID`,`expenses`.`ExpenseDate` AS `ExpenseDate`,`expenses`.`Description` AS `Description`,`expenses`.`Category` AS `Category`,`expenses`.`Amount` AS `Amount` from `expenses` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `profitreport`
--

/*!50001 DROP VIEW IF EXISTS `profitreport`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `profitreport` AS select `pr`.`productname` AS `ProductName`,`si`.`Quantity` AS `Quantity`,`si`.`UnitPrice` AS `SellingPrice`,`pi`.`UnitCost` AS `CostPrice`,((`si`.`UnitPrice` - `pi`.`UnitCost`) * `si`.`Quantity`) AS `Profit` from ((`saleitems` `si` join `products` `pr` on((`si`.`ProductID` = `pr`.`productid`))) join `purchaseitems` `pi` on((`si`.`ProductID` = `pi`.`ProductID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `purchasereport`
--

/*!50001 DROP VIEW IF EXISTS `purchasereport`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `purchasereport` AS select `p`.`PurchaseID` AS `PurchaseID`,`p`.`PurchaseDate` AS `PurchaseDate`,`p`.`InvoiceNumber` AS `InvoiceNumber`,`s`.`SupplierName` AS `SupplierName`,`pr`.`productname` AS `ProductName`,`pi`.`Quantity` AS `Quantity`,`pi`.`UnitCost` AS `UnitCost`,`pi`.`TotalAmount` AS `TotalAmount` from (((`purchases` `p` join `suppliers` `s` on((`p`.`SupplierID` = `s`.`SupplierID`))) join `purchaseitems` `pi` on((`p`.`PurchaseID` = `pi`.`PurchaseID`))) join `products` `pr` on((`pi`.`ProductID` = `pr`.`productid`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `salesreport`
--

/*!50001 DROP VIEW IF EXISTS `salesreport`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `salesreport` AS select `s`.`SaleID` AS `SaleID`,`s`.`SaleDate` AS `SaleDate`,`c`.`CustomerName` AS `CustomerName`,`pr`.`productname` AS `ProductName`,`si`.`Quantity` AS `Quantity`,`si`.`UnitPrice` AS `UnitPrice`,`si`.`TotalAmount` AS `TotalAmount` from (((`sales` `s` join `customers` `c` on((`s`.`CustomerID` = `c`.`CustomerID`))) join `saleitems` `si` on((`s`.`SaleID` = `si`.`SaleID`))) join `products` `pr` on((`si`.`ProductID` = `pr`.`productid`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-22  1:14:35
