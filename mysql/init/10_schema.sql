USE `vulshop`;

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `sessions`;

CREATE TABLE `users` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` BIGINT NOT NULL,
  `updated_at` BIGINT NOT NULL,
  `password_hash` VARCHAR(255) NOT NULL,
  `active` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4;

CREATE TABLE `products` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  `description` VARCHAR(255) NOT NULL,
  `stock` INT NOT NULL,
  `created_at` BIGINT NOT NULL,
  `updated_at` BIGINT NOT NULL,
  `active` BOOLEAN NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4;

CREATE TABLE `sessions` (
  `user_id` BIGINT NOT NULL AUTO_INCREMENT,
  `session` VARCHAR(255) NOT NULL,
  `created_at` BIGINT NOT NULL,
  `expired_at` BIGINT NOT NULL,
  PRIMARY KEY (`user_id`, `session`),
  UNIQUE KEY `session` (`session`)
) ENGINE=InnoDB DEFAULT CHARACTER SET=utf8mb4;
