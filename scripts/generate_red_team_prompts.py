import subprocess

scripts = ["script_raw_data.py", "script_copy_data.py", "script_generate_db.py"]

for script in scripts:
    try:
        print(f"Running {script}...")
        result = subprocess.run(
            ["python", script],
            check=True,
        )
        print(f"{script} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {script}. Exiting.")
        print(f"Error details: {e}")
        break
