import sys
import csv

# Define the Employee class
class Employee:
	def __init__(self, id, name, department, birthMonth):
		self.id = id
		self.name = name
		self.department = department
		self.birthMonth = birthMonth

	def __eq__(self, other):
		return self.id == other.id and self.name == other.name and self.department == other.department and self.birthMonth == other.birthMonth

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
			employee = Employee(row["id"], row["name"], row["department"], row["birthday month"])
			employeeList.append(employee)
			
			line_count += 1
			
	return employeeList

# Function for getting a list of IDs from a list of Employee objects
def get_employee_ids(employeeList):
	employeeIDs = []
	
	for employee in employeeList:
		employeeIDs.append(employee.id)

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

# Get old and new employee ID lists
oldEmployeeIDs = get_employee_ids(oldEmployeeList)
newEmployeeIDs = get_employee_ids(newEmployeeList)

# Find employees from old list who have been removed in new list
for employee in oldEmployeeList:
	if not (employee.id in newEmployeeIDs):
		removedEmployees.append(employee)
	
# Find employees from new list who were not in the old list OR are in the old list but are not an exact match
for employee in newEmployeeList:
	if not (employee.id in oldEmployeeIDs):
		addedEmployees.append(employee)
	else:
		if not (employee in oldEmployeeList):
			# Find the employee in the old employee list that has the same ID but is not identical, and note the changes
			updates = []
			oldVersionsOfEmployee = filter(lambda x: x.id == employee.id, oldEmployeeList)
			for oldVersionOfEmployee in oldVersionsOfEmployee:
				if employee.name != oldVersionOfEmployee.name:
					updates.append("Name: " + oldVersionOfEmployee.name + " → " + employee.name)
				
				if employee.department != oldVersionOfEmployee.department:
					updates.append("Department: " + oldVersionOfEmployee.department + " → " + employee.department)
				
				if employee.birthMonth != oldVersionOfEmployee.birthMonth:
					updates.append("Birth Month: " + oldVersionOfEmployee.birthMonth + " → " + employee.birthMonth)
			
			employeeUpdate = EmployeeUpdate(employee, updates)	
			employeeUpdates.append(employeeUpdate)


# Output the results
print("The following employees were removed:")
for employee in removedEmployees:
	print(employee.name + " (ID: " + employee.id + ")")

print("")

print("The following employees were added:")
for employee in addedEmployees:
	print(employee.name + " (ID: " + employee.id + ")")
	
print("")

print("The following employees were updated:")
for employeeUpdate in employeeUpdates:
	print(employeeUpdate.employee.name + " (ID: " + employee.id + ")")
	
	for update in employeeUpdate.updates:
		print("\t" + update)
	
	
