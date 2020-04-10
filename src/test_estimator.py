import unittest
import estimator

class TestEstimator(unittest.TestCase):

    def setUp(self):
        self.inputDataFormat={
            "region": {
                "name": "Africa",
                "avgAge": 19.7,
                "avgDailyIncomeInUSD": 5,
                "avgDailyIncomePopulation":0.71
                },
            "periodType": "days",
            "timeToElapse": 58,
            "reportedCases": 674,
            "population": 66622705,
            "totalHospitalBeds": 1380614
        }

    def tearDown(self):
        pass

    def test_output_format(self):
        output = estimator.estimator(self.inputDataFormat)
        print(output)
        
        #assert the required keys exists in the output data
        self.assertEqual("data" in output.keys(), True)
        self.assertEqual("impact" in output.keys(), True)
        self.assertEqual("severeImpact" in output.keys(), True)

        #assert data input data is contained in the output dict
        self.assertEqual(output["data"], self.inputDataFormat)

        #assert len of output is equal to 3
        self.assertEqual(len(output), 3)

    def test_estimate_currently_infected(self):
        output = estimator.estimate_currently_infected(self.inputDataFormat["reportedCases"])
        self.assertEqual(output["impact"], 6740)
        self.assertEqual(output["severe_impact"], 33700)

    def test_infections_by_requested_time(self):
        current_infections = {"impact":200, "severe_impact":2000}
        output = estimator.infections_by_requested_time(current_infections, self.inputDataFormat["periodType"], self.inputDataFormat["timeToElapse"])
        self.assertEqual(output["impact"], 104857600)
        self.assertEqual(output["severe_impact"], 1048576000)

        with self.assertRaises(ValueError):
            estimator.infections_by_requested_time(current_infections, "some_val", self.inputDataFormat["timeToElapse"])
            
    def test_severe_cases_requested_time(self):
        infections_by_requested_time={"impact":100, "severe_impact": 1000}
        output = estimator.get_severe_cases_with_time(infections_by_requested_time)

        self.assertEqual(output["impact"], 15)
        self.assertEqual(output["severe_impact"], 150)
    
    def test_hospital_beds_by_requested_time(self):
        severe_cases = {"impact":100, "severe_impact":1000}
        available_beds = estimator.estimate_available_beds(severe_cases, 2000)
        
        self.assertEqual(int(available_beds["impact"]), 700)
        self.assertEqual(int(available_beds["severe_impact"]), -300)
        

if (__name__=="__main__"):
    unittest.main()