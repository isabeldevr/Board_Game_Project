import traceback
import easygui

FILE_PATH = "leaderboard.txt"

def leaderboard_append(name, points):
    """ Append a new record to the leaderboard
    Input: name (str) - the name of the player
           points (int) - the number of points the player has
    Output: None
    Time Complexity: O(1) """
    name = ''.join([char for char in name if char != ' '])

    try:
        with open(FILE_PATH, 'a') as file:
            # Add new name score pair to the file
            file.write(f"{name} {points}\n")

    except Exception as e:
        print(f"Error reading leaderboard: {e}, {traceback.print_exc()}")


def leaderboard_read():
    """ Read the leaderboard
    Input: None
    Output: records (list) - a list of records
    Time Complexity: O(n) """
    try:
        # Creating an empty list to store the records
        records = []
        with open(FILE_PATH, 'r') as file:
            for line in file:
                # We split each line into name and points using whitespace as a separator
                name, points = line.strip().split()
                records.append((name, int(points)))
            return records

    except Exception as e:
        print(f"Error reading leaderboard: {e}, {traceback.print_exc()}")
        return []


def merge_sort(records) -> list:
    """ Sort a list of records using merge sort
    Input: records (list) - a list of records
    Output: sorted_records (list) - a sorted list of records
    Time Complexity: O(n log n) """
    if len(records) <= 1:
        return records

    # Split the list in two
    mid = len(records) // 2
    left_half = records[:mid]
    right_half = records[mid:]

    # Recursively sort each half
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Merge the halves
    sorted_records = merge(left_half, right_half)
    return sorted_records


def merge(left, right) -> list:
    """ Merge two sorted lists
    Input: left (list) - the left half
           right (list) - the right half
    Output: merged (list) - the merged list
    Time Complexity: O(n) """
    merged = []
    i = j = 0

    # Compare the elements of the two halves
    while i < len(left) and j < len(right):
        if left[i][1] > right[j][1]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Add the remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


class LeaderboardUI:
    def __init__(self):
        self.leaderboard = []

    def populate_leaderboard(self) -> None:
        """ Populate the leaderboard with the records
        Input: None
        Output: None
        Time Complexity: O(n log n) because of merge sort"""
        records = leaderboard_read()
        sorted_records = merge_sort(records)

        leaderboard_text = "\n".join([f"{index + 1}. {record[0]} - {record[1]} points" for index, record in enumerate(sorted_records)])
        if leaderboard_text == "":
            leaderboard_text = "No records yet! Play a game to add a record."
        easygui.msgbox(leaderboard_text, "Leaderboard")

        
    def submit_score(self, points, name) -> None:
        """ Submit the score to the leaderboard
        Input: points (int) - the number of points the player has
        Output: None
        Time Complexity: O(1)"""
        if name:
            leaderboard_append(name, points)
            self.populate_leaderboard()


    def quit_leaderboard(self) -> None:
        """ Function to quit the leaderboard
        Input: None
        Output: None
        Time Complexity: O(1)"""
        easygui.msgbox("Goodbye! :)")
        quit()


    def show_leaderboard_options(self, points, game_over, name) -> None:
        """ Show options for the leaderboard
        Input: None
        Output: None
        Time Complexity: O(1)"""
        choices = ["Submit Score", "View Leaderboard", "Quit"]
        choice = easygui.buttonbox("Select an option", "Leaderboard Options", choices=choices)

        if choice == "Submit Score":
            if game_over == False:
                easygui.msgbox("You can't submit a score if the game is not over!")
            else:
                self.submit_score(points, name)
        elif choice == "View Leaderboard":
            self.populate_leaderboard()
        elif choice == "Quit":
            self.quit_leaderboard()
