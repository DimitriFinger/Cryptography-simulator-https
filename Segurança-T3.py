# Author: Dimitri da Silva Finger
# Sistemas de segurança
# 2021/1

import random
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# 1: random a generated 
#   a = 123705312412318916704247743587675603001627154551172868392175465183200784471918996863253192551547811473668156778008783691613079446343592061823441420292256291907063602243168905562636317108716473779802217627667873328989749104444477128445677107334922735974961431126411924656090058162704483844784149775442141726090
#
# 2: calculate A value using g^a mod p, then sent the value of A to teacher
#   A = AC4A952F24FEA263270ADD001C45265E189F2F4E19F13FDECD953019242A10F3E0FEC19BAD7244CA2EF3A73B03AC51B0B7ED36D517974BEAFD065C2FE6CA36573D40F50434DCBACDCC3FED0BDD60A131C4744721BF6B8118F1F8FAAB0D6CC6030401EAF264356C465F15625A41D46449C08D1CE81A0116EAB9E402142F6790F9
#
# 3: receive B value and message from teacher
#   B = 7B1DD90FD7313D59DF4065FD8F2CB7B29A2A40E7B556014C3821990C59D3F51EC0C43BE565DCA759D663C2027C65F88C7D506DF86A513C6436F5ECE274DB840A393CA6C5D6C66585EEB7C2FFD2E97A12008437B768F28501325633542FC7803FD341B00BFA8B9B91497D63948DA3DACAD356FCE1E2C998D6D750F9E37B031409
#   message = A478E62F9A8AE3F83DFBCD619DFA332483FF8E830CC958060947D518BB69EA3763D6FFECF82AA1784DD4EB34941198E8DCEED40F76CD94878F4B2C58AEDA0C8ED0F0E0DFA34F3F71B32FF0C5E2549A9FB21BEB2172FCD97F426755824370D2E3F05918CCC370851BF7206907519205ED3C4DF11AB24BD8E2EB498CEE57E2C2115A825F7687A9523805B644E1D63EF06B
#
# 4: calculate V value using B^a mod p
#   V = 56B99671DE71DF2BF43557DC2BEBC71F70A4BAC427011931C951B1F559A63740EEE04574E68A8F6091186C81A1A6271E13DC91946604040DD408156B6DC8EE9D2A2421DE1FC1A181DE771C477C398FDF7137F92DC8CEF3D8774BA50E84D9DDF3E581FDFA5C2DF96E5EB75413F688C83BA16774C42ACE899ACDD8500A768FA059
#
# 5: generate S value from SHA256(V), and use first 128bits as password 
#   S = B1FCF45EFA1765C79C7BE5E0D600E8AD096F5ECD65FCFE9436F23AF1E7CA101F
#   password = B1FCF45EFA1765C79C7BE5E0D600E8AD
#
# 6: decrypt message using AES at MODE_CBC, first 128bits are iv. Generenate unpadded decrypted message from remaining blocks 
#   plain text: Acho que agora foi :-). Um bit de diferença já invalida tudo. Manda esta msg de volta invertida e cifrada. Valeu
#
# 7: message is reversed and padded, then encrypted and sent to teacher
#   reversed_plain_text = uelaV .adarfic e aditrevni atlov ed gsm atse adnaM .odut adilavni \xc3\xa1j a\xc3\xa7nerefid ed tib mU .)-: iof aroga euq ohcA
#   hexadecimal_crypted_message = 12398AF616C99BA20FF21B1F4ED8A333FFA1B0394C365667B0D618710984FA15D7979547CE4B87ABA8B63809050C469CD4EB021C3919DC10259E474D30E5365E8A3FB3175C537C5C8ECDE8052C0C25CC9F64AB14B263BD51CF84272676B2BB5A3373790CE0E426DDE16C5E205AD393CEEF0B1473AEBD951446D4216C0F968E655CFC517AD9D87E490D775B42D656D636
# 
# 8: the new message received from teacher is decrypted for confirmatition
#   crypted_new_message = 5D7304AF32367F61317FF6392DA00AD45146E490E4E57694218E63FC25E01869B8845B390D17C28774971C9FE0390CB29310C45FBAF59B05246239CCDF2DC39F971C508E4BA470DBC3A9D3AA105EB147656DA5CD860AC61BE87FE88FC22338A278D4C2D7FA540032C092745D5382167578EEC9F1BEE2AABAAA961B5621FE2317
#   new_message = Foi mesmo :-). Agora comenta bem o código e coloca este exemplo completo no início do código. Show.
#


p_hexadecimal = "B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB06A3C69A6A9DCA52D23B616073E28675A23D189838EF1E2EE652C013ECB4AEA906112324975C3CD49B83BFACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE5644738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37DF365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371"
g_hexadecimal = "A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507FD6406CFF14266D31266FEA1E5C41564B777E690F5504F213160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28AD662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24855E6EEB22B3B2E5"

p_decimal = int(p_hexadecimal,16)
g_decimal = int(g_hexadecimal,16)


def generate_random_a_value(p_decimal):
    # a = random.randint(1,p_decimal-1)
    # first number generated by function above is mocked below
    return 123705312412318916704247743587675603001627154551172868392175465183200784471918996863253192551547811473668156778008783691613079446343592061823441420292256291907063602243168905562636317108716473779802217627667873328989749104444477128445677107334922735974961431126411924656090058162704483844784149775442141726090


# calculate A using random a, A = g_decimal^a mod p_decimal
def calculate_A(a, p, g):
    A_decimal = pow(g,a,p)
    A_hexadecimal = hex(A_decimal)    
    return A_hexadecimal[2:].upper()

# calculate B using B given by teacher and random a (same as before), B = g_decimal^a mod p_decimal
def calculate_V(B,a,p):
    B_decimal = int(B,16)
    return pow(B_decimal,a,p)

# calculate S value and generate hexadecimal password
def get_password(V):
    V_hexadecimal = hex(V)[2:]
    h = SHA256.new()
    h.update(bytes.fromhex(V_hexadecimal))
    S = h.hexdigest().upper()  
    print('\nS value:\n', S)    
    return S[:32]

# decrypt message given by teacher and unpad it, returning plain text
def AES_decrypt(message, password):
    bytes_message = bytes.fromhex(message)
    bytes_password = bytes.fromhex(password)
    iv = bytes_message[:16]
    cipher = AES.new(bytes_password, AES.MODE_CBC, iv)
    return unpadding(cipher.decrypt(bytes_message[16:]))

# unpad cipher and decode plain text
def unpadding(cipher):
    plain_text = cipher[:-cipher[len(cipher)-1]].decode()
    return plain_text

# pad message 
def padding(message):
    length = 16 - (len(message) % 16)
    message += bytes([length])*length  
    return message

# pad message, then concatenate iv with encrypted message
def AES_encrypt(message, password):
    message = padding(message)
    bytes_password = bytes.fromhex(password)
    iv = get_random_bytes(16)
    aes = AES.new(bytes_password, AES.MODE_CBC, iv)
    return iv + aes.encrypt(message)


if __name__ == "__main__":

    print("------------------------- First step -----------------------")

    a = generate_random_a_value(p_decimal)
    print("\nRandom a:\n", a)
    # a = 123705312412318916704247743587675603001627154551172868392175465183200784471918996863253192551547811473668156778008783691613079446343592061823441420292256291907063602243168905562636317108716473779802217627667873328989749104444477128445677107334922735974961431126411924656090058162704483844784149775442141726090
    
    # A_hexadeximal value sent to teacher
    A_hexadecimal = calculate_A(a,p_decimal,g_decimal)
    print("\nA hexadecimal:\n" + ' '.join([A_hexadecimal[i:i+8] for i in range(0, len(A_hexadecimal), 8)]))

    # B_hexadecimal value given by teacher
    B_hexadecimal = "7B1DD90FD7313D59DF4065FD8F2CB7B29A2A40E7B556014C3821990C59D3F51EC0C43BE565DCA759D663C2027C65F88C7D506DF86A513C6436F5ECE274DB840A393CA6C5D6C66585EEB7C2FFD2E97A12008437B768F28501325633542FC7803FD341B00BFA8B9B91497D63948DA3DACAD356FCE1E2C998D6D750F9E37B031409"
    print("\nB hexadecimal:\n" + ' '.join([B_hexadecimal[i:i+8] for i in range(0, len(B_hexadecimal), 8)]))

    V = calculate_V(B_hexadecimal, a, p_decimal)
    print("\nV value:\n", V)

    password = get_password(V)
    print("\nPassword: \n", password)

    print("\n------------------------- Second step -----------------------")
    
    # message given by teacher
    # message = A478E62F 9A8AE3F8 3DFBCD61 9DFA3324 83FF8E83 0CC95806
    #           0947D518 BB69EA37 63D6FFEC F82AA178 4DD4EB34 941198E8
    #           DCEED40F 76CD9487 8F4B2C58 AEDA0C8E D0F0E0DF A34F3F71
    #           B32FF0C5 E2549A9F B21BEB21 72FCD97F 42675582 4370D2E3
    #           F05918CC C370851B F7206907 519205ED 3C4DF11A B24BD8E2
    #           EB498CEE 57E2C211 5A825F76 87A95238 05B644E1 D63EF06B
    message = "A478E62F9A8AE3F83DFBCD619DFA332483FF8E830CC958060947D518BB69EA3763D6FFECF82AA1784DD4EB34941198E8DCEED40F76CD94878F4B2C58AEDA0C8ED0F0E0DFA34F3F71B32FF0C5E2549A9FB21BEB2172FCD97F426755824370D2E3F05918CCC370851BF7206907519205ED3C4DF11AB24BD8E2EB498CEE57E2C2115A825F7687A9523805B644E1D63EF06B"
    #message = '5D7304AF32367F61317FF6392DA00AD45146E490E4E57694218E63FC25E01869B8845B390D17C28774971C9FE0390CB29310C45FBAF59B05246239CCDF2DC39F971C508E4BA470DBC3A9D3AA105EB147656DA5CD860AC61BE87FE88FC22338A278D4C2D7FA540032C092745D5382167578EEC9F1BEE2AABAAA961B5621FE2317'
    print("\nEncrypted message:\n", message)

    # plain_text = Acho que agora foi :-). Um bit de diferença já invalida tudo. Manda esta msg de volta invertida e cifrada. Valeu
    plain_text = AES_decrypt(message, password)
    print("\nPlain text:\n", plain_text)

    # reversed_plain_text = uelaV .adarfic e aditrevni atlov ed gsm atse adnaM .odut adilavni \xc3\xa1j a\xc3\xa7nerefid ed tib mU .)-: iof aroga euq ohcA
    reversed_plain_text = plain_text[::-1].encode()
    print("\nReversed encoded plain text:\n", reversed_plain_text)
    # message given to teacher
    # message = 747E1A77 844DCEAD D89F8BFC 78C2B3AA EB821CB4 629FF321
    #           9359B75A 4805C4B9 6DC9F83C DDAE0FAC 44460992 F6EB8228
    #           26B7A538 AA0FBB0D 7939DB9F 3D2D9240 827CBE0A 8241C76C
    #           B3C3FC73 FE0C9099 F7DDE05A 2A99447F E8833853 8043FD45
    #           94FFDCC9 85A0FF7F 9C66DB52 BBEF234B D0859C15 1E071100
    #           5E28F0F4 69939845 CCAA1F6E 54C82AE8 5CE5EC95 3ABA0DE6

    reversed_crypted_message = AES_encrypt(reversed_plain_text, password).hex().upper()
    print("\n Plain text encrypted:\n", reversed_crypted_message)
    
    
    
    