DROP DATABASE IF EXISTS rbcdb;
-- CREATES THE BANK DATABASE
create database if not exists rbcdb;

use rbcdb;

-- CREATES THE CUSTOMER TABLE
use rbcdb;
DROP TABLE IF EXISTS `Customer` ;

CREATE TABLE IF NOT EXISTS `Customer` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(45) NOT NULL,
  `LastName` VARCHAR(45) NOT NULL,
  `Gender` VARCHAR(45) NOT NULL,
  `DOB` DATE NOT NULL,
  `RelationshipStatus` VARCHAR(45) NOT NULL,
  `PhoneNumber` VARCHAR(45) NOT NULL,
  `StateOfOrigin` VARCHAR(45) NOT NULL,
  `CountryOfOrigin` VARCHAR(45) NOT NULL,
  `HouseAddress` VARCHAR(45) NOT NULL,
  `Town_City` VARCHAR(45) NOT NULL,
  `CountryOfResidence` VARCHAR(45) NOT NULL,
  `PostalCode` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`)
  )
ENGINE = InnoDB;


CREATE UNIQUE INDEX `ID_UNIQUE` ON `Customer` (`ID` ASC) VISIBLE;


-- CREATES THE ACCOUNT TYPE TABLE FOR REFERENCES

DROP TABLE IF EXISTS `AccountType` ;

CREATE TABLE IF NOT EXISTS `AccountType` (
  `ID` INT NOT NULL,
  `Name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- CREATES THE ACCOUNTS TABLE


DROP TABLE IF EXISTS `Accounts` ;

CREATE TABLE IF NOT EXISTS `Accounts` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Customer_ID` INT NOT NULL,
  PRIMARY KEY (`ID`),
  CONSTRAINT `fk_Accounts_Customer1`
    FOREIGN KEY (`Customer_ID`)
    REFERENCES `Customer` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


CREATE INDEX `fk_Accounts_Customer1_idx` ON `Accounts` (`Customer_ID` ASC) VISIBLE;

-- CREATES THE ONLINE BANKING ACCOUNT TABLE

DROP TABLE IF EXISTS `OnlineBankingAcct` ;

CREATE TABLE IF NOT EXISTS `OnlineBankingAcct` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Email` VARCHAR(40) NOT NULL,
  `Password` VARCHAR(100) NOT NULL,
  `customerID`INT NOT NULL,
  `AccountsID` INT NULL,
  
  PRIMARY KEY (`ID`),
  CONSTRAINT cust_onlinebankID_fk 
  foreign key (`customerID`) references `Customer`(`ID`),
  CONSTRAINT online_accountsID_fk
  foreign key (`AccountsID`) references `Accounts`(`ID`))
  
ENGINE = InnoDB;

CREATE UNIQUE INDEX `Email_UNIQUE` ON `OnlineBankingAcct` (`Email` ASC) VISIBLE;





-- CREATES THE ACCOUNT TABLE

DROP TABLE IF EXISTS `Account` ;

CREATE TABLE IF NOT EXISTS `Account` (
  `AccountNumber` INT NOT NULL AUTO_INCREMENT,
  `Balance` DECIMAL(9,2) NOT NULL,
  `Active` TINYINT NOT NULL,
  `AccountType_ID` INT NOT NULL,
  `Accounts_ID` INT NOT NULL,
  PRIMARY KEY (`AccountNumber`),
  CONSTRAINT `fk_Account_AccountType1`
    FOREIGN KEY (`AccountType_ID`)
    REFERENCES `AccountType` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Account_Accounts1`
    FOREIGN KEY (`Accounts_ID`)
    REFERENCES `Accounts` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_Account_AccountType1_idx` ON `Account` (`AccountType_ID` ASC) VISIBLE;

CREATE INDEX `fk_Account_Accounts1_idx` ON `Account` (`Accounts_ID` ASC) VISIBLE;



-- CREATES THE TRANSACTION TABLE

DROP TABLE IF EXISTS `Transaction` ;

CREATE TABLE IF NOT EXISTS `Transaction` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `accountID` INT NOT NULL,
  `type` VARCHAR(10) NOT NULL,
  `Amount` DECIMAL(9,2) NOT NULL,
  `DateAndTime` DATE NOT NULL,
  `FromBankName` VARCHAR(45) NOT NULL,
  `FromName` VARCHAR(45) NOT NULL,
  `FromAccountNumber` VARCHAR(45) NOT NULL,
  `ToBankName` VARCHAR(45) NOT NULL,
  `ToName` VARCHAR(45) NOT NULL,
  `ToAccountNumber` VARCHAR(45) NOT NULL,
  `Status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`ID`, `accountID`),
  CONSTRAINT `fk_Transaction_Account1`
    FOREIGN KEY (`accountID`)
    REFERENCES `Account` (`Accounts_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_Transaction_Account1_idx` ON `Transaction` (`accountID` ASC) VISIBLE;


-- INSERTS REQUIRED VALUES FOR THE ACCOUNT TYPE TABLE
USE rbcdb;
INSERT INTO `AccountType` VALUES (1,'CHEQUING');
INSERT INTO `AccountType` VALUES (2, 'SAVINGS');
INSERT INTO `AccountType` VALUES (3, 'INVESTMENT');

-- CREATES THE TRIGGER FOR CREATING FINANCIAL ACCOUNT ONCE A NEW CUSTOMER IS ADDED TO THE BANK DEFAULT IS CHEQUINGS ACCOUNT CREATION
drop trigger if exists create_financial_account;

delimiter //
create trigger create_financial_account
	after insert on `Customer`
	for each row
BEGIN

	declare accountsid int;
	declare customer_id int;
	declare onlinebankid int;
	declare account_number int;
	
	select `ID` into customer_id from `Customer` where `ID` = new.`ID`;
	set accountsid = FLOOR(RAND() * (9999 - 1000 + 1)) + 1000;
	set account_number = concat(accountsid,'',FLOOR(RAND() * (9999 - 1000 + 1)) + 1000);
	
	insert into `Accounts` (`ID`,`Customer_ID`) values (accountsid,customer_id);
	insert into `Account` values (account_number,0,True,1,accountsid);
END //

delimiter ;



-- CREATES THE CUSTOMER_ACCOUNTS_ACCOUNT VIEW 
drop view if exists `Customer_Accounts_Account`;

CREATE VIEW `Customer_Accounts_Account` AS
SELECT `Customer`.`ID` , `Customer`.`LastName`, `Customer`.`PhoneNumber`, `Accounts`.`ID` as accounts_id, `Account`.`AccountNumber`, `Account`.`AccountType_ID`, `Account`.`Active`
FROM `Accounts` 
join `Account` on `Accounts`.`ID` = `Account`.`Accounts_ID`
join `Customer` on `Accounts`.`Customer_ID` = `Customer`.`ID`;

-- CREATES THE TRIGGER TO CLOSE CUSTOMER ACCOUNT AND DELETE CUSTOMER FROM THE DATABASE IF CUSTOMER WISHES TO CLOSE ACCOUNT


drop trigger if exists close_customer_account;

delimiter //
create trigger close_customer_account
	before delete on `Customer`
	for each row
BEGIN

	
	declare customer_id int;
	declare onlinebankid int default null;
    declare accountsid int;
    declare counter int default 1;
    declare accountNumber int;
    
	
    select `ID` into customer_id from `Customer` where `ID` = old.`ID`;
	select `Accounts_id` into accountsid from `Customer_Accounts_Account` where `ID` = customer_id;
    select `OnlineBankingAcct_ID` into onlinebankid from customer_accounts_account where `ID` = customer_id;
    
    delete from `Account` where `Accounts_ID` = accounts_id and `AccountType_ID` =1;
    delete from `Account` where `Accounts_ID`= accounts_id and `AccountType_ID`=2;
    delete from `Account` where `Accounts_ID`= accounts_id and `AccountType_ID` =3;
    
    delete from `Accounts` where `ID` = accountsid;
    
    
    IF onlinebankid is not null then
		delete from `OnlineBankingAcct` where `ID` = onlinebankid;
	END IF;
	
END //

delimiter ;

-- CREATES A TRIGGER TO GENERATE AN ACCOUNT NUMBER WHEN A NEW FINANCE ACCOUNT(INVESTMENT OR SAVINGS) IS CREATED FOR A CUSTOMER

drop trigger if exists generate_account_number;

delimiter //
create trigger generate_account_number
	before insert on `Account`
	for each row
BEGIN

    declare account_number int;
    
	set account_number = concat(new.`Accounts_ID`,'',FLOOR(RAND() * (9999 - 1000 + 1)) + 1000);
    set new.`AccountNumber` = account_number;
	
END //

delimiter ;

-- CREATES THE TRIGGER FOR ALL TRANSFER TRANSACTIONS TO RECORD INTO THE DATABASE

drop trigger if exists transfer_transactions;

delimiter //
create trigger transfer_transactions
	before insert on `Transaction`
	for each row
BEGIN
	declare from_accountName varchar(10);
    declare from_accttype int;
    declare to_accountName varchar(10);
    declare to_accttype int;
    declare from_balance Decimal(9,2);
    declare to_balance Decimal(9,2);
    
    
    select `AccountType_ID` into from_accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`FromAccountNumber`;
    select `Name` into from_accountName from `AccountType` where `ID` = from_accttype;
    select `AccountType_ID` into to_accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`ToAccountNumber`;
    select `Name` into to_accountName from `AccountType` where `ID` = to_accttype;
    
    select `Balance` into from_balance from `Account` where `AccountNumber` =new.`FromAccountNumber`;
    select `Balance` into to_balance from `Account` where `AccountNumber` = new.`ToAccountNumber`;
    
    
    
    
	if new.`Type` = 'TRANSFER' THEN
        set new.`Status` = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`ToBankName` = 'INTERNAL';
        set new.`FromBankName` = 'INTERNAL';
        set new.`FromName` = from_accountName;
        set new.`ToName` = to_accountName;
        update account set `Balance` = from_balance - new.`Amount` where `AccountNumber` = new.`FromAccountNumber`;
		update account set `Balance` = to_balance + new.`Amount` where `AccountNumber` = new.`ToAccountNumber`;
	end if;
    
   
END //

delimiter ;

-- CREATES THE TRIGGER FOR ALL TRANSFER DEPOSIT TRANSACTIONS TO RECORD INTO THE DATABASE

drop trigger if exists deposit_transfer_transactions;

delimiter //
create trigger deposit_transfer_transactions
	before insert on `Transaction`
	for each row
BEGIN
	declare from_accountName varchar(10);
    declare from_accttype int;
    declare to_accountName varchar(10);
    declare to_accttype int;
    
    
    
    select `AccountType_ID` into from_accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`FromAccountNumber`;
    select `Name` into from_accountName from `AccountType` where `ID` = from_accttype;
    select `AccountType_ID` into to_accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`ToAccountNumber`;
    select `Name` into to_accountName from `AccountType` where `ID` = to_accttype;
    
    
    
    
	if new.`Type` = 'T_DEPOSIT' THEN
        set new.`Status` = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`ToBankName` = 'INTERNAL';
        set new.`FromBankName` = 'INTERNAL';
        set new.`FromName` = from_accountName;
        set new.`ToName` = to_accountName;
	end if;
    
   
END //

delimiter ;



-- CREATES THE TRIGGER FOR ALL DEPOSIT TRANSACTIONS TO RECORD INTO THE DATABASE


drop trigger if exists deposit_into_account;

delimiter //
create trigger deposit_into_account
	before insert on `Transaction`
	for each row
BEGIN
	declare accountName varchar(10);
    declare accttype int;
    
    
    select `AccountType_ID` into accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`ToAccountNumber`;
    select `Name` into accountName from `AccountType` where `ID` = accttype;
    
	if new.`Type` = 'DEPOSIT' THEN
        set new.`Status`  = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`FromBankName` = 'N/A';
        set new.`FromAccountNumber` = 'N/A';
        set new.`ToBankName` = 'CUSTOMER';
        set new.`ToName` = accountName;
	end if;
END //

delimiter ;

-- CREATES THE TRIGGER FOR ALL WITHDRAWAL TRANSACTION TO RECORD INTO THE DATABASE

drop trigger if exists withdraw_from_account;

delimiter //
create trigger withdraw_from_account
	before insert on `Transaction`
	for each row
BEGIN
	declare accountName varchar(10);
    declare accttype int;
    
    
    select `AccountType_ID` into accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`FromAccountNumber`;
    select `Name` into accountName from `AccountType` where `ID` = accttype;
    
	if new.`Type` = 'WITHDRAWAL' THEN
        set new.`Status` = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`ToBankName` = 'N.A';
        set new.`ToAccountNumber` = 'N.A';
        set new.`FromBankName` = 'CUSTOMER';
        set new.`FromName` = accountName;
	end if;
END //

delimiter ;




-- CREATES A TRIGGER THAT CREATES AN ONLINE BANKING ACCOUNT WHEN NEW INFO IS INSERTED


drop trigger if exists create_online_account_accounts;

delimiter //
create trigger create_online_account_accounts
	before insert on `OnlineBankingAcct`
	for each row
BEGIN
	declare accountsID int;
	
    select `ID` into accountsID from `Accounts` where `Customer_ID` = new.`customerID`;
    set new.`AccountsID` = accountsID;
    
    
END //

delimiter ;


-- CREATES THE TRIGGER FOR ALL DEBIT TRANSACTIONS TO RECORD INTO THE DATABASE


drop trigger if exists debit_from_account;

delimiter //
create trigger debit_from_account
	before insert on `Transaction`
	for each row
BEGIN
	declare accountName varchar(10);
    declare accttype int;
    declare accountID int;
    declare cur_bal decimal(9,2);
    declare new_bal decimal(9,2);
    
    select `Accounts_ID` into accountID from `Account` where `AccountNumber` = new.`FromAccountNumber`;
    select `AccountType_ID` into accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`FromAccountNumber`;
    select `Name` into accountName from `AccountType` where `ID` = accttype;
    select `Balance` into cur_bal from `Account` where `AccountNumber` = new.`FromAccountNumber`;
    
    
	if new.`Type` = 'DEBIT' THEN
        set new.`Status` = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`FromName` = accountName;
        set new.`accountID` = accountID;
        set new_bal = cur_bal - new.`Amount`;
        update `Account` set `Balance` = new_bal where `AccountNumber` = new.`FromAccountNumber`;
        
        
	end if;
END //

delimiter ;


-- CREATES THE TRIGGER FOR ALL CREDIT TRANSACTIONS TO RECORD INTO THE DATABASE


drop trigger if exists credit_into_account;

delimiter //
create trigger credit_into_account
	before insert on `Transaction`
	for each row
BEGIN
	declare accountName varchar(10);
    declare accttype int;
    declare accountID int;
    declare cur_bal decimal(9,2);
    declare new_bal decimal(9,2);
    
    select `Accounts_ID` into accountID from `Account` where `AccountNumber` = new.`ToAccountNumber`;
    select `AccountType_ID` into accttype from `Customer_Accounts_Account` where `AccountNumber` = new.`ToAccountNumber`;
    select `Name` into accountName from `AccountType` where `ID` = accttype;
    select `Balance` into cur_bal from `Account` where `AccountNumber` = new.`ToAccountNumber`;
    
    
	if new.`Type` = 'CREDIT' THEN
        set new.`Status` = 'SUCCESSFUL';
        set new.`DateAndTime` = current_timestamp();
        set new.`ToName` = accountName;
        set new.`accountID` = accountID;
        set new_bal = cur_bal + new.amount;
        update `Account` set `Balance` = new_bal where `AccountNumber` = new.`ToAccountNumber`;
        
        
	end if;
END //

delimiter ;

insert into `Customer` values (default,'Demo','Account','Unknown', current_date(),'Unknown',7023123452, 'NewfoundLand and Labrador', 'Canada', 'unknown','st. johns', 'Canada', 'A2B 1B2');