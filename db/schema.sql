CREATE TABLE user (
  uid VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  username VARCHAR(255) NOT NULL,
  INDEX `user_idx_email` (email),
  INDEX `user_id_username` (username)
);

CREATE TABLE chat (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  is_public tinyint NOT NULL default 0,
  user_id VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (uid),
  INDEX `chat_idx_name` (name)
);

CREATE TABLE message (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  message LONGTEXT NOT NULL,
  translation LONGTEXT NOT NULL,
  chat_id BIGINT NOT NULL,
  FOREIGN KEY (chat_id) REFERENCES chat (id)
);

CREATE TABLE comment (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  message LONGTEXT NOT NULL,
  user_id VARCHAR(255) NOT NULL,
  chat_id BIGINT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES user (uid),
  FOREIGN KEY (chat_id) REFERENCES chat (id)
);