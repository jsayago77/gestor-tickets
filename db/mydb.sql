-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.11.6-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.3.0.6589
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping data for table mydb.cliente: ~1 rows (approximately)
INSERT IGNORE INTO `cliente` (`id_cliente`, `cedula`, `nombre`, `correo`, `contrasena`, `telefono`) VALUES
	(1, '27146763', 'luis castro', 'jesucristo@mail.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi', '04122342343');

-- Dumping data for table mydb.detalle_factura: ~1 rows (approximately)
INSERT IGNORE INTO `detalle_factura` (`id`, `id_factura`, `id_producto`, `cantidad`, `precio_unitario`) VALUES
	(1, 1, 5, 1, 95);

-- Dumping data for table mydb.empleado: ~6 rows (approximately)
INSERT IGNORE INTO `empleado` (`id_empleado`, `cedula`, `nombre`, `rol`, `telefono`, `correo`, `contrasena`) VALUES
	(1, '12345678', 'jorge', 'asistente', '0412231342', 'jorge@mail.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi'),
	(2, '123456789', 'Michael Kim', 'Gerente', '555-1111', 'michaelkim@example.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi'),
	(3, '987654321', 'Sarah Chen', 'Vendedor', '555-2222', 'sarahchen@example.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi'),
	(4, '567890123', 'Alex Wong', 'Técnico', '555-3333', 'alexwong@example.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi'),
	(5, '901234567', 'Laura Ramirez', 'Contador', '555-4444', 'lauraramirez@example.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi'),
	(6, '345678901', 'Carlos Lopez', 'Recepcionista', '555-5555', 'carloslopez@example.com', '$2b$12$7/z99buGdA.DW75Rg26zxu5Byc8xkMziSbDiLAuFIhlaeT7WolFMi');

-- Dumping data for table mydb.factura: ~1 rows (approximately)
INSERT IGNORE INTO `factura` (`id`, `id_cliente`, `fecha_emision`, `total`, `status`) VALUES
	(1, 1, '2024-05-06 20:11:15', 100, 'PAGADA');

-- Dumping data for table mydb.garantia: ~0 rows (approximately)

-- Dumping data for table mydb.historial_ticket: ~0 rows (approximately)

-- Dumping data for table mydb.producto: ~5 rows (approximately)
INSERT IGNORE INTO `producto` (`id`, `nombre`, `modelo`, `descripcion`) VALUES
	(1, 'Laptop', 'XYZ123', 'Laptop ABC'),
	(2, 'Teléfono', 'ABC456', 'Teléfono XYZ'),
	(3, 'Mouse', 'MNO789', 'Mouse USB'),
	(4, 'Impresora', 'PQR012', 'Impresora A'),
	(5, 'Teclado', 'DEF345', 'Teclado QWERTY');

-- Dumping data for table mydb.responsable_ticket: ~1 rows (approximately)
INSERT IGNORE INTO `responsable_ticket` (`id`, `id_ticket`, `id_empleado`, `fecha_asignacion`, `comentario`, `status`) VALUES
	(1, 1, 1, '2024-05-08', 'Hazte cargo', 'ABIERTO');

-- Dumping data for table mydb.ticket: ~2 rows (approximately)
INSERT IGNORE INTO `ticket` (`id`, `id_producto`, `id_cliente`, `fecha_creacion`, `fecha_cierre`, `descripcion`, `asunto`, `status`) VALUES
	(1, 5, 1, '2024-05-06', '2024-05-11', 'Saludos, el teclado no enciende cuando hago Ctrl+0.', 'Problema iluminacon', 'ABIERTO'),
	(2, 5, 1, '2024-05-06', '2024-05-11', 'A veces el cable suelta chispas', 'Problema en cable', 'ABIERTO');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
