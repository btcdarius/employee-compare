import unittest

from employee_compare import main

class FinalOutput(unittest.TestCase):
	file1 = "/Users/briancraine/Documents/Temp/samplea.csv"
	file2 = "/Users/briancraine/Documents/Temp/sampleb.csv"
	
	def test_compare1(self):
		expectedResult = "The following employees were removed:\nErica Meyers (Employee Number: 3)\n\nThe following employees were added:\nBill Jones (Employee Number: 6)\n\nThe following employees were updated:\nSean Colbert (Employee Number: 1)\n\tDepartment: Marketing → Finance\n\tGroup: G3 → G10\n\tTeam: T1 → T3\n\tSupervisor: Mark Penn → Anton Troianovski\n\tCost Center: R&D → GA\nJane Doe (Employee Number: 5)\n\tEmployee Name: Jane Mori → Jane Doe\n"
		self.assertEqual(expectedResult, main(self.file1, self.file2))

	def test_compare2(self):
		expectedResult = "The following employees were removed:\nBill Jones (Employee Number: 6)\n\nThe following employees were added:\nErica Meyers (Employee Number: 3)\n\nThe following employees were updated:\nSean Colbert (Employee Number: 1)\n\tDepartment: Finance → Marketing\n\tGroup: G10 → G3\n\tTeam: T3 → T1\n\tSupervisor: Anton Troianovski → Mark Penn\n\tCost Center: GA → R&D\nJane Mori (Employee Number: 5)\n\tEmployee Name: Jane Doe → Jane Mori\n"
		self.assertEqual(expectedResult, main(self.file2, self.file1))


if __name__ == '__main__':
	unittest.main()