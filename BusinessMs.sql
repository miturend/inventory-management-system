CREATE TABLE Settings (
    SettingID INT PRIMARY KEY AUTO_INCREMENT,
    BusinessName VARCHAR(150) NOT NULL,
    BusinessAddress TEXT,
    Phone VARCHAR(30),
    Email VARCHAR(100),
    CurrencySymbol VARCHAR(10) DEFAULT '₦',
    ReceiptFooter TEXT,
    LowStockThreshold INT DEFAULT 10,
    UpdatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);