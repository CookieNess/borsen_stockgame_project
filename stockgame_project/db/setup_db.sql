USE stockgamedb;

DROP TABLE IF EXISTS Tickers, Prices;

CREATE TABLE IF NOT EXISTS Tickers (
    YahooTicker VARCHAR(20),
    PRIMARY KEY (YahooTicker)
);

CREATE TABLE IF NOT EXISTS Prices (
    PriceID int NOT NULL AUTO_INCREMENT,
    YahooTicker VARCHAR(20),
    DateRecorded DATE, /*YYYY-MM-DD*/
    OpenPrice DECIMAL(10,2),
    HighPrice DECIMAL(10,2),
    LowPrice DECIMAL(10,2),
    ClosePrice DECIMAL(10,2),
    Volume int,
    PRIMARY KEY (PriceID),
    FOREIGN KEY (YahooTicker) REFERENCES Tickers(YahooTicker)
);

SELECT * FROM Tickers;
SELECT * FROM Prices
DELETE FROM Prices;

INSERT INTO Prices(LowPrice) VALUES (
    (308.54)
);