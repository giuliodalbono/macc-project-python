CREATE TABLE user (
  uid VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  username VARCHAR(255) NOT NULL,
  creation_time DATETIME NOT NULL DEFAULT NOW(),
  last_update DATETIME NOT NULL DEFAULT NOW(),
  INDEX `user_idx_email` (email),
  INDEX `user_idx_username` (username),
  INDEX `user_idx_last_update` (last_update)
);

CREATE TABLE chat (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  is_public tinyint NOT NULL default 0,
  user_id VARCHAR(255) NOT NULL,
  creation_time DATETIME NOT NULL DEFAULT NOW(),
  last_update DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES user (uid),
  INDEX `chat_idx_name` (name),
  INDEX `chat_idx_last_update` (last_update)
);

CREATE TABLE message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  message LONGTEXT NOT NULL,
  translation LONGTEXT NOT NULL,
  city VARCHAR(255),
  chat_id BIGINT NOT NULL,
  creation_time DATETIME NOT NULL DEFAULT NOW(),
  last_update DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (chat_id) REFERENCES chat (id),
  INDEX `message_idx_last_update` (last_update)
);

CREATE TABLE comment (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  message LONGTEXT NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  chat_id BIGINT NOT NULL,
  creation_time DATETIME NOT NULL DEFAULT NOW(),
  last_update DATETIME NOT NULL DEFAULT NOW(),
  FOREIGN KEY (user_id) REFERENCES user (uid),
  FOREIGN KEY (chat_id) REFERENCES chat (id),
  INDEX `comment_idx_last_update` (last_update)
);