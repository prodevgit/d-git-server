def validate_ssh(key):
    import base64, struct, sys, binascii
    array = bytes(key,'utf-8').split();
    # Each rsa-ssh key has 3 different strings in it, first one being
    # typeofkey second one being keystring third one being username .
    if len(array) != 3:
        return False
    typeofkey = array[0];
    string = array[1];
    username = array[2];
    # must have only valid rsa-ssh key characters ie binascii characters
    try:
        data = base64.decodestring(string)
    except binascii.Error:
        return False
    a = 4
    # unpack the contents of data, from data[:4] , it must be equal to 7 , property of ssh key .
    try:
        str_len = struct.unpack('>I', data[:a])[0]
    except struct.error:
        return False
    # data[4:11] must have string which matches with the typeofkey , another ssh key property.
    if data[a:a + str_len] == typeofkey and int(str_len) == int(7):
        return True
    else:
        return False