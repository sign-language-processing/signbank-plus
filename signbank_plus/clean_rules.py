import re


def clean_instance(instance):
    for i, text in enumerate(instance['texts']):
        # Remove texts that match to urls
        url_regex = re.compile(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
        if url_regex.search(text):
            instance['texts'][i] = ""

        # TODO: if text is less than 5 words, but more than 15 signs, remove it

    if instance['puddle_id'] == 52:
        for i, text in enumerate(instance['texts']):
            text = re.sub(r'\((UPOL|biol|IMoTeSP|UPOL2)\)$', '', text, flags=re.IGNORECASE)
            text = text.strip()
            text = re.sub(r' [0-9A-Zv2]$', '', text)
            instance['texts'][i] = text

    if instance['puddle_id'] == 49:
        sgbfss_regex = re.compile(
            r'(lexique SGBFSS|lexique SGB-FSS|^liste:|jeu SignEcriture|JEU-COULEURS|CCSS|ApéroSignes)',
            flags=re.IGNORECASE)
        for i, text in enumerate(instance['texts']):
            if sgbfss_regex.search(text):
                instance['texts'][i] = ""

    if instance['puddle_id'] == 16:
        for i, text in enumerate(instance['texts']):
            if 'SWS-TAG' in text:
                instance['texts'][i] = ""

    if instance['puddle_id'] == 53:
        for i, text in enumerate(instance['texts']):
            if text.startswith('vgl') or 'vgl:' in text or text == 'KK' or 'delegs' in text or 'vgl KK' in text:
                instance['texts'][i] = ""

            if re.match(r'^Variante \d$', text.strip()):
                instance['texts'][i] = ""

            if re.match(r'^Geschichte \".*?\"$', text.strip()):
                instance['texts'][i] = ""

            if re.match(r'^[Ss][\d\. ]*$', text.strip()):  # S.221 4.1313
                instance['texts'][i] = ""

            if re.match(r'^rwth\d*$', text.strip()):  # S.221 4.1313
                instance['texts'][i] = ""

    if instance['puddle_id'] == 4:
        for i, text in enumerate(instance['texts']):
            if text == 'English sign':
                instance['texts'][i] = ""

    if instance['puddle_id'] == 41:
        for i, text in enumerate(instance['texts']):
            if text.startswith('.LSC'):
                instance['texts'][i] = ""

    if instance['puddle_id'] == 47:
        for i, text in enumerate(instance['texts']):
            if text.startswith('Liste: ') or text.startswith('Alice'):
                instance['texts'][i] = ""

        last_text = instance['texts'][-1].strip().lower()
        # replace with regex
        if 'nom.' in last_text or re.match(
                r'^(nom|verbe|adjectif|adverbe|pronom|préposition|conjonction|interjection|déterminant|phrase|géographie)',
                last_text):
            instance['texts'][-1] = ""

    if instance['puddle_id'] == 49:
        for i, text in enumerate(instance['texts']):
            if text.startswith('FMS') or text.startswith('EMM') or 'n°' in text:
                instance['texts'][i] = ""

    # Remove empty texts from the array
    instance['texts'] = [text for text in instance['texts'] if text.strip() != ""]
