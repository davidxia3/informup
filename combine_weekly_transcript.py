import os
from datetime import datetime

def combine_transcripts_between_dates(start_date_str, end_date_str, city_folder):
    start_date = datetime.strptime(start_date_str, "%Y_%m_%d")
    end_date = datetime.strptime(end_date_str, "%Y_%m_%d")
    
    combined_text = ""

    filenames = sorted([f for f in os.listdir(f"raw_transcripts/{city_folder}") if f.endswith(".txt")])

    for filename in filenames:
        if not filename.endswith(".txt"):
            continue
        
        try:
            file_date = datetime.strptime(filename.split('_')[0] + "_" + filename.split('_')[1] + "_" + filename.split('_')[2], "%Y_%m_%d")
        except (IndexError, ValueError):
            print("error parsing date")
            continue 

        if start_date <= file_date <= end_date:
            with open(os.path.join(f"raw_transcripts/{city_folder}", filename), 'r', encoding='utf-8') as f:
                combined_text += f.read() + "\n\n"

    output_filename = f"combined_transcripts/{city_folder}/{start_date_str}_to_{end_date_str}_combined.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(combined_text)

    print(f"Combined transcript written to {output_filename}")



combine_transcripts_between_dates("2025_05_26", "2025_05_30", "new_york_city")
