import io
import unittest
import xmlrunner
import pandas as pd
from app import app

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
    
    def test_hinzufuegen_loeschen_herunterladen_gpids(self):
        for i in range(1, 7):
            self.client.post('/add/gpid', data={
                'gpid': f'GPID {i}'
                })
            
        for i in range(1,7):
            self.client.post('/add/gpname', data={
                'gpname': f'GPNAME {i}'
                })

        self.client.get('/remove/4') 
        self.client.get('/remove/1')

        response = self.client.get('/download_gpids')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        with io.BytesIO(response.data) as buffer:
            df = pd.read_excel(buffer)
            self.assertListEqual(['GPID 2', 'GPID 3', 'GPID 5', 'GPID 6'], df.gpid.values.tolist())
            self.assertListEqual(['GPNAME 2', 'GPNAME 3', 'GPNAME 5', 'GPNAME 6'], df.gp_name.values.tolist())
            
if __name__ == '__main__':
    with open('./test_reports/report.xml', 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output))