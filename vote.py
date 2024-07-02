import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


db_config = {
    'user': 'root',
    'password': 'ashu@123',
    'host': 'localhost',
    'database': 'voting_system'
}

try:
   
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

   
    def vote(candidate_name):
        query = "UPDATE votes SET vote_count = vote_count + 1 WHERE candidate_name = %s"
        cursor.execute(query, (candidate_name,))
        db.commit()
        messagebox.showinfo("Success", "Your vote has been recorded!")
        update_results()

   
    def reset_votes():
        if messagebox.askyesno("Confirm", "Are you sure you want to reset all votes?"):
            query = "UPDATE votes SET vote_count = 0"
            cursor.execute(query)
            db.commit()
            messagebox.showinfo("Reset", "All votes have been reset to zero.")
            update_results()

   
    def add_candidate():
        new_candidate = new_candidate_entry.get().strip()
        if new_candidate:
            query = "INSERT INTO votes (candidate_name, vote_count) VALUES (%s, 0)"
            cursor.execute(query, (new_candidate,))
            db.commit()
            messagebox.showinfo("Success", f"{new_candidate} has been added as a new candidate!")
            new_candidate_entry.delete(0, tk.END)  # Clear the entry field
            update_candidates()

    
    def delete_candidate(candidate_name):
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {candidate_name}?"):
            query = "DELETE FROM votes WHERE candidate_name = %s"
            cursor.execute(query, (candidate_name,))
            db.commit()
            messagebox.showinfo("Deleted", f"{candidate_name} has been deleted.")
            update_candidates()

    
    def update_candidates():
        for button_frame in candidate_frames:
            button_frame.destroy()  
        candidate_frames.clear()

        cursor.execute("SELECT candidate_name FROM votes")
        candidates = cursor.fetchall()
        for candidate in candidates:
            candidate_name = candidate[0]
            button_frame = tk.Frame(root)
            button_frame.pack()
            candidate_frames.append(button_frame)

            
            button = tk.Button(button_frame, text=candidate_name, bg=button_color, fg='white', padx=10, pady=5,
                               command=lambda name=candidate_name: vote(name))
            button.pack(side=tk.LEFT, padx=5, pady=5)

        
            delete_button = tk.Button(button_frame, text="Delete", bg='red', fg='white', padx=10, pady=5,
                                     command=lambda name=candidate_name: delete_candidate(name))
            delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    
    def update_results():
        cursor.execute("SELECT candidate_name, vote_count FROM votes")
        results = cursor.fetchall()
        results_text = "\n".join([f"{name}: {votes} votes" for name, votes in results])
        results_label.config(text=results_text)

    
    root = tk.Tk()
    root.title("Voting System")

    
    root.configure(bg='white')
    button_color = '#4CAF50'  
    label_color = '#2196F3'   

   
    new_candidate_label = tk.Label(root, text="New Candidate:", bg='white')
    new_candidate_label.pack(pady=(20, 5))

    new_candidate_entry = tk.Entry(root, width=30)
    new_candidate_entry.pack()

    add_candidate_button = tk.Button(root, text="Add Candidate", bg='orange', fg='white', padx=10, pady=5,
                                     command=add_candidate)
    add_candidate_button.pack(pady=5)

    
    candidate_frames = []

    
    update_candidates()


    reset_button = tk.Button(root, text="Reset Votes", bg='red', fg='white', padx=10, pady=5, command=reset_votes)
    reset_button.pack(pady=10)

    
    results_label = tk.Label(root, text="", bg=label_color, fg='white', padx=10, pady=10)
    results_label.pack(pady=20, fill=tk.X)

    
    update_results()

    root.mainloop()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    
    if 'db' in locals() and db.is_connected():
        cursor.close()
        db.close()
