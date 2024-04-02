CREATE PROCEDURE CreateRequest @EmployeeName varchar(100), @Comment text, @Status varchar(100), @Unit varchar(100), @ItemId int, @Quantity int, @Price int, @RowComment text
AS
BEGIN
    DECLARE @RequestId int, @RequestsRowId int;

    -- Insert a new row into the Requests table
    INSERT INTO Requests (EmployeeName, Comment, Status)
    VALUES (@EmployeeName, @Comment, @Status);

    -- Get the ID of the newly inserted row
    SET @RequestId = SCOPE_IDENTITY();

    -- Insert a new row into the RequestsRows table
    INSERT INTO RequestsRows (Unit, ItemId, Quantity, Price, Comment)
    VALUES (@Unit, @ItemId, @Quantity, @Price, @RowComment);

    -- Get the ID of the newly inserted row
    SET @RequestsRowId = SCOPE_IDENTITY();

    -- Connect the new request with the new request row
    INSERT INTO RequestsRowsConnect (RequestsRowId, RequestId)
    VALUES (@RequestsRowId, @RequestId);
END;




CREATE PROCEDURE AddRequestToExisting @EmployeeName varchar(100), @Unit varchar(100), @ItemId int, @Quantity int, @Price int, @RowComment text
AS
BEGIN
    DECLARE @RequestsRowId int;
    DECLARE @LastRequestId int;

    -- Insert a new row into the RequestsRows table
    INSERT INTO RequestsRows (Unit, ItemId, Quantity, Price, Comment)
    VALUES (@Unit, @ItemId, @Quantity, @Price, @RowComment);

    -- Get the ID of the newly inserted row
    SET @RequestsRowId = SCOPE_IDENTITY();

    -- Get the ID of the last request made by the employee
    SELECT @LastRequestId = MAX(Id) FROM Requests WHERE EmployeeName = @EmployeeName;

    -- Connect the new request row with the last request
    INSERT INTO RequestsRowsConnect (RequestsRowId, RequestId)
    VALUES (@RequestsRowId, @LastRequestId);
END;
