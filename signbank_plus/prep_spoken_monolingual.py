import gzip
import random
from pathlib import Path

from tqdm import tqdm
from wordfreq import top_n_list, available_languages

SPOKEN_SIGNED = {
    "ak": ["ads", "gse"],
    "sq": ["sqk"],
    "ps": ["afg"],
    "ar": ["asp", "syy", "esl", "jos", "jos", "sqx", "lbs", "xms", "sdl", "tse"],
    "ja": ["jks", "jsl", "ehs"],
    "en": ["ase", "asf", "asw", "bfi", "hps", "jcs", "jls", "xki", "lws", "nsr", "lsy", "mre", "rsm", "nbs", "nzs",
           "nsi", "okl", "pgz", "psp", "psd", "rsi", "sgx", "lsv", "sls", "szs", "tsy", "lst", "ugn", "yhs", "ygs",
           "zsl", "zib"],
    "es": ["aed", "bvl", "csg", "csn", "csr", "csf", "doq", "ecs", "gsm", "hds", "mfs", "ncs", "lsp", "pys", "prl",
           "prz", "psl", "esn", "ssp", "ugy", "vsl", "msd"],
    "hy": ["aen"],
    "de": ["asq", "gsg", "sgg"],
    "fr": ["bog", "lsb", "cds", "fsl", "gus", "lsg", "mzc", "mzg", "fcs", "sfb", "ssr"],
    "th": ["bfk", "csd", "tsq"],
    "id": ["bqy", "inl"],
    "pt": ["bzs", "mzy", "psr", "uks"],
    "bg": ["bqn"], "km": ["csx"],
    "ca": ["csc", "vsv"],
    "zh": ["csl", "hks", "tss"],
    "hr": ["csq"], "cs": ["cse"],
    "da": ["dsl"], "nl": ["dse", "vgt"],
    "et": ["eso"], "am": ["eth"],
    "fi": ["fss", "fse"],
    "ne": ["gds", "jhs", "jus", "nsp"],
    "el": ["gss", "gss-cy"],
    "vi": ["haf", "hab", "hos"],
    "ha": ["hsl"],
    "hu": ["hsh"],
    "is": ["icl"],
    "hi": ["ins"],
    "iu": ["iks"],
    "ga": ["isg"],
    "he": ["isr"],
    "it": ["ise", "slf"],
    "ko": ["kvk"],
    "lo": ["lso"],
    "lv": ["lsl"],
    "lt": ["lls"],
    "ms": ["xml", "psg", "kgi"],
    "mt": ["mdl"],
    "ro": ["vsi", "rms"],
    "mn": ["msr"],
    "my": ["ysm"],
    "no": ["nsl"],
    "ur": ["pks"],
    "fa": ["psc"],
    "pl": ["pso"],
    "ru": ["rsl"],
    "sk": ["svk"],
    "af": ["sfs"],
    "si": ["sqs"],
    "sv": ["swl"],
    "sw": ["tza"],
    "bo": ["lsn"],
    "tr": ["tsm"],
    "uk": ["ukl"],
    "bn": ["wbs"],
    "yi": ["yds"],
    "sr": ["ysl", "ysl"],
    "be": ["rsl-by"]
}


def save_mono_words(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    f_gzip = gzip.open(path.joinpath(f'mono.spoken.gz'), 'wt')

    languages = list(available_languages().keys())
    for language in tqdm(languages):
        if len(language) != 2:
            continue
        signed_languages = ["ils"] # International sign
        if language in SPOKEN_SIGNED:
            signed_languages += SPOKEN_SIGNED[language]

        for signed_language in signed_languages:
            flags = f"${language} ${signed_language}"

            words = top_n_list(language, 20000)
            for word in words:
                tokenized = " ".join(list(word.replace(" ", "_")))
                f_gzip.write(flags + " " + tokenized + "\n")

    f_gzip.close()


if __name__ == "__main__":
    mono_path = Path(__file__).parent.parent / "data" / "mono"
    save_mono_words(mono_path / "words")
