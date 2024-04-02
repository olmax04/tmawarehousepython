-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-03-31 02:37:56.552

-- tables
-- Table: Items
CREATE TABLE Items (
    Id int IDENTITY(1, 1)  NOT NULL,
    ItemGroup varchar(100)  NOT NULL,
    Unit varchar(100)  NOT NULL,
    Quantity int  NOT NULL,
    Price int  NOT NULL,
    Status varchar(100)  NOT NULL,
    StorageLocation varchar(100)  NULL,
    ContactPerson text  NULL,
    Photo varchar(250)  NULL,
    CONSTRAINT Items_pk PRIMARY KEY  (Id)
);

-- Table: Requests
CREATE TABLE Requests (
    Id int IDENTITY(1, 1)  NOT NULL,
    EmployeeName varchar(100)  NOT NULL,
    Comment text  NULL,
    Status varchar(100)  NULL,
    CONSTRAINT Requests_pk PRIMARY KEY  (Id)
);

-- Table: RequestsRows
CREATE TABLE RequestsRows (
    Id int IDENTITY(1, 1)  NOT NULL,
    Unit varchar(100)  NOT NULL,
    ItemId int  NOT NULL,
    Quantity int  NOT NULL,
    Price int  NOT NULL,
    Comment text  NULL,
    CONSTRAINT RequestsRows_pk PRIMARY KEY  (id)
);

-- Table: RequestsRowsConnect
CREATE TABLE RequestsRowsConnect (
    Id int IDENTITY(1, 1)  NOT NULL,
    RequestsRowId int  NOT NULL,
    RequestId int  NOT NULL,
    CONSTRAINT RequestsRowsConnect_pk PRIMARY KEY  (id)
);

-- foreign keys
-- Reference: RequestsRowsConnect_Requests (table: RequestsRowsConnect)
ALTER TABLE RequestsRowsConnect ADD CONSTRAINT RequestsRowsConnect_Requests
    FOREIGN KEY (RequestId)
    REFERENCES Requests (Id);

-- Reference: RequestsRowsConnect_RequestsRows (table: RequestsRowsConnect)
ALTER TABLE RequestsRowsConnect ADD CONSTRAINT RequestsRowsConnect_RequestsRows
    FOREIGN KEY (RequestsRowId)
    REFERENCES RequestsRows (id);

-- Reference: RequestsRows_Items (table: RequestsRows)
ALTER TABLE RequestsRows ADD CONSTRAINT RequestsRows_Items
    FOREIGN KEY (ItemId)
    REFERENCES Items (Id);

-- End of file.

