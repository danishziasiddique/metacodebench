import unittest
import os
from solution import *

class TestMainDatabase(unittest.TestCase):
    def setUp(self):
        os.remove("companies.db") if os.path.exists("companies.db") else None
        db_url = "https://github.com/hiblackai/public-datasets/raw/refs/heads/main/companies.db"
        self.db = MainDatabase(db_url)
        self.db._cd()  

    def test_get_multiple_companies(self):
        result = self.db._f(numberofdata=5)
        expected = {
            'id': [159, 193, 238, 654, 673],
            'name': ['globalcomputerservicesllc', 'ipfsoftwares', 'adamjeegroup', 'artgalleryline', 'samaalandalus'],
            'domain': ['globcom-oman.com', 'ipfsoftwares.com', 'adamjee.mu', 'artgalleryline.com', 'sama-alandalus.ly'],
            'year_founded': ['1998.0', '2013.0', '1979.0', '2003.0', '2011.0'],
            'industry': ['computer software', 'information technology and services', 'real estate', 'fine art', 'pharmaceuticals'],
            'size range': ['51 - 200', '11 - 50', '1 - 10', '1 - 10', '1 - 10'],
            'locality': ['burnsville, minnesota, united states', 'dar es salaam, dar es salaam, tanzania',
                         'grand baie, riviere du rempart, mauritius', "tbilisi, dushet'is raioni, georgia",
                         'tripoli, tripoli, libya'],
            'country': ['oman', 'tanzania', 'mauritius', 'georgia', 'libya'],
            'current_employees': ['24', '5', '1', '2', '1'],
            'total_employees': ['35', '7', '1', '2', '1']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_name(self):
        result = self.db._f(name="atlas", numberofdata=2)
        expected = {
            'id': [4057, 39329],
            'name': ['atlasfoundation', 'bpratlasmara'],
            'domain': ['atlasfoundation.me', None],
            'year_founded': ['2010.0', '1975.0'],
            'industry': ['civic & social organization', 'financial services'],
            'size range': ['1 - 10', '11 - 50'],
            'locality': ['montenegro, rio grande do sul, brazil', 'kigali, kigali, rwanda'],
            'country': ['montenegro', 'rwanda'],
            'current_employees': ['1', '10'],
            'total_employees': ['5', '11']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_industry(self):
        result = self.db._f(industry="human resources", numberofdata=1)
        expected = {
            'id': [1951],
            'name': ['asiatravelhrrecruitmentcompany'],
            'domain': ['asiatravel.kg'],
            'year_founded': ['2012.0'],
            'industry': ['human resources'],
            'size range': ['1 - 10'],
            'locality': ['bishkek, bishkek, kyrgyzstan'],
            'country': ['kyrgyzstan'],
            'current_employees': ['1'],
            'total_employees': ['1']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_location_and_employees(self):
        result = self.db._f(locality="france", country="benin", current_employees=1, numberofdata=2)
        expected = {
            'id': [1422, 46533],
            'name': ['anthonyg', 'solisoeurope'],
            'domain': ['anthonyg.design', None],
            'year_founded': ['2017.0', None],
            'industry': ['architecture & planning', 'textiles'],
            'size range': ['1 - 10', '11 - 50'],
            'locality': ['nantes, pays de la loire, france', 'nantes, pays de la loire, france'],
            'country': ['benin', 'benin'],
            'current_employees': ['1', '8'],
            'total_employees': ['1', '17']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_country(self):
        result = self.db._f(country="benin", numberofdata=3)
        expected = {
            'id': [1422, 4326, 41851],
            'name': ['anthonyg', 'tbcsarl', 'stededistributiondupointdujour'],
            'domain': ['anthonyg.design', 'groupetbc.com', 'pointdujour.fr'],
            'year_founded': ['2017.0', '2012.0', None],
            'industry': ['architecture & planning', 'computer software', 'broadcast media'],
            'size range': ['1 - 10', '1 - 10', '11 - 50'],
            'locality': ['nantes, pays de la loire, france', 'cotonou, littoral, benin', None],
            'country': ['benin', 'benin', 'benin'],
            'current_employees': ['1', '3', '8'],
            'total_employees': ['1', '4', '42']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_locality(self):
        result = self.db._f(locality="france", numberofdata=1)
        expected = {
            'id': [1422],
            'name': ['anthonyg'],
            'domain': ['anthonyg.design'],
            'year_founded': ['2017.0'],
            'industry': ['architecture & planning'],
            'size range': ['1 - 10'],
            'locality': ['nantes, pays de la loire, france'],
            'country': ['benin'],
            'current_employees': ['1'],
            'total_employees': ['1']
        }
        self.assertEqual(result, expected)

    def test_get_companies_by_employees(self):
        result = self.db._f(current_employees=5, numberofdata=3)
        expected = {
            'id': [193, 782, 1282],
            'name': ['ipfsoftwares', 'amecointernationaltravel', 'formesandominicanasrl'],
            'domain': ['ipfsoftwares.com', 'amecotravel.com', 'com.co'],
            'year_founded': ['2013.0', '1977.0', None],
            'industry': ['information technology and services', 'airlines/aviation', 'civil engineering'],
            'size range': ['11 - 50', '11 - 50', '11 - 50'],
            'locality': ['dar es salaam, dar es salaam, tanzania', None, 'santo domingo oeste, santo domingo, dominican republic'],
            'country': ['tanzania', 'fiji', 'dominican republic'],
            'current_employees': ['5', '5', '9'],
            'total_employees': ['7', '6', '17']
        }
        self.assertEqual(result, expected)

    def test_get_specific_company(self):
        result = self.db._f(name="globalcomputerservicesllc", domain="globcom-oman", industry="computer software",
                            locality="minnesota", country="oman", current_employees=24)
        expected = {
            'id': [159],
            'name': ['globalcomputerservicesllc'],
            'domain': ['globcom-oman.com'],
            'year_founded': ['1998.0'],
            'industry': ['computer software'],
            'size range': ['51 - 200'],
            'locality': ['burnsville, minnesota, united states'],
            'country': ['oman'],
            'current_employees': ['24'],
            'total_employees': ['35']
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
