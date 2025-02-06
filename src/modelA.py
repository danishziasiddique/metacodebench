
import sqlite3
import requests
import os
import re

class MainDatabase:
    def __init__(self, db_url, db_filename='companies.db'):
        self.db_url = db_url
        self.db_filename = db_filename
        self.connection = None

        try:
            if not os.path.exists(self.db_filename):
                self._download_database()
            self.connection = sqlite3.connect(self.db_filename)
        except Exception as e: raise RuntimeError(f"Failed to initialize database: {e}")

    def _download_database(self): 
        response = requests.get(self.db_url)
        if response.status_code != 200: raise RuntimeError("Failed to download the database. Please check the URL.")
        
        with open(self.db_filename, 'wb') as f:
            f.write(response.content)

    def _cd(self):
        """
        Cleans the database data as per the requirements:
        - Simplifies the domain column to retain only the main domain.
        - Drops rows where both 'domain' and 'locality' are missing.
        - Cleans the 'name' column by converting to lowercase and removing non-alphabetic characters.
        """
        cursor = self.connection.cursor()

        # Select all data
        cursor.execute("SELECT * FROM companies")
        rows = cursor.fetchall()

        # Get column names
        cursor.execute("PRAGMA table_info(companies)")
        columns = [info[1] for info in cursor.fetchall()]

        # Get column indices
        domain_idx = columns.index('domain')
        locality_idx = columns.index('locality')
        name_idx = columns.index('name')

        cleaned_data = []

        for row in rows:
            domain = row[domain_idx]
            locality = row[locality_idx]
            name = row[name_idx]

            # Simplify the domain
            if domain:
                main_domain = re.search(r'([\w-]+\.[\w]+)$', domain)
                domain = main_domain.group(1) if main_domain else None

            # Drop rows if both domain and locality are missing
            if not domain and not locality:
                continue

            # Clean the name column
            if name:
                name = re.sub(r'[^a-zA-Z]', '', name).lower()

            cleaned_row = list(row)
            cleaned_row[domain_idx] = domain
            cleaned_row[name_idx] = name
            cleaned_data.append(cleaned_row)

        # Recreate the table and insert cleaned data
        cursor.execute("DROP TABLE IF EXISTS companies_cleaned")
        cursor.execute(f"CREATE TABLE companies_cleaned AS SELECT * FROM companies LIMIT 0")

        for row in cleaned_data:
            placeholders = ', '.join(['?' for _ in row])
            cursor.execute(f"INSERT INTO companies_cleaned VALUES ({placeholders})", row)

        self.connection.commit()
        cursor.close()

    def _f(self, name=None, domain=None, industry=None, locality=None, country=None, current_employees=None, numberofdata=None):
        """
        Fetches data from the cleaned database table based on filters.
        """
        cursor = self.connection.cursor()
        query = "SELECT * FROM companies_cleaned"
        filters = []
        params = []

        if name:
            filters.append("name LIKE ?")
            params.append(f"%{name.lower()}%")
        if domain:
            filters.append("domain LIKE ?")
            params.append(f"%{domain.lower()}%")
        if industry:
            filters.append("industry LIKE ?")
            params.append(f"%{industry.lower()}%")
        if locality:
            filters.append("locality LIKE ?")
            params.append(f"%{locality.lower()}%")
        if country:
            filters.append("country LIKE ?")
            params.append(f"%{country.lower()}%")
        if current_employees is not None:
            filters.append("current_employees >= ?")
            params.append(current_employees)

        if filters:
            query += " WHERE " + " AND ".join(filters)

        if numberofdata is not None:
            query += f" LIMIT {numberofdata}"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Fetch column names
        cursor.execute("PRAGMA table_info(companies_cleaned)")
        columns = [info[1] for info in cursor.fetchall()]

        # Convert rows to dictionary format
        result = {col: [] for col in columns}
        for row in rows:
            for col, value in zip(columns, row):
                result[col].append(value)

        cursor.close()
        return result
