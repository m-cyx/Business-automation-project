s = 'aaabbcdddd'

def convert(s):
    converted_str = ''
    for el in s:
        converted_str += el + str(s.count(el))

    return converted_str

print(convert(s))

return ''.join(i + str(text.count(i)) for i in sorted(set(text)))
