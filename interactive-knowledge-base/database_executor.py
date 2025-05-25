import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import pandas as pd
from typing import Dict, List, Any, Optional, Union

class DatabaseExecutor:
    """
    A class to connect to PostgreSQL database and execute SQL queries.
    """
    
    def __init__(self, 
                 host: str = "localhost", 
                 port: int = 5432, 
                 dbname: str = "loan_application", 
                 user: str = "loan_application_user", 
                 password: str = "loan_application_password"):
        """
        Initialize the DatabaseExecutor with connection parameters.
        
        Args:
            host: Database host
            port: Database port
            dbname: Database name
            user: Database username
            password: Database password
        """
        self.connection_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password
        }
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Union[str, pd.DataFrame]:
        """
        Execute a SQL query and return the results.
        
        Args:
            query: SQL query to execute
            params: Parameters for the SQL query
            
        Returns:
            Results of the query as a formatted string or DataFrame
        """
        try:
            # Connect to the database
            conn = psycopg2.connect(**self.connection_params)
            
            # Create a cursor with dictionary results
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Execute the query
                cursor.execute(query, params)
                
                # Check if this is a SELECT query (has results)
                if cursor.description:
                    # Fetch all results
                    results = cursor.fetchall()
                    
                    # Convert to DataFrame for easier handling
                    df = pd.DataFrame(results)
                    
                    if df.empty:
                        return "Query executed successfully, but no results were returned."
                    
                    # Format the results as a string table
                    return df.to_string(index=False)
                else:
                    # For non-SELECT queries (INSERT, UPDATE, DELETE)
                    conn.commit()
                    row_count = cursor.rowcount
                    return f"Query executed successfully. {row_count} rows affected."
                    
        except Exception as e:
            return f"Error executing query: {str(e)}"
        
        finally:
            # Close the connection
            if 'conn' in locals() and conn is not None:
                conn.close()