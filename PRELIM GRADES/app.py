# Inputs
absences = int(input("Enter the number of absences: "))
if absences < 0:
    print("Invalid input. Absences cannot be negative.")
    absences = int(input("Please enter a valid number of absences: "))

if absences >= 4:
    print("FAILED due to absences.")
else:
    prelim_exam = float(input("Enter the Prelim Exam Grade (0-100): "))
    quizzes = float(input("Enter the Quizzes Grade (0-100): "))
    requirements = float(input("Enter the Requirements Grade (0-100): "))
    recitation = float(input("Enter the Recitation Grade (0-100): "))

    # Validate grades
    for grade in [prelim_exam, quizzes, requirements, recitation]:
        if grade < 0 or grade > 100:
            print("Invalid input. Grades should be between 0 and 100.")
            grade = float(input("Please enter a valid grade: "))

attendance = 100 - (absences * 10)
class_standing = (quizzes * 0.40) + (requirements * 0.30) + (recitation * 0.30)
prelim_grade = (prelim_exam * 0.60) + (attendance * 0.10) + (class_standing * 0.30)
print(f"Prelim Grade: {prelim_grade:.2f}")
overall_grade = lambda prelim, midterm, final: (prelim * 0.20) + (midterm * 0.30) + (final * 0.50)

# For passing grade (overall 75)
required_midterm_pass = (75 - (prelim_grade * 0.20)) / 0.80
required_final_pass = (75 - (prelim_grade * 0.20)) / 0.50

# For Dean's Lister (overall 90)
required_midterm_deans = (90 - (prelim_grade * 0.20)) / 0.80
required_final_deans = (90 - (prelim_grade * 0.20)) / 0.50

# Output results
print(f"To pass with 75%, you need a Midterm grade of {required_midterm_pass:.2f} and a Final grade of {required_final_pass:.2f}.")
print(f"To achieve 90%, you need a Midterm grade of {required_midterm_deans:.2f} and a Final grade of {required_final_deans:.2f}.")

from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    try:
        # Retrieve form data
        absences = int(request.form['absences'])
        prelim_exam = float(request.form['prelim_exam'])
        quizzes = float(request.form['quizzes'])
        requirements = float(request.form['requirements'])
        recitation = float(request.form['recitation'])

        # Check if absences exceed the allowed threshold (4 or more fails the student)
        if absences >= 4:
            return "FAILED due to absences (4 or more absences)."

        # Attendance calculation
        attendance = 100 - (absences * 10)

        # Class standing calculation
        class_standing = (0.40 * quizzes) + (0.30 * requirements) + (0.30 * recitation)

        # Prelim grade calculation
        prelim_grade = (0.60 * prelim_exam) + (0.10 * attendance) + (0.30 * class_standing)

        # Grade requirement calculations
        required_midterm_pass = (75 - (0.20 * prelim_grade)) / 0.30
        required_final_pass = (75 - (0.20 * prelim_grade) - (0.30 * required_midterm_pass)) / 0.50

        required_midterm_dl = (90 - (0.20 * prelim_grade)) / 0.30
        required_final_dl = (90 - (0.20 * prelim_grade) - (0.30 * required_midterm_dl)) / 0.50

        return (f"Prelim Grade: {prelim_grade:.2f}<br>"
                f"To pass with 75%, you need a Midterm grade of {required_midterm_pass:.2f} and a Final grade of {required_final_pass:.2f}.<br>"
                f"To achieve 90%, you need a Midterm grade of {required_midterm_dl:.2f} and a Final grade of {required_final_dl:.2f}.")
    
    except ValueError:
        return "Invalid input! Please enter valid numerical values."

if __name__ == '__main__':
    app.run(debug=True)
