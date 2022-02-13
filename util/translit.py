def bgn_pcgn(cyr_str: str) -> str:
    prev_letter = ' '
    default_uppercase: dict[str, str] = {
        'А': 'A',
        'Б': 'B',
        'В': 'V',
        'Г': 'G',
        'Д': 'D',
        'Е': 'Ye',
        'Ё': 'Yё',
        'Ж': 'Zh',
        'З': 'Z',
        'И': 'I',
        'Й': 'Y',
        'К': 'K',
        'Л': 'L',
        'М': 'M',
        'Н': 'N',
        'О': 'O',
        'П': 'P',
        'Р': 'R',
        'С': 'S',
        'Т': 'T',
        'У': 'U',
        'Ф': 'F',
        'Х': 'Kh',
        'Ц': 'Ts',
        'Ч': 'Ch',
        'Ш': 'Sh',
        'Щ': 'Shch',
        'Ъ': '”',
        'Ы': 'Y',
        'Ь': '’',
        'Э': 'E',
        'Ю': 'Yu',
        'Я': 'Ya'
    }
    default_lowercase: dict[str, str] = {
        c.lower(): default_uppercase[c].lower() for c in default_uppercase
    }
    default_lowercase['е'] = 'e'
    default_lowercase['ё'] = 'ё'
    default: dict[str, str] = { **default_uppercase, **default_lowercase }
    ioted_e_prevs = 'аоуэыяёюеиАОУЭЫЯЁЮЕИйЙъь -'
    res: list[str] = []
    for c in cyr_str:
        if c == 'е' and prev_letter in ioted_e_prevs:
            res.append('ye')
        elif c == 'ё' and prev_letter in ioted_e_prevs:
            res.append('yё')
        elif c in default:
            res.append(default[c])
        else:
            res.append(c)
        prev_letter = c
    return ''.join(res)