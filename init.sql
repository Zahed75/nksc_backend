-- Initialize database
SET NAMES utf8mb4;

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS nksc_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Grant privileges (already root user, but for safety)
GRANT ALL PRIVILEGES ON nksc_db.* TO 'root'@'%';
FLUSH PRIVILEGES;

-- Set timezone if needed
SET GLOBAL time_zone = '+00:00';