import pymorphy3
import string
from dataclasses import dataclass

@dataclass
class ParsedWord:
    normal_form: str
    POS: str
    number: int
    gender: str | None
    case: str


def get_word_pairs(filepath):
    morph = pymorphy3.MorphAnalyzer()
    
    # Чтение текста из файла
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Разделение текста на слова
    words = text.split()
    
    # Результирующий список пар
    pairs = []

    for i in range(len(words) - 1):
        parsed1 = parse_word(morph, words[i])
        parsed2 = parse_word(morph, words[i + 1])
        
        # Проверка, что одно из слов - существительное или прилагательное
        if ('NOUN' in {parsed1.POS, parsed2.POS} or
            'ADJF' in {parsed1.POS, parsed2.POS}):
            
            # Проверка совпадения рода, числа и падежа
            if (parsed1.gender == parsed2.gender and
                parsed1.number == parsed2.number and
                parsed1.case == parsed2.case):
                
                # Добавление пары лемм в результат
                pairs.append((parsed1.normal_form, parsed2.normal_form))
    
    return pairs

def parse_word(morph: pymorphy3.MorphAnalyzer, word: str) -> ParsedWord:
    word = morph.parse(remove_punctuation(word))[0]
    word = ParsedWord(
        word.normal_form, 
        word.tag.POS,
        word.tag.number, 
        word.tag.gender,
        word.tag.case
    )

    if word.gender is None:
        word.gender = morph.parse(word.normal_form)[0].tag.gender
    
    return word

def remove_punctuation(word):
    translator = str.maketrans('', '', string.punctuation)
    return word.translate(translator)

# Использование функции
filepath = 'file.txt'
pairs = get_word_pairs(filepath)
for pair in pairs:
    print(pair)
