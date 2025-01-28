from app import update_portfolio

if __name__ == "__main__": # Handles any potential errors
    try:
        update_portfolio()
        print("Portfolio updated successfully.")
    except Exception as e:
        print(f"An error occurred during portfolio update: {e}")