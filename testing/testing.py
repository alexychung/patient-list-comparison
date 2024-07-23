import unittest
import pandas as pd

class TestMethods(unittest.TestCase):
    def test_pdreading(self):
        self.assertEqual("")


if __name__ == "__main__":
    data = pd.read_excel("InsuranceTest.xlsx")
    list = []
    for index,row in data.iterrows():
        print(index)
        list.append(row)
    print (list[0]["First Name"])