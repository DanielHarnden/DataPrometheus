CREATE TABLE Customer (
    Id INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Address VARCHAR(100)
);

CREATE TABLE Order (
    Id INT PRIMARY KEY,
    CustomerId INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerId) REFERENCES Customer(Id)
);

CREATE TABLE Product (
    Id INT PRIMARY KEY,
    Name VARCHAR(50),
    Price DECIMAL(10, 2)
);

CREATE TABLE OrderItem (
    Id INT PRIMARY KEY,
    OrderId INT,
    ProductId INT,
    Quantity INT,
    FOREIGN KEY (OrderId) REFERENCES Order(Id),
    FOREIGN KEY (ProductId) REFERENCES Product(Id)
);

CREATE TABLE Category (
    Id INT PRIMARY KEY,
    Name VARCHAR(50)
);

CREATE TABLE ProductCategory (
    Id INT PRIMARY KEY,
    ProductId INT,
    CategoryId INT,
    FOREIGN KEY (ProductId) REFERENCES Product(Id),
    FOREIGN KEY (CategoryId) REFERENCES Category(Id)
);

CREATE TABLE Supplier (
    Id INT PRIMARY KEY,
    Name VARCHAR(50),
    Address VARCHAR(100)
);

CREATE TABLE SupplierProduct (
    Id INT PRIMARY KEY,
    SupplierId INT,
    ProductId INT,
    FOREIGN KEY (SupplierId) REFERENCES Supplier(Id),
    FOREIGN KEY (ProductId) REFERENCES Product(Id)
);

CREATE TABLE Employee (
    Id INT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    HireDate DATE,
    ManagerId INT,
    DepartmentId INT,
    FOREIGN KEY (ManagerId) REFERENCES Employee(Id),
    FOREIGN KEY (DepartmentId) REFERENCES Department(Id)
);

CREATE TABLE Department (
    Id INT PRIMARY KEY,
    Name VARCHAR(50)
);