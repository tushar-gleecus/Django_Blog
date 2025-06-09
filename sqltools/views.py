import csv
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def sql_to_csv(sql_file_path, csv_file_path):
    # Example function: Extract table CREATEs and write to csv (update for real parsing)
    # For demo: Just writes SQL lines to a single-column CSV
    with open(sql_file_path, 'r') as infile, open(csv_file_path, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['SQL Line'])
        for line in infile:
            writer.writerow([line.strip()])

def sql_summary_upload(request):
    if request.method == 'POST' and request.FILES['sqlfile']:
        sql_file = request.FILES['sqlfile']
        fs = FileSystemStorage()
        filename = fs.save(sql_file.name, sql_file)
        uploaded_file_path = fs.path(filename)
        csv_file_path = os.path.splitext(uploaded_file_path)[0] + '.csv'

        # Here, use your real sql-to-csv logic!
        sql_to_csv(uploaded_file_path, csv_file_path)

        # Prepare for download
        with open(csv_file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(csv_file_path)}"'
            return response

    return render(request, 'sqltools/sql_summary.html')
