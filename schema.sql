CREATE DATABASE watermelon CHARACTER SET utf8mb4;

CREATE TABLE watermelon.user(
    id BIGINT UNSIGNED UNIQUE NOT NULL,
    email VARCHAR(64) UNIQUE NOT NULL,
    register_time TIMESTAMP NOT NULL,
    -- password related
    salt BINARY(16) NOT NULL, -- 16 byte is recommanded by scrypt
    password_encrypted BINARY(64) NOT NULL, -- python scrypt dklen default
    PRIMARY KEY(id)
);

CREATE TABLE watermelon.session(
    id BIGINT UNSIGNED UNIQUE NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    ip0 TINYINT UNSIGNED NOT NULL,
    ip1 TINYINT UNSIGNED NOT NULL,
    ip2 TINYINT UNSIGNED NOT NULL,
    ip3 TINYINT UNSIGNED NOT NULL,
    -- e.g. 192.168.1.255: ip0 = 192, ip1 = 168, ip2 = 1, ip3 = 255
    expire_time TIMESTAMP NOT NULL,
    PRIMARY KEY(id, user_id),
    FOREIGN KEY(user_id) REFERENCES watermelon.user(id) ON DELETE CASCADE
);
