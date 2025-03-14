import pymssql

# Use the loopback IP address for localhost (127.0.0.1)
server = '127.0.0.1'  # Or use 'localhost' (should be equivalent)
database = 'AdventureWorks2019'  # Replace with your database name
username = 'DESKTOP-4ALJIGT\\Tharsol'  # Your Windows username
password = ''  # Leave empty for Windows Authentication

try:
    # Establish the connection
    connection = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database,
        charset='UTF-8'  # Optional, just to ensure character encoding compatibility
    )

    # Create a cursor to execute the SQL query
    cursor = connection.cursor()

    # Define your query
    query = """
    SELECT BusinessEntityID, JobTitle, BirthDate, MaritalStatus, Gender, HireDate
    FROM HumanResources.Employee
    """

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    for row in cursor:
        print(row)

    # Close the connection
    cursor.close()
    connection.close()

except pymssql.OperationalError as e:
    print(f"Error connecting to SQL Server: {e}")
