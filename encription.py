import unicodedata
import json
from time import sleep


def reverse_and_remove_last(password):
    """Reverse the password and remove the last character."""
    password = password[::-1]
    taken_out = password.pop()  # Save the popped-out letter
    return password, taken_out

vowels_lst = []

def replace_vowels_with_ascii(password, vowels="aeiouAEIOU"):
    """Replace vowels with their ASCII values."""
    counter = 0
    for index, letter in enumerate(password):
        if letter in vowels:
            password[index] = ord(letter)
            vowels_lst.append((letter, counter))
        counter += 1
    return password

def save_the_vowels_indexes(encrypted_password, vowels_list):
    vowels_dict = {vowel: int(ind) for vowel, ind in vowels_list}

    try:
        # Read existing data if the file exists
        try:
            with open("vowels.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Add the new dictionary under the encrypted password key
        data["".join(map(str, encrypted_password))] = vowels_dict

        # Write updated data back to the file
        with open("vowels.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: {e}")

def split_and_swap(password):
    """Split the password in half and swap the second half."""
    mid_index = len(password) // 2
    half_list = password[: mid_index + 1]
    swapped_half = password[:mid_index:-1]
    return half_list + swapped_half


def asterisk_split(password):
    """Convert elements to strings, join with asterisks, and split back."""
    asterisk_string = "*".join(map(str, password)) + "*"
    new_list = []
    temp = ""

    for char in asterisk_string:
        if char == "*":
            if temp:
                new_list.append(int(temp) if temp.isdigit() else temp)
                temp = ""
            new_list.append("*")
        else:
            temp += char

    if temp:
        new_list.append(int(temp) if temp.isdigit() else temp)
    return new_list


def is_symbol(x):
    """Check if a character is a symbol."""
    return x.isprintable() and not x.isalnum()


def writing_form(symbol):
    """Return the Unicode name of a symbol."""
    try:
        return unicodedata.name(symbol)
    except ValueError:
        return "No Unicode name found for the symbol entered"


def short(extended):
    """Create a short form (abbreviation) from the Unicode name."""
    words = extended.split()
    if len(words) == 1:
        return words[0][:4].upper()
    return "".join(word[0] for word in words[:4]).upper()


def save_abbr_to_json(encrypted_password, abbr_list):
    """Save abbreviations to a JSON file under the name of the encrypted password."""
    abbr_dict = {short: long for short, long in abbr_list}

    try:
        # Read existing data if the file exists
        try:
            with open("abbr.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Add the new dictionary under the encrypted password key
        data["".join(map(str, encrypted_password))] = abbr_dict

        # Write updated data back to the file
        with open("abbr.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: {e}")


def save_taken_out_to_json(encrypted_password, taken_out):
    """Save the TAKENOUT letter to a separate JSON file."""
    try:
        # Read existing data if the file exists
        try:
            with open("taken_out.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Add the TAKENOUT letter under the encrypted password key
        data["".join(map(str, encrypted_password))] = taken_out

        # Write updated data back to the file
        with open("taken_out.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: {e}")


def process_password_elements(password, abbr_list):
    """Process password elements based on type."""
    for index, element in enumerate(password):
        if isinstance(element, int):
            if element % 2 == 0:
                password[index] = element**2
            elif element <= 10:
                password[index] = element + 9
            else:
                password[index] = element + 9
        elif is_symbol(element) and element != "*":
            extend_form = writing_form(element)
            short_form = short(extend_form)
            abbr_list.append((short_form, extend_form))
            password[index] = short_form
    return password


def main():
    # Input password
    raw_password = input("Password: ")
    password = list(raw_password)

    # First step
    password, taken_out = reverse_and_remove_last(password)
    password = replace_vowels_with_ascii(password)
    password = split_and_swap(password)
    password = asterisk_split(password)

    # Second step
    abbr_list = []
    password = process_password_elements(password, abbr_list)

    # Encrypt and print
    encrypted_password = password[::-1]
    print("Encrypting...")
    sleep(5)
    print("".join(map(str, encrypted_password)))

    # Save abbreviations and TAKENOUT to JSON files
    save_abbr_to_json(encrypted_password, abbr_list)
    save_taken_out_to_json(encrypted_password, taken_out)
    save_the_vowels_indexes(encrypted_password, vowels_lst)


if __name__ == "__main__":
    main()
