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


def is_even(number : int) -> bool: return number % 2 == 0
def is_odd(number : int) -> bool: return not is_even(number)
def is_zero(number : int) -> bool: return number == 0
def make_double(number : int) -> int: return number * 2
def increment(number : int) -> int: return number + 1
def decrement(number : int) -> int: return number - 1

class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheel1 = wheels[WHEEL1_POSITION]
        self.wheel2 = wheels[WHEEL2_POSITION]
        self.wheel3 = wheels[WHEEL3_POSITION]
        self._original_state_wheel1 = wheels[WHEEL1_POSITION]
        self._original_state_wheel2 = wheels[WHEEL2_POSITION]
        self._original_state_wheel3 = wheels[WHEEL3_POSITION]
        self.reflector_map = reflector_map
        pass

    @staticmethod
    def next_val_wheel1(current_value : int) -> int: return increment((current_value % WHEEL1_CYCLE_LIMIT))

    @staticmethod
    def next_val_wheel2(current_value : int, encrypted_characters_counter : int) -> int: 
        if is_odd(encrypted_characters_counter):
            return decrement(current_value)
        return make_double(current_value)

    @staticmethod
    def next_val_wheel3(encrypted_characters_counter : int) -> int: 
        next_value = DEFAULT_WHEEL3
        if is_zero(encrypted_characters_counter % STATE1_WHEEL3_CONDITION):
            next_value = STATE1_WHEEL3
        elif is_zero(encrypted_characters_counter % STATE2_WHEEL3_CONDITION):
            next_value = STATE2_WHEEL3
        return next_value

    def update_wheels(self,encrypted_characters_counter : int) -> None:
        self.wheel1 = self.next_val_wheel1(self.wheel1)
        self.wheel2 = self.next_val_wheel2(self.wheel2,encrypted_characters_counter)
        self.wheel3 = self.next_val_wheel3(encrypted_characters_counter)

    def calculate_special_formula(self) -> int: return (((make_double(self.wheel1))-self.wheel2+self.wheel3)%ALPHABET_SIZE)

    def special_formula_condition(self) -> bool: return not is_zero(self.calculate_special_formula())
    
    def modulo_for_i(self,current_val_i : int) -> int:
        return current_val_i % ALPHABET_SIZE
    
    def next_val_i(self, current_val_i : int) -> int:
        i_increment = 1
        if self.special_formula_condition():
            i_increment = self.calculate_special_formula()
        return current_val_i + i_increment
        

    def reset_wheels(self) -> None:
        self.wheel1 = self._original_state_wheel1
        self.wheel2 = self._original_state_wheel2
        self.wheel3 = self._original_state_wheel3

    def calculate_char_encryption(self, char : str) -> str: return char #TODO

    def encrypt(self, message : str) -> str:
        encrypted_message = ''
        encrypted_characters_counter = 0
        for char in message:
            i = self.next_val_i(i)
            i = self.modulo_for_i(i)
            next_char = char
            if 'a' <= char <= 'z':
                next_char = self.calculate_char_encryption(char)
                encrypted_characters_counter = increment(encrypted_characters_counter)
            self.update_wheels()
            encrypted_message += next_char

        
        self.reset_wheels()
        return encrypted_message




    def load_enigma_from_path(path):
        pass

class JSONFileException(Exception):
    def __init__(self, message):
        super().__init__(message)