from collections import OrderedDict
from pathlib import Path

from faker import Faker
from tqdm import tqdm

from fingerspelling import spell, get_chars
from faker.providers import person


def strip_all(word: str, space=True):
    return word.replace(" ", "" if space else " ") \
        .replace(".", "") \
        .replace(",", "") \
        .replace("-", "" if space else " ") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("\\n", " ")


def fake_text_data(language: str, country: str):
    if language == "es" and country in ["hn", "ni"]:
        country = "es"

    fake = Faker(f'{language.lower()}_{country.upper()}')
    fake.add_provider(person.Provider)
    Faker.seed(0)

    # Add some names
    new_first_names = ["Amit", "Zifan"]
    for p in fake.get_providers():
        if isinstance(p, person.Provider) and isinstance(p.first_names, OrderedDict):
            first_num = next(iter(p.first_names.values()))
            for new_first_name in new_first_names:
                p.first_names[new_first_name] = first_num

    stripper = lambda s: strip_all(s, space=False)
    FAKE_CATEGORIES = {
        # Adresses
        "address": stripper,
        "city": stripper,
        "country": stripper,
        "postcode": stripper,
        "street_name": stripper,
        # Automotive
        "license_plate": lambda s: strip_all(s),
        # Banking
        "swift": stripper,
        # Barcode
        "ean": stripper,
        # Currency
        "currency_code": stripper,
        "cryptocurrency_code": stripper,
        "currency_symbol": stripper,
        # File extension
        "file_extension": stripper,
        "file_name": lambda s: s.replace(".", " . "),
        # Domains
        "free_email": lambda s: s.replace('@', ' @ ').replace(".", " . "),
        # Person
        "first_name": stripper,
        "last_name": stripper,
        "name": stripper,
        "phone_number": lambda s: strip_all(s),
        # Number
        "random_int": lambda s: s,
    }

    for category, stripper in FAKE_CATEGORIES.items():
        for i in range(300):
            value = str(fake.__getattr__(category)()).replace("\n", " \\n ")
            yield value, stripper(value)


def spoken_text_fingerspelling(text: str, chars: dict):
    words = text.split()

    signs = [spell(word, chars=chars) for word in words]
    if any(sign is None for sign in signs):
        return None
    return " ".join(signs)


def my_name_is(language: str, country: str, iana: str, chars: dict):
    my_name = {
        "ase": [
            "My name is {name}",
            "M514x514S15a01491x487S20500487x503 M522x525S11541498x491S11549479x498S20600489x476 {name}"
        ]
    }
    if iana in my_name:
        spoken_sentence, signed_sentence = my_name[iana]

        fake = Faker(f'{language.lower()}_{country.upper()}')
        Faker.seed(42)
        for i in range(1000):
            for faker_type in ['name', 'first_name', 'last_name']:
                spoken_name = fake.__getattr__(faker_type)()
                signed_name = spoken_text_fingerspelling(strip_all(spoken_name, space=False), chars)
                yield spoken_sentence.format(name=spoken_name), signed_sentence.format(name=signed_name)


def fake_data_signed(language: str, country: str, iana: str, chars: dict):
    for char, writings in chars.items():
        for writing in writings:
            yield char, writing

    # Adding defaults if do not exist
    if "@" not in chars:
        chars["@"] = ["M510x524S1f720488x487S2f104492x507S21600496x475",
                      "M512x528S1f720488x481S2e308488x501S2f900495x473",
                      "M512x523S1f720488x478S2e300487x496"]
    if "." not in chars:
        chars["."] = ["M513x518S10a20482x483S2f900494x513"]

    for spoken, spoken_stripped in fake_text_data(language, country):
        writing = spoken_text_fingerspelling(spoken_stripped, chars)
        if writing is not None:
            yield spoken, writing

    # Experimental: adding "my name is..." sentences
    for spoken, signed in my_name_is(language, country, iana, chars):
        yield spoken, signed


if __name__ == "__main__":
    current_dir = Path(__file__).parent
    data_dir = current_dir.parent.parent / "data"
    fingerspelling_dir = data_dir / "fingerspelling"
    fingerspelling_csv = data_dir / "fingerspelling.csv"

    # CSV Writer
    import csv

    with open(fingerspelling_csv, "w", encoding="utf-8") as f:
        # write header
        writer = csv.writer(f)
        writer.writerow(["spoken_language", "country_code", "sign_language", "sign_writing", "texts"])

        for f_path in tqdm(fingerspelling_dir.iterdir()):
            if f_path.name == "README.md":
                continue

            name = f_path.name.split(".")[0]
            spoken_language, country, iana, local_name = name.split("-")
            chars = get_chars(name)

            print(spoken_language, list(chars.keys()))
            hashes = set()
            for spoken, signed in fake_data_signed(spoken_language, country, iana, chars):
                row = [spoken_language, country, iana, signed, spoken]
                row_hash = hash(tuple(row))
                if row_hash not in hashes:
                    hashes.add(row_hash)
                    writer.writerow([spoken_language, country, iana, signed, spoken])
