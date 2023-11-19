import os
import subprocess

def run_script(script_file):
    subprocess.run(["python", script_file], check=True)

if __name__ == "__main__":
    # Step 1: Run concat_data.py
    print("Step 1: Running concat_data.py")
    run_script("concat_data.py")
    print("All wx_data files concatenated")

    # Step 2: Run data_model.py
    if not os.path.exists("weather_data.db"):
        print("Step 2: Running data_model.py")
        run_script("data_model.py")
        print("Data model setup completed!")
    else:
        print("weather_data.db already exists. Skipping data_model.py")

    # Step 3: Run ingest_data.py
    print("Step 3: Running ingest_data.py")
    run_script("ingest_data.py")
    print("Completed loading weather station data for all dates/stations")

    # Step 4: Run aggregate_station_data.py
    print("Step 4: Running aggregate_station_data.py")
    run_script("aggregate_station_data.py")
    print("Station data aggreggation is complete by year with min&mean temps, total precipitation.")