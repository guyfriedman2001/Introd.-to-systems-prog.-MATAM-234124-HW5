import json
import sys

ALPHABET_SIZE = 26
WHEEL1_CYCLE_LIMIT = 8

WHEEL1_POSITION = 0
WHEEL2_POSITION = 1
WHEEL3_POSITION = 2

DEFAULT_WHEEL3 = 0
STATE1_WHEEL3_CONDITION = 10
STATE1_WHEEL3 = 10
STATE2_WHEEL3_CONDITION = 3
STATE2_WHEEL3 = 5

PLUS_OPERATION = 1
MINUS_OPERATION = -1

def is_even(number : int) -> bool: 
    """Checks if a number is even.""" 
    return number % 2 == 0
def is_odd(number : int) -> bool: 
    """Checks if a number is odd.""" 
    return not is_even(number)
def is_zero(number : int) -> bool:
    """Checks if a number is zero.""" 
    return number == 0
def make_double(number : int) -> int: 
    """Returns twice the given number.""" 
    return number * 2
def increment(number : int) -> int: 
    """Increments the given number by one.""" 
    return number + 1
def decrement(number : int) -> int: 
    """Decrements the given number by one.""" 
    return number - 1

class Enigma:
    def __init__(self, hash_map : dict, wheels : list, reflector_map : dict):
        """Initializes the Enigma machine with mappings and wheel settings."""
        self.hash_map = hash_map
        self.wheel1 = wheels[WHEEL1_POSITION]
        self.wheel2 = wheels[WHEEL2_POSITION]
        self.wheel3 = wheels[WHEEL3_POSITION]
        self._original_state_wheel1 = self.wheel1
        self._original_state_wheel2 = self.wheel2
        self._original_state_wheel3 = self.wheel3
        self.reflector_map = reflector_map
        pass

    @staticmethod
    def next_val_wheel1(current_value : int) -> int: 
        """Calculates the next position of wheel 1.""" 
        return increment((current_value % WHEEL1_CYCLE_LIMIT))

    @staticmethod
    def next_val_wheel2(current_value : int, encrypted_characters_counter : int) -> int:
        """Calculates the next position of wheel 2 based on the encryption progress."""
        if is_odd(encrypted_characters_counter):
            return decrement(current_value)
        return make_double(current_value)

    @staticmethod
    def next_val_wheel3(encrypted_characters_counter : int) -> int:
        """Determines the next value for wheel 3 based on conditions."""
        next_value = DEFAULT_WHEEL3
        if is_zero(encrypted_characters_counter % STATE1_WHEEL3_CONDITION):
            next_value = STATE1_WHEEL3
        elif is_zero(encrypted_characters_counter % STATE2_WHEEL3_CONDITION):
            next_value = STATE2_WHEEL3
        return next_value

    def update_wheels(self,encrypted_characters_counter : int) -> None:
        """Updates the positions of the wheels after each encryption step."""
        self.wheel1 = self.next_val_wheel1(self.wheel1)
        self.wheel2 = self.next_val_wheel2(self.wheel2,encrypted_characters_counter)
        self.wheel3 = self.next_val_wheel3(encrypted_characters_counter)

    def calculate_special_formula(self) -> int: 
        """Computes a transformation value used in the encryption process.""" 
        return (((make_double(self.wheel1))-self.wheel2+self.wheel3)%ALPHABET_SIZE)

    def special_formula_condition(self) -> bool: 
        """Checks whether the special formula yields a nonzero result.""" 
        return not is_zero(self.calculate_special_formula())
        
    def reset_wheels(self) -> None:
        """Resets the wheels to their initial states."""
        self.wheel1 = self._original_state_wheel1
        self.wheel2 = self._original_state_wheel2
        self.wheel3 = self._original_state_wheel3

    def cycle(self, char : str, operation : int) -> str:
        """Applies a transformation cycle to a character."""
        i = self.hash_map[char]
        temp_calculation = self.calculate_special_formula()
        i += temp_calculation*operation if temp_calculation != 0 else operation
        i = i % ALPHABET_SIZE
        return [key for key, val in self.hash_map.items() if val == i][0]

    def encrypt(self, message : str) -> str:
        """Encrypts a given message."""
        encrypted_message = ''
        encrypted_characters_counter = 0
        for char in message:
            encrypted_char = char
            if char in self.hash_map:
                c1 = self.cycle(char, PLUS_OPERATION)
                c2 = self.reflector_map[c1]
                encrypted_char = self.cycle(c2, MINUS_OPERATION)
                encrypted_characters_counter = increment(encrypted_characters_counter)
            encrypted_message += encrypted_char
            self.update_wheels(encrypted_characters_counter)
        self.reset_wheels()
        return encrypted_message

def load_enigma_from_path(path : str) -> Enigma:
    """Loads an Enigma machine configuration from a JSON file."""
    try:
        with open(path, 'r') as file:
            loaded_data = json.load(file)
            hash_map = loaded_data["hash_map"]
            wheels = loaded_data["wheels"]
            reflector_map = loaded_data["reflector_map"]
            return Enigma(hash_map, wheels, reflector_map)
    except (KeyError, OSError, json.JSONDecodeError, FileNotFoundError):
        raise JSONFileException()

class JSONFileException(Exception):
    """Exception raised for errors in JSON file loading."""
    def __init__(self):
        self.message = "The enigma script has encountered an error"

if __name__ == "__main__":
    """Handles command-line arguments and runs the Enigma encryption process."""
    flags = ["-c", "-i", "-o"]
    try:
        input_list = sys.argv[1:]
        data = {}
        check_invalid = False
        for i in range(0, len(input_list), 2) :
            if input_list[i] in flags :
                data[input_list[i]] = input_list[i+1]
            else:
                check_invalid = True
        if "-c" not in data or "-i" not in data or check_invalid:
                print("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>", file=sys.stderr)
                exit(1)
        config_file = data["-c"]
        input_file = data["-i"]
        output_file = data["-o"] if "-o" in data else sys.stdout
        enigma = load_enigma_from_path(config_file)
        out_file = open(output_file, 'w') if output_file != sys.stdout else sys.stdout
        with open(input_file, 'r') as in_file:
            for line in in_file:
                out_file.write(enigma.encrypt(line))
        if output_file != sys.stdout:
            out_file.close()
    except (JSONFileException, IndexError, KeyError, OSError):
        print("The enigma script has encountered an error")
        exit(1)