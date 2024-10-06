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
        # print(query, [Sub_Topic, Level, number_of_questions])

        cursor.execute(query, [Sub_Topic, Level, number_of_questions])
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows

def create_question_paper(request):
    if request.method == 'POST':
        form = QuestionPaperForm(request.POST)
        if form.is_valid():
            Topic = form.cleaned_data['Topic']
            Sub_Topic = form.cleaned_data['Sub_Topic']
            Level = form.cleaned_data['Level']
            number_of_questions = form.cleaned_data['number_of_questions']

            # Construct the table name dynamically based on the topic
            table_name = Topic.lower().replace(" ", "_")  # e.g., 'Data Types' becomes 'data_types'

            # Fetch questions from the dynamically accessed table
            questions = fetch_questions_from_dynamic_table(table_name, Sub_Topic, Level, number_of_questions)


            # # Fetch the filtered questions from the PostgreSQL database
            # questions = Question.objects.filter(
            #     Topic=Topic,
            #     Sub_Topic=Sub_Topic,
            #     Level=Level
            # )[:number_of_questions]  # Limit to the number of questions requested

            # print(questions) 

            return render(request, 'question_paper.html', {'questions': questions, 'form': form})

    else:
        form = QuestionPaperForm()

    return render(request, 'create_question_paper.html', {'form': form})