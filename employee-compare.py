import sys
import csv

# Define the Employee class
class Employee:
	def __init__(self, employeeNumber, department, group, team, employeeName, supervisor, costCenter):
		self.employeeNumber = employeeNumber
		self.department = department
		self.group = group
		self.team = team
		self.employeeName = employeeName
		self.supervisor = supervisor
		self.costCenter = costCenter

	def __eq__(self, other):
		return self.employeeNumber == other.employeeNumber and self.department == other.department and self.group == other.group and self.team == other.team and self.employeeName == other.employeeName and self.supervisor == other.supervisor and self.costCenter == other.costCenter

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
			employee = Employee(row["Employee Number"], row["Department"], row["Group"], row["Team"], row["Employee Name"], row["Supervisor"], row["Cost Center"])
			employeeList.append(employee)
			
			line_count += 1
			
	return employeeList

# Function for getting a list of Employee Numbers from a list of Employee objects
def get_employee_numbers(employeeList):
	employeeNumbers = []
	
	for employee in employeeList:
		employeeNumbers.append(employee.employeeNumber)

	return employeeNumbers


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
oldEmployeeNumbers = get_employee_numbers(oldEmployeeList)
newEmployeeNumbers = get_employee_numbers(newEmployeeList)

# Find employees from old list who have been removed in new list
for employee in oldEmployeeList:
	if not (employee.employeeNumber in newEmployeeNumbers):
		removedEmployees.append(employee)
	
# Find employees from new list who were not in the old list OR are in the old list but are not an exact match
for employee in newEmployeeList:
	if not (employee.employeeNumber in oldEmployeeNumbers):
		addedEmployees.append(employee)
	else:
		if not (employee in oldEmployeeList):
			# Find the employee in the old employee list that has the same Employee Number but is not identical, and note the changes
			updates = []
			oldVersionsOfEmployee = filter(lambda x: x.employeeNumber == employee.employeeNumber, oldEmployeeList)
			for oldVersionOfEmployee in oldVersionsOfEmployee:
				if employee.department != oldVersionOfEmployee.department:
					updates.append("Department: " + oldVersionOfEmployee.department + " → " + employee.department)
				
				if employee.group != oldVersionOfEmployee.group:
					updates.append("Group: " + oldVersionOfEmployee.group + " → " + employee.group)
				
				if employee.team != oldVersionOfEmployee.team:
					updates.append("Team: " + oldVersionOfEmployee.team + " → " + employee.team)
					
				if employee.employeeName != oldVersionOfEmployee.employeeName:
					updates.append("Employee Name: " + oldVersionOfEmployee.employeeName + " → " + employee.employeeName)
				
				if employee.supervisor != oldVersionOfEmployee.supervisor:
					updates.append("Supervisor: " + oldVersionOfEmployee.supervisor + " → " + employee.supervisor)
					
				if employee.costCenter != oldVersionOfEmployee.costCenter:
					updates.append("Cost Center: " + oldVersionOfEmployee.costCenter + " → " + employee.costCenter)	
			
			employeeUpdate = EmployeeUpdate(employee, updates)	
			employeeUpdates.append(employeeUpdate)


# Output the results
print("The following employees were removed:")
for employee in removedEmployees:
	print(employee.employeeName + " (Employee Number: " + employee.employeeNumber + ")")

print("")

print("The following employees were added:")
for employee in addedEmployees:
	print(employee.employeeName + " (Employee Number: " + employee.employeeNumber + ")")
	
print("")

print("The following employees were updated:")
for employeeUpdate in employeeUpdates:
	print(employeeUpdate.employee.employeeName + " (Employee Number: " + employeeUpdate.employee.employeeNumber + ")")
	
	for update in employeeUpdate.updates:
		print("\t" + update)
	
	
