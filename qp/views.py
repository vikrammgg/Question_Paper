from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
from .forms import QuestionPaperForm
from django.db import connection

# Create your views here.

def home(request):
    return render(request, 'home.html')

def add(request):
    return render(request, 'add.html')

# def fetch_questions_from_dynamic_table(table_name, Sub_Topic, Level, number_of_questions):
#     """
#     Fetch questions from the dynamic table based on filters.
#     """
#     with connection.cursor() as cursor:
#         query = f"""
#             SELECT * FROM "{table_name}"
#             LOWER("Sub_Topic") = LOWER(%s) AND LOWER("Level") = LOWER(%s)
#             LIMIT %s;
#         """
#         # print(query, [Sub_Topic, Level, number_of_questions])

#         cursor.execute(query, [Sub_Topic, Level, number_of_questions])
#         columns = [col[0] for col in cursor.description]
#         rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
#     return rows

# def create_question_paper(request):
#      # Initialize session storage for questions if it doesn't exist
#     if 'questions' not in request.session:
#         request.session['questions'] = []

#     if request.method == 'POST':
#         form = QuestionPaperForm(request.POST)
#         if form.is_valid():
#             Topic = form.cleaned_data['Topic']
#             Sub_Topic = form.cleaned_data['Sub_Topic']
#             Level = form.cleaned_data['Level']
#             number_of_questions = form.cleaned_data['number_of_questions']

#             # Construct the table name dynamically based on the topic
#             table_name = Topic.lower().replace(" ", "_")  # e.g., 'Data Types' becomes 'data_types'

#            # Fetch new questions based on filters
#             new_questions = fetch_questions_from_dynamic_table(table_name, Sub_Topic, Level, number_of_questions)

#             # Add questions to the existing session list
#             questions = request.session['questions']
#             questions.extend(new_questions)

#             # Save updated questions list to session
#             request.session['questions'] = questions

#              # Check if "Add Questions" or "Create Paper" was pressed
#             if request.POST.get('action') == 'add_questions':
#                 # Re-render the form, allowing more questions to be added
#                 return render(request, 'create_question_paper.html', {'form': form})

#             elif request.POST.get('action') == 'create_paper':
#                 # Render the question paper with all questions added so far
#                 return render(request, 'question_paper.html', {'questions': request.session['questions'], 'form': form})

#     else:
#         form = QuestionPaperForm()

#     return render(request, 'create_question_paper.html', {'form': form})

def fetch_questions_from_dynamic_table(table_name, Sub_Topic, Level, number_of_questions):
    """
    Fetch questions from the dynamic table based on filters.
    """
    with connection.cursor() as cursor:
        query = f"""
            SELECT * FROM "{table_name}"
            WHERE "Sub_Topic" = %s AND "Level" = %s
            LIMIT %s;
        """
        # Execute the query with parameterized values for security
        cursor.execute(query, [Sub_Topic, Level, number_of_questions])
        
        # Fetching column names
        columns = [col[0] for col in cursor.description]
        
        # Fetching all rows and converting them into a dictionary
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        # Debug: Print the resulting rows to see what is being fetched
        print("Fetched Rows: ", rows)
        
    return rows

def create_question_paper(request):
    # Initialize session storage for questions if it doesn't exist
    if 'questions' not in request.session:
        request.session['questions'] = []

    if request.method == 'POST':
        form = QuestionPaperForm(request.POST)
        if form.is_valid():
            Topic = form.cleaned_data['Topic']
            Sub_Topic = form.cleaned_data['Sub_Topic']
            Level = form.cleaned_data['Level']
            number_of_questions = form.cleaned_data['number_of_questions']

            # Construct the table name dynamically based on the topic
            table_name = Topic.lower().replace(" ", "_")  # Ensure correct table name

            # Debug: Print topic details for verification
            # print(f"Fetching from table: {table_name}, Sub-Topic: {Sub_Topic}, Level: {Level}, Questions: {number_of_questions}")
            
            # Fetch new questions based on filters
            new_questions = fetch_questions_from_dynamic_table(table_name, Sub_Topic, Level, number_of_questions)

            # Add questions to the existing session list
            questions = request.session['questions']
            questions.extend(new_questions)

            # Save updated questions list to session
            request.session['questions'] = questions

            # Check if "Add Questions" or "Create Paper" was pressed
            if request.POST.get('action') == 'add_questions':
                return render(request, 'create_question_paper.html', {'form': form})

            elif request.POST.get('action') == 'create_paper':
                # Render the question paper with all questions added so far
                response = render(request, 'question_paper.html', {'questions': request.session['questions'], 'form': form})

                # Optionally clear the session once the paper is created
                request.session.flush()
                return response

    else:
        form = QuestionPaperForm()

    return render(request, 'create_question_paper.html', {'form': form})