
class Enigma:
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheel1 = wheels[0]
        self.wheel2 = wheels[1]
        self.wheel3 = wheels[2]
        self._original_state_wheel1 = wheels[0]
        self._original_state_wheel2 = wheels[1]
        self._original_state_wheel3 = wheels[2]
        self.reflector_map = reflector_map
        pass

    def next_val_wheel1(current_value : int) -> int: return (current_value % 8) + 1 #FIXME make dis static

    def next_val_wheel2(current_value : int,encrypted_characters : int) -> int: 
        next_value = 0
        if encrypted_characters % 10 == 0:
            next_value = 10
        elif encrypted_characters % 3 == 0:
            next_value = 5
        return next_value

    def next_val_wheel3(current_value : int) -> int: 
        return (current_value % 8) + 1

    def update_wheels(self,encrypted_characters : int) -> None:
        self.wheel1 = self.next_val_wheel1(self.wheel1)
        self.wheel2 = self.next_val_wheel2(self.wheel2,encrypted_characters)
        self.wheel3 = self.next_val_wheel3(self.wheel3,encrypted_characters)

    def wheels_arithmetics(self) -> bool:
        #TODO KOL HAKESEM HAZE - FUNCTION FROM 2 AND 7 SE I FIM
        return
    
    def modulo_for_i(self,current_val_1 : int) -> int:
        pass
    
    def next_val_i(self, current_val_1 : int) -> int: #FIXME SE I FIM 2 VE 3
        #TODO - MATEMATICA
        return
        



    def encrypt(self, message : str) -> str:
        encrypted_message = ''
        encrypted_characters = 0
        for char in message:
            i = self.next_val_i(i)
            next_char = char
            if 'a' <= char <= 'z':
                next_char = 'a'#helper function to get encrypted charachter
                encrypted_characters += 1
            '''
            else:
                pass
            '''
            next_char = next_char#no decryption
            encrypted_message+= char
            #TODO CREATE FOONKTZIA UPDATE WHEELZ
        
        self.reset_wheels()

        pass

def reset_wheels(self):
    self.wheel1 = self._original_state_wheel1
    self.wheel2 = self._original_state_wheel2
    self.wheel3 = self._original_state_wheel3


def load_enigma_from_path(path):
    pass
