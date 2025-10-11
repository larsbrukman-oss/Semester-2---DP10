-- ========================================
-- DDL: tabeldefinities
-- ========================================
CREATE DATABASE IF NOT EXISTS LSM_treintje;
USE LSM_treintje;

-- Tabel: Locatie (Attracties)
CREATE TABLE `Locatie` (
  `locatie_id` INT NOT NULL AUTO_INCREMENT,
  `naam` VARCHAR(255) NOT NULL,
  `beschrijving` TEXT NOT NULL,
  `wachttijd` INT DEFAULT 0,
  `loc_x` INT NULL,
  `loc_y` INT NULL,
  
  PRIMARY KEY (`locatie_id`)
);

-- Tabel: QRCode
CREATE TABLE `QRCode` (
  `qr_id` INT NOT NULL AUTO_INCREMENT,
  `data` VARCHAR(255) NOT NULL,
  `datum` DATE NOT NULL,
  
  PRIMARY KEY (`qr_id`)
);

-- Tabel: Trein (een enkele parktrein)
CREATE TABLE `Trein` (
  `trein_id` INT NOT NULL AUTO_INCREMENT,
  `max_capaciteit` INT NOT NULL,
  `vertrekkend_locatie_id` INT,
  `aankomend_locatie_id` INT,
  
  PRIMARY KEY (`trein_id`),
  FOREIGN KEY `fk_trein_vertrek` (`vertrekkend_locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY `fk_trein_aankomst` (`aankomend_locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabel: Reis (check-ins bij attractie of trein)
CREATE TABLE `Reis` (
  `reis_check_id` INT NOT NULL AUTO_INCREMENT,
  `qr_id` INT NOT NULL,
  `trein_id` INT NULL,
  `locatie_id` INT NOT NULL,
  `ingecheckt` TINYINT NOT NULL,
  
  PRIMARY KEY (`reis_check_id`),
  FOREIGN KEY `fk_reis_qrcode` (`qr_id`) REFERENCES `QRCode` (`qr_id`) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY `fk_reis_trein` (`trein_id`) REFERENCES `Trein` (`trein_id`) ON UPDATE CASCADE ON DELETE SET NULL,
  FOREIGN KEY `fk_reis_locatie` (`locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabel: Reisplan (bezoekplan per QR-code)
CREATE TABLE `Reisplan` (
  `qr_id` INT NOT NULL,
  `locatie_id` INT NOT NULL,

  PRIMARY KEY (`qr_id`, `locatie_id`),
  FOREIGN KEY `fk_reisplan_qrcode` (`qr_id`) REFERENCES `QRCode` (`qr_id`) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY `fk_reisplan_locatie` (`locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabel: Reservering (alleen voor mindervalide/kinderwagen e.d.)
CREATE TABLE `Reservering` (
  `qr_id` INT NOT NULL,
  `trein_id` INT NOT NULL,
  `type_behoefte` VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (`qr_id`, `trein_id`),
  FOREIGN KEY `fk_reservering_qrcode` (`qr_id`) REFERENCES `QRCode` (`qr_id`) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY `fk_reservering_trein` (`trein_id`) REFERENCES `Trein` (`trein_id`) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Tabel: Feedback
CREATE TABLE `Feedback` (
  `feedback_id` INT NOT NULL AUTO_INCREMENT,
  `qr_code` INT NOT NULL,
  `van_locatie_id` INT NOT NULL,
  `naar_locatie_id` INT NOT NULL,
  `rating` INT NOT NULL,
  `bericht` TEXT NOT NULL,
  `verzonden_op` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`feedback_id`),
  FOREIGN KEY `fk_feedback_qr_code` (`qr_code`) REFERENCES `QRCode` (`qr_id`) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY `fk_feedback_trein_van` (`van_locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY `fk_feedback_trein_naar` (`naar_locatie_id`) REFERENCES `Locatie` (`locatie_id`) ON UPDATE CASCADE ON DELETE RESTRICT
);