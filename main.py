import tkinter as tk
from mysql.connector import connect, Error


# Function to clear all text fields on the record page
def clear_text():
    name_box.delete(1.0, tk.END)
    breed_box.delete(1.0, tk.END)
    age_box.delete(1.0, tk.END)
    owner_box.delete(1.0, tk.END)


# Function to handle the submit button on the record page
def submit_data():
    name = name_box.get(1.0, tk.END).strip()
    breed = breed_box.get(1.0, tk.END).strip()
    age = age_box.get(1.0, tk.END).strip()
    owner = owner_box.get(1.0, tk.END).strip()

    if not name or not breed or not age or not owner:
        print("Please fill out all fields!")
        return

    try:
        with connect(
                host="localhost",
                user="root",
                password="",
                database="pets",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO furbaby (name, breed, age, owner) VALUES (%s, %s, %s, %s)",
                    (name, breed, age, owner),
                )
                connection.commit()
                print("Data submitted successfully!")
    except Error as e:
        print(f"Error: {e}")

    clear_text()
    show_page(records_frame)
    show_all_records()


# Function to retrieve and display names as buttons
def show_all_records():
    try:
        with connect(
                host="localhost",
                user="root",
                password="",
                database="pets",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, breed, age, owner FROM furbaby")
                records = cursor.fetchall()
                for widget in records_frame.winfo_children():
                    widget.destroy()
                # Heading for the records page
                records_heading = tk.Label(records_frame, text="Pet Records", font=("Arial", 18, "bold"))
                records_heading.pack(pady=20)

                # Back button for the records page
                go_back_button_records = tk.Button(records_frame, text="Go Back", font=("Arial", 12),
                                                   command=lambda: show_page(welcome_frame))
                go_back_button_records.pack(pady=10)

                if records:
                    for record in records:
                        record_id, name, breed, age, owner = record
                        btn = tk.Button(
                            records_frame,
                            text=name,
                            font=("Arial", 12),
                            command=lambda r=record: show_pet_details(r),
                        )
                        btn.pack(pady=5)
                else:
                    tk.Label(records_frame, text="No records found.", font=("Arial", 14)).pack()
    except Error as e:
        print(f"Error: {e}")


# Function to display reminders based on breed and age
def show_breed_reminders(breed, age):
    breed = breed.lower()
    reminders = ""
    total_months = 0

    # Parse the age input into total months
    try:
        age = age.lower()
        if "year" in age or "month" in age:
            years = 0
            months = 0

            # Extract years
            if "year" in age:
                years_part = age.split("year")[0].strip()
                years = int(years_part) if years_part.isdigit() else 0

            # Extract months
            if "month" in age:
                months_part = age.split("month")[0].split()[-1].strip()
                months = int(months_part) if months_part.isdigit() else 0

            total_months = years * 12 + months
        else:
            total_months = int(age) * 12  # Fallback if given as a number
    except ValueError:
        total_months = -1  # Invalid input

    # General cat care reminders
    if "cat" in breed or breed in ["persian", "siamese", "bengal", "sphynx"]:
        reminders = "Cat Care Reminders:\n"
        if total_months < 0:
            reminders += "- Unable to determine vet visit frequency due to invalid age.\n"
        elif total_months < 12:
            reminders += "- Visit the vet very often during the first six months.\n"
        elif total_months < 120:
            reminders += "- Visit the vet once a year.\n"
        else:
            reminders += "- Visit the vet twice a year.\n"

        reminders += (
            "- Give required Vitamin B12 (Cobalamin) amount to your pet\n"
            "- Provide scratching posts and toys for enrichment.\n"
            "- Clean the litter box daily.\n"
            "- Maintain a balanced diet with appropriate portion sizes.\n"
            "- Provide required worm tablets every 3 months\n"
            "- Inject the needed medications such as Rabies, Feline leukemia virus (FeLV), Feline calicivirus\n"
        )

    # General dog care reminders
    elif "dog" in breed or breed in ["labrador", "poodle", "bulldog", "beagle"]:
        reminders = "Dog Care Reminders:\n"
        if total_months < 0:
            reminders += "- Unable to determine vet visit frequency due to invalid age.\n"
        elif total_months < 12:
            reminders += "- Puppies need frequent vet visits during the first year.\n"
            reminders += "- Socialization and training are essential during this time.\n"
        elif total_months < 84:
            reminders += "- Visit the vet annually for routine check-ups.\n"
            reminders += "- Ensure regular exercise and a balanced diet.\n"
        else:
            reminders += "- For senior dogs, visit the vet twice a year.\n"
            reminders += "- Monitor for signs of arthritis or other age-related issues.\n"

        reminders += (
            "- Provide Vetzyme B Plus E Dog Vitamin to your pet\n"
            "- Schedule regular walks and exercise.\n"
            "- Provide chew toys for dental health.\n"
            "- Maintain a grooming routine (bathing, nail trimming).\n"
            "- Provide required worm tablets every 3 months\n"
            "- Inject the needed medications such as Leptospirosis, Rabies, Distemper\n"
        )

    # For unknown breeds
    else:
        reminders = f"No specific reminders found for the breed: {breed.title()}"

    return reminders



# Function to display pet details and breed-specific reminders
def show_pet_details(record):
    record_id, name, breed, age, owner = record
    reminders = show_breed_reminders(breed, age)
    details_label.config(
        text=(f"Name: {name}\n"
              f"Breed: {breed}\n"
              f"Age: {age}\n"
              f"Owner: {owner}\n\n"
              f"{reminders}")
    )
    # Store the record id globally to use it when updating
    global pet_to_update
    pet_to_update = record
    show_page(details_frame)


# Function to show a specific page and hide others
def show_page(page_to_show):
    for page in pages:
        page.pack_forget()
    page_to_show.pack(fill="both", expand=True)


# Function to populate the update form with pet details
def load_update_form():
    # Fetch details of the pet to update
    record_id, name, breed, age, owner = pet_to_update
    name_box_update.delete(1.0, tk.END)
    breed_box_update.delete(1.0, tk.END)
    age_box_update.delete(1.0, tk.END)
    owner_box_update.delete(1.0, tk.END)

    name_box_update.insert(tk.END, name)
    breed_box_update.insert(tk.END, breed)
    age_box_update.insert(tk.END, age)
    owner_box_update.insert(tk.END, owner)

    show_page(update_frame)


# Function to handle the update submission
def update_pet_record():
    # Get values from the update form
    name = name_box_update.get(1.0, tk.END).strip()
    breed = breed_box_update.get(1.0, tk.END).strip()
    age = age_box_update.get(1.0, tk.END).strip()
    owner = owner_box_update.get(1.0, tk.END).strip()

    if not name or not breed or not age or not owner:
        print("Please fill out all fields!")
        return

    try:
        with connect(
                host="localhost",
                user="root",
                password="",
                database="pets",
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE furbaby SET name=%s, breed=%s, age=%s, owner=%s WHERE id=%s",
                    (name, breed, age, owner, pet_to_update[0]),
                )
                connection.commit()
                print("Data updated successfully!")
    except Error as e:
        print(f"Error: {e}")

    show_page(records_frame)
    show_all_records()


# Create main root window
root = tk.Tk()
root.geometry("1000x600")
root.title("Fur Baby Record.exe")

# List of all frames (pages)
pages = []

# Welcome page
welcome_frame = tk.Frame(root)
pages.append(welcome_frame)

welcome_label = tk.Label(welcome_frame, text="Welcome to the Fur Baby Records", font=("Arial", 20, "bold"))
welcome_label.pack(pady=30)

start_button = tk.Button(welcome_frame, text="Proceed to Add Record", font=("Arial", 14),
                         command=lambda: show_page(record_frame))
start_button.pack(pady=20)

view_button = tk.Button(welcome_frame, text="View All Records", font=("Arial", 14),
                        command=lambda: [show_page(records_frame), show_all_records()])
view_button.pack(pady=10)

# Record page
record_frame = tk.Frame(root)
pages.append(record_frame)

record_heading = tk.Label(record_frame, text="Add Pet Record", font=("Arial", 18, "bold"))
record_heading.pack(pady=20)

name_label = tk.Label(record_frame, text="Name", font=("Arial", 14))
name_label.pack(pady=5)
name_box = tk.Text(record_frame, height=2, font=("Arial", 16))
name_box.pack(pady=5)

breed_label = tk.Label(record_frame, text="Breed", font=("Arial", 14))
breed_label.pack(pady=5)
breed_box = tk.Text(record_frame, height=2, font=("Arial", 16))
breed_box.pack(pady=5)

age_label = tk.Label(record_frame, text="Age", font=("Arial", 14))
age_label.pack(pady=5)
age_box = tk.Text(record_frame, height=2, font=("Arial", 16))
age_box.pack(pady=5)

owner_label = tk.Label(record_frame, text="Owner's Name", font=("Arial", 14))
owner_label.pack(pady=5)
owner_box = tk.Text(record_frame, height=2, font=("Arial", 16))
owner_box.pack(pady=5)

submit_button = tk.Button(record_frame, text="Submit", font=("Arial", 12), command=submit_data)
submit_button.pack(pady=10)

go_back_button = tk.Button(record_frame, text="Go Back", font=("Arial", 12), command=lambda: show_page(welcome_frame))
go_back_button.pack(pady=10)

# Records page
# Records page
records_frame = tk.Frame(root)
pages.append(records_frame)

# Heading for the records page
records_heading = tk.Label(records_frame, text="Pet Records", font=("Arial", 18, "bold"))
records_heading.pack(pady=2)

# Scrollable area for pet records
records_list_frame = tk.Frame(records_frame)
records_list_frame.pack(fill="both", expand=True)

# Back button for the records page, placed at the bottom
go_back_button_records = tk.Button(
    records_frame,
    text="Go Back",
    font=("Arial", 12),
    command=lambda: show_page(welcome_frame)
)
go_back_button_records.pack(side="bottom", pady=10, anchor="s")


# Details page
details_frame = tk.Frame(root)
pages.append(details_frame)

details_heading = tk.Label(details_frame, text="Pet Details", font=("Arial", 18, "bold"))
details_heading.pack(pady=20)

details_label = tk.Label(details_frame, text="", font=("Arial", 14), justify="left")
details_label.pack(pady=10)

update_button = tk.Button(details_frame, text="Update Record", font=("Arial", 12), command=load_update_form)
update_button.pack(pady=10)

go_back_button_details = tk.Button(details_frame, text="Back", font=("Arial", 12),
                                   command=lambda: show_page(records_frame))
go_back_button_details.pack(pady=10)

# Update frame
update_frame = tk.Frame(root)
pages.append(update_frame)

update_label = tk.Label(update_frame, text="Update Pet Record", font=("Arial", 18, "bold"))
update_label.pack(pady=10)

name_label_update = tk.Label(update_frame, text="Name", font=("Arial", 14))
name_label_update.pack(pady=5)
name_box_update = tk.Text(update_frame, height=2, font=("Arial", 16))
name_box_update.pack(pady=5)

breed_label_update = tk.Label(update_frame, text="Breed", font=("Arial", 14))
breed_label_update.pack(pady=5)
breed_box_update = tk.Text(update_frame, height=2, font=("Arial", 16))
breed_box_update.pack(pady=5)

age_label_update = tk.Label(update_frame, text="Age", font=("Arial", 14))
age_label_update.pack(pady=5)
age_box_update = tk.Text(update_frame, height=2, font=("Arial", 16))
age_box_update.pack(pady=5)

owner_label_update = tk.Label(update_frame, text="Owner's Name", font=("Arial", 14))
owner_label_update.pack(pady=5)
owner_box_update = tk.Text(update_frame, height=2, font=("Arial", 16))
owner_box_update.pack(pady=5)

update_submit_button = tk.Button(update_frame, text="Update", font=("Arial", 12), command=update_pet_record)
update_submit_button.pack(pady=10)

go_back_button_update = tk.Button(update_frame, text="Cancel", font=("Arial", 12),
                                  command=lambda: show_page(details_frame))
go_back_button_update.pack(pady=10)

# Start the app by showing the welcome page
show_page(welcome_frame)

# Run the application
root.mainloop()