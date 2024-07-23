import unittest
import pandas as pd
import FileHelper
import DatabaseDriver

class TestMethods(unittest.TestCase):
    def test_pdreading(self):
        self.assertEqual("")


if __name__ == '__main__':
    fh = FileHelper.FileHelper()
    database = DatabaseDriver(fh)
    database.clearTables()
    database.create_sqlite_db()
    database.create_tables()
    adf = pd.read_excel(io='ActivePatientTest.xlsx', names = ["firstname", "lastname", "dob", "attributedprovider"])
    idf = pd.read_excel(io='InsuranceTest.xlsx', names = ["firstname", "lastname", "dob", "attributedprovider"])
    adf['dob'] = pd.to_datetime(adf['dob']).dt.date
    idf['dob'] = pd.to_datetime(idf['dob']).dt.date
    database.insertActivePatientDFIntoTable(adf)
    database.insertInsuranceDFIntoTable(idf)
    database.generateOutput()