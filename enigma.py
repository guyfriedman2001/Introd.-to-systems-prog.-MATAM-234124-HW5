
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
