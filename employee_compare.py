import sys
import csv

# Configuration
idField = "Employee ID"
nameField = "Preferred Name"
otherFields = ["Department", "Group", "Team", "CF LO Supervisory Level 4", "Cost Center - Name", "Subgroup", "Discipline"]


# Define the Employee class
class Employee:
	def __init__(self, employeeID, employeeName, employeeInfo):
		self.employeeID = employeeID
		self.employeeName = employeeName
		self.employeeInfo = employeeInfo

	def __eq__(self, other):
		return self.employeeID == other.employeeID and self.employeeName == other.employeeName and self.employeeInfo == other.employeeInfo

# Define the EmployeeUpdate class
class EmployeeUpdate:
	def __init__(self, employee, updates):
		self.employee = employee
		self.updates = updates

# Function for loading employees from a CSV and return as a list of Employee objects
def load_employee_list(fileName):
	employeeList = []
	
	with open(fileName, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
	
		for row in csv_reader:
			employeeInfo = {}
			for field in otherFields:
				employeeInfo[field] = row[field]
			
			employee = Employee(row[idField], row[nameField], employeeInfo)
			employeeList.append(employee)
			
			line_count += 1
			
	return employeeList

# Function for getting a list of Employee Numbers from a list of Employee objects
def get_employee_numbers(employeeList):
	employeeIDs = []
	
	for employee in employeeList:
		employeeIDs.append(employee.employeeID)

	return employeeIDs


## EXECUTION

# Create variables for output
addedEmployees = []
removedEmployees = []
employeeUpdates = []


# Exit with error if two arguments are not supplied
if len(sys.argv) != 3:
	print("Error: Two files must be supplied.")
	sys.exit()

# Get the old and new file paths from the arguments passed
oldFile = sys.argv[1]
newFile = sys.argv[2]

# Load old and new employee lists into objects
oldEmployeeList = load_employee_list(oldFile)
newEmployeeList = load_employee_list(newFile)

# Get old and new employee number lists
oldEmployeeIDs = get_employee_numbers(oldEmployeeList)
newEmployeeIDs = get_employee_numbers(newEmployeeList)

# Find employees from old list who have been removed in new list
for employee in oldEmployeeList:
	if not (employee.employeeID in newEmployeeIDs):
		removedEmployees.append(employee)
	
# Find employees from new list who were not in the old list OR are in the old list but are not an exact match
for employee in newEmployeeList:
	if not (employee.employeeID in oldEmployeeIDs):
		addedEmployees.append(employee)
	else:
		if not (employee in oldEmployeeList):
			# Find the employee in the old employee list that has the same Employee Number but is not identical, and note the changes
			updates = []
			oldVersionsOfEmployee = filter(lambda x: x.employeeID == employee.employeeID, oldEmployeeList)
			for oldVersionOfEmployee in oldVersionsOfEmployee:
				if employee.employeeName != oldVersionOfEmployee.employeeName:
					updates.append(nameField + ": " + oldVersionOfEmployee.employeeName + " → " + employee.employeeName)
				
				for field in otherFields:
					if employee.employeeInfo[field] != oldVersionOfEmployee.employeeInfo[field]:
						updates.append(field + ": " + oldVersionOfEmployee.employeeInfo[field] + " → " + employee.employeeInfo[field])
								
			employeeUpdate = EmployeeUpdate(employee, updates)	
			employeeUpdates.append(employeeUpdate)


# Output the results
print("The following employees were removed:")
for employee in removedEmployees:
	print(employee.employeeName + " (Employee Number: " + employee.employeeID + ")")

print("")

print("The following employees were added:")
for employee in addedEmployees:
	print(employee.employeeName + " (Employee Number: " + employee.employeeID + ")")
	
print("")

print("The following employees were updated:")
for employeeUpdate in employeeUpdates:
	print(employeeUpdate.employee.employeeName + " (Employee Number: " + employeeUpdate.employee.employeeID + ")")
	
	for update in employeeUpdate.updates:
		print("\t" + update)
	
	
