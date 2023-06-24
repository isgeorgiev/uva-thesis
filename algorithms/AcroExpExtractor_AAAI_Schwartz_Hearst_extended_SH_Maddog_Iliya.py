import logging
from AcroExpExtractors.AcroExpExtractor import (
    AcroExpExtractorRb,
)
from nltk import word_tokenize
import re
from nltk.corpus import stopwords
from nltk import sent_tokenize
import spacy
sp = spacy.load('en_core_web_sm')
import re
import string 
from AcroExpExtractors.AcroExpExtractor_MadDog import AcroExpExtractor_MadDog
tokenizer = word_tokenize

logger = logging.getLogger(__name__)
stop_words = set(stopwords.words('english'))
logger = logging.getLogger(__name__)
stop_words.update(['and', 'the', 'METHODS', 'RESULTS', 'CONCLUSIONS', 'OBJECTIVE', 'BACKGROUND', 'COMMIT', 'SUBJECTS','DESIGN', 'PURPOSE', 'MEASURES', 'SETTING', 'I','II','III','IV','V','VI','VII','VIII','IX','X','XX','CONCLUSION','MATERIALS','AND', 'et', 'du'])
# Add bulgarian stop words
bulgarian_stop_words = ["а","автентичен","аз","ако","ала","бе","без","беше","би","бивш","бивша","бившо","бил","била","били","било","благодаря","близо","бъдат","бъде","бяха","в","вас","ваш","ваша","вероятно","вече","взема","ви","вие","винаги","внимава","време","все","всеки","всички","всичко","всяка","във","въпреки","върху","г","ги","главен","главна","главно","глас","го","година","години","годишен","д","да","дали","два","двама","двамата","две","двете","ден","днес","дни","до","добра","добре","добро","добър","докато","докога","дори","досега","доста","друг","друга","други","е","евтин","едва","един","една","еднаква","еднакви","еднакъв","едно","екип","ето","живот","за","забавям","зад","заедно","заради","засега","заспал","затова","защо","защото","и","из","или","им","има","имат","иска","й","каза","как","каква","какво","както","какъв","като","кога","когато","което","които","кой","който","колко","която","къде","където","към","лесен","лесно","ли","лош","м","май","малко","ме","между","мек","мен","месец","ми","много","мнозина","мога","могат","може","мокър","моля","момента","му","н","на","над","назад","най","направи","напред","например","нас","не","него","нещо","нея","ни","ние","никой","нито","нищо","но","нов","нова","нови","новина","някои","някой","няколко","няма","обаче","около","освен","особено","от","отгоре","отново","още","пак","по","повече","повечето","под","поне","поради","после","почти","прави","пред","преди","през","при","пък","първата","първи","първо","пъти","равен","равна","с","са","сам","само","се","сега","си","син","скоро","след","следващ","сме","смях","според","сред","срещу","сте","съм","със","също","т","тази","така","такива","такъв","там","твой","те","тези","ти","т.н","то","това","тогава","този","той","толкова","точно","три","трябва","тук","тъй","тя","тях","у","утре","харесва","хиляди","ч","часа","че","често","чрез","ще","щом","юмрук","я","як"]
stop_words.update(bulgarian_stop_words)

class AcroExpExtractor_AAAI_Schwartz_Hearst_extended_SH_Maddog_Iliya(AcroExpExtractorRb):
    """Implementation of the Schwartz and Hearts rule based algorithm."""

    def __init__(self):
        pass

    def _has_capital(self, string):
        """Checks if a string has a capital.

        Args:
            string (str): a string

        Returns:
            bool: True if string as capital, False otherwise.
        """
        for i in string:
            if i.isupper():
                return True
        return False

    def _is_valid_short_form(self, acr):
        """Checks if an acronym has a letter and the first character is alphanumeric.

        Args:
            acr (str): the acronym

        Returns:
            bool: True if acronym is valid, False otherwise.
        """
        if self._has_letter(acr) and (
            acr[0].isalpha() or acr[0].isdecimal() or acr[0] == "("
        ):
            return True
        else:
            return False

    def _has_letter(self, string):
        """Checks if a string as a letter.

        Args:
            string (str): a string.

        Returns:
            bool: True if the string as a letter, False otherwise.
        """
        for c in string:
            if c.isalpha():
                return True
        return False

    def _find_best_long_form(self, short_form, long_form):
        """Returns the best long form for a short form from a series of candidate long forms.

        Args:
            short_form (str): the acronym
            long_form (str): the candidate expansion
        Returns:
            str: the best long form for the short form. If one is not found None is returned.
        """
        l_index = len(long_form) - 1

        print (short_form, long_form)
        for s_index in range(len(short_form) - 1, -1, -1):
            curr_char = short_form[s_index].lower()
            if not (curr_char.isalpha() or curr_char.isdecimal()):
                continue
            while (l_index >= 0 and long_form[l_index].lower() != curr_char) or (
                s_index == 0
                and l_index > 0
                and (
                    long_form[l_index - 1].isalpha()
                    or long_form[l_index - 1].isdecimal()
                )
            ):
                l_index -= 1
            if l_index < 0:
                return None
            l_index -= 1
        l_index = long_form.rfind(" ", 0, l_index + 1) + 1
        return long_form[l_index:]

    def _extract_abbr_pair(self, short_form, long_form, candidates):
        """Extracts the best long form for a short form from several candidate long forms.

        Args:
            short_form (str): the acronym
            long_form (str): the candidate expansion
            candidates (dict): a dictionary whose keys are acronyms and values are expansions.

        Returns:
            dict: a dicionary whose keys are acronyms and values are expansions.
        """
        best_long_form = ""
        long_form_size, short_form_size = 0, 0
        if len(short_form) == 1:
            return candidates
        best_long_form = self._find_best_long_form(short_form, long_form)
        if best_long_form == None:
            return candidates
        best_long_tokens = re.split("[ \t\n\r\f-]", best_long_form)
        best_long_tokens = [x for x in best_long_tokens if x != ""]
        long_form_size = len(best_long_tokens)
        short_form_size = len(short_form)
        for i in range(short_form_size - 1, -1, -1):
            if not (short_form[i].isalpha() or short_form[i].isdecimal()):
                short_form_size -= 1
        if (
            len(best_long_form) < len(short_form)
            or best_long_form.find(short_form + " ") > -1
            or best_long_form.endswith(short_form)
            or long_form_size > short_form_size * 2
            or long_form_size > short_form_size + 5
            or short_form_size > 10
        ):
            return candidates

        candidates[short_form] = best_long_form
        return candidates

    def _extract_abbr_pairs_from_str(self, text):
        """Extracts acronyms and the corresponding expansions that are present in text.

        Args:
            text (str): the text to analyse

        Returns:
            dict: a dicionary whose keys are acronyms and values are expansions.
        """
        tmp_str, long_form, short_form, curr_sentence = "", "", "", ""
        (
            open_paren_index,
            close_paren_index,
            sentence_end,
            new_close_paren_index,
            tmp_index,
        ) = (
            -1,
            -1,
            -1,
            -1,
            -1,
        )
        new_paragraph = True
        candidates = {}
        try:
            text_split = text.split("\n")
            for phrase in text_split:
                if len(phrase) == 0 or new_paragraph and not phrase[0].isupper():
                    curr_sentence = ""
                    new_paragraph = True
                    continue
                new_paragraph = False
                phrase += " "
                curr_sentence += phrase
                open_paren_index = curr_sentence.find(" (")
                paren_cond = True
                while paren_cond:
                    if open_paren_index > -1:
                        open_paren_index += 1
                    sentence_end = max(
                        curr_sentence.rfind(". "), curr_sentence.rfind(", ")
                    )
                    if open_paren_index == -1 and not sentence_end == -1:
                        curr_sentence = curr_sentence[sentence_end + 2 :]
                    elif curr_sentence.find(")", open_paren_index) > -1:
                        close_paren_index = curr_sentence.find(")", open_paren_index)
                        sentence_end = max(
                            curr_sentence.rfind(". ", 0, open_paren_index + 1),
                            curr_sentence.rfind(", ", 0, open_paren_index + 1),
                        )
                        if sentence_end == -1:
                            sentence_end = -2
                        long_form = curr_sentence[sentence_end + 2 : open_paren_index]
                        short_form = curr_sentence[
                            open_paren_index + 1 : close_paren_index
                        ]
                    if len(short_form) > 0 or len(long_form) > 0:
                        if len(short_form) > 1 and len(long_form) > 1:
                            if (
                                short_form.find("(") > -1
                                and curr_sentence.find(")", close_paren_index + 1) > -1
                            ):
                                new_close_paren_index = curr_sentence.find(
                                    ")", close_paren_index + 1
                                )
                                short_form = curr_sentence[
                                    open_paren_index + 1 : new_close_paren_index
                                ]
                                close_paren_index = new_close_paren_index

                            if short_form.find(", ") > -1:
                                tmp_index = short_form.find(", ")
                                short_form = short_form[0:tmp_index]
                            if short_form.find("; ") > -1:
                                tmp_index = short_form.find("; ")
                                short_form = short_form[0:tmp_index]
                            short_tokens = re.split("[ \t\n\r\f]", short_form)
                            short_tokens = [x for x in short_tokens if x != ""]
                            if len(short_tokens) > 2 or len(short_form) > len(
                                long_form
                            ):
                                tmp_index = curr_sentence.rfind(
                                    " ", 0, open_paren_index - 2 + 1
                                )
                                tmp_str = curr_sentence[
                                    tmp_index + 1 : open_paren_index - 1
                                ]
                                long_form = short_form
                                short_form = tmp_str
                                if not self._has_capital(short_form):
                                    short_form = ""
                            if self._is_valid_short_form(short_form):
                                candidates = self._extract_abbr_pair(
                                    short_form.strip(), long_form.strip(), candidates
                                )

                        curr_sentence = curr_sentence[close_paren_index + 1 :]
                    elif open_paren_index > -1:
                        if (len(curr_sentence) - open_paren_index) > 200:
                            # Matching close paren was not found
                            curr_sentence = curr_sentence[open_paren_index + 1 :]
                        break
                    short_form = ""
                    long_form = ""
                    open_paren_index = curr_sentence.find(" (")
                    paren_cond = open_paren_index > -1
        except Exception:
            logger.exception(
                "Fatal error running Schwartz and Hearst AcroExpExtractor for text: "
                + text
            )

        return candidates

    def _split_tokens(self, tokens):
        """Split element according to specific chars.

        Args:
            tokens (list): list of tokens
        """
        for token in tokens:
            for element in re.split(
                "[\u002D\u058A\u05BE\u1400\u1806\u2010-\u2015\u2E17\u2E1A\u2E3A\u2E3B\u2E40\u301C\u3030\u30A0\uFE31\uFE32\uFE58\uFE63\uFF0D/]",
                token,
            ):
                yield element

    def get_all_acronyms(self, text):
        """Extract all the possible acronyms inside a given text.

        Args:
            text (str): the text
        Returns:
            acronyms (list): the extracted acronyms
        """
        tokens = set(self._split_tokens(tokenizer(text)))
        acronyms = []
        for token in tokens:
            if len(token) < 2 or token[1:].islower():
                continue
            if len(token) < 3 and token[1] == ".":
                continue
            if self._is_valid_short_form(token):
                acronyms.append(token)
        return acronyms

    def get_all_acronyms_extended(self, text):
        """Extract all the possible acronyms inside a given text.

        Args:
            text (str): the text
        Returns:
            acronyms (list): the extracted acronyms
        """
        tokens = set(tokenizer(text))
        acronyms = []
        for token in tokens:
            if len(token) < 2 or token[1:].islower():
                continue
            if len(token) < 3 and token[1] in string.punctuation:
                continue
            # added by Iliya
            if len(token) > 0 and not (token[0].isupper() or token[0].isdigit()):
                continue
            # if 70% of the letter are capital 
            if (len([s for s in token if s.isupper() or s.isdigit()]) < len(token)*0.7):
                continue
            if token in stop_words:
                continue
            if len(token) < 2 and len(token) > 10:
                continue
            if self._is_valid_short_form(token):
                acronyms.append(token)
        return acronyms

    def get_all_acronym_expansion(self, text):
        """Returns a dicionary where each key is an acronym (str) and each value is an expansion (str). The expansion is None if no expansion is found.

        Args:
            text (str): the text to extract acronym-expansion pairs from

        Returns:
            dict:
             a dict that has acronyms as values and definitions as keys. Definition is None if no definition is found for the acronym in text.
             The returned dict is enconded in UTF-8 (the python3 standard)
        """
        acronyms = self.get_all_acronyms(text)
        abbrev_map = {acronym: None for acronym in acronyms}
        for acronym, expansion in self.get_acronyms_expansions_from_text(text).items():
            abbrev_map[acronym] = expansion
        return abbrev_map

    def get_acronym_expansion_pairs(self, text):
        """Returns a dicionary where each key is an acronym (str) and each value is an expansion (str).

        Args:
            text (str): the text to extract acronym-expansion pairs from

        Returns:
            dict:
             a dict that has acronyms as values and definitions as keys. The returned dict is enconded in UTF-8 (the python3 standard)
        """
        return self.get_acronyms_expansions_from_text(text)

    def find_acronyms_indexes_text(self, abbrev_map, tokenized_text, acronym_list):
        """Returns a dicionary where each key is an acronym (str) and each value is a list of indexes of the acronym in the text.

        Args:
            abbrev_map (dict): a dict that has acronyms as values and definitions as keys.
            tokenized_text (list): a list of tokens
            acronym_list (list): a list of acronyms

        Returns:
            dict:
             a dict that has acronyms as values and indexes as keys. The returned dict is enconded in UTF-8 (the python3 standard)
        """
        acronym_map = {}

        # Build acronym map, check the index of the acronym
        for acronym in abbrev_map.keys():
            if acronym in tokenized_text and (acronym_list.get(acronym) is None):
                # Get index of the acronym in the tokenized text
                acronym_map[tokenized_text.index(acronym)] = acronym
                # Add the acronym to the global list of acronyms

        # Check if acronym is in two tokens
        for acronym_index, acronym in acronym_map.items():
            if acronym_map.get(acronym_index + 1) in abbrev_map.keys():
                if acronym_map.get(acronym_index + 1) is not None and abbrev_map.get(acronym_index) is not None:
                    acronym_map[acronym_index] = acronym_map[acronym_index] + " " + acronym_map[acronym_index + 1]
                    # delete index 
                    del acronym_map[acronym_index + 1]
        return acronym_map


    def _find_best_long_form_extended(self, short_form, long_form):
        """Returns the best long form for a short form from a series of candidate long forms.

        Args:
            short_form (str): the acronym
            long_form (str): the candidate expansion
        Returns:
            str: the best long form for the short form. If one is not found None is returned.
        """
        if(len(long_form)<1):
            return None
        long_form = long_form.replace(short_form, "")
        long_form = long_form.replace("-", " ").strip()

        long_form_words = long_form.split(' ')
        l_index = len(long_form_words) - 1
        short_form_capitals = ''.join([c.lower() for c in short_form if c.isupper() or c.isdigit()])
        r_index = -1

        for s_index in range(len(short_form_capitals) - 1, -1, -1):
            curr_char = short_form_capitals[s_index].lower()
            if not (curr_char.isalpha() or curr_char.isdecimal()):
                continue

            while (len(long_form_words[l_index])>0 and l_index >= 0 and (long_form_words[l_index][0].lower() != curr_char or long_form_words[l_index] in stop_words)) or (
                s_index == 0
                and l_index > 0
            ):
                l_index -= 1
            if l_index < 0:
                break
            if(r_index < 0):
                r_index = l_index
        if(l_index >= 0):
            long_form = " ".join(long_form_words[l_index:r_index+1]).strip()
            return self._extra_rules(short_form,  long_form)
        
        else:
            l_index = len(long_form) - 1

            for s_index in range(len(short_form) - 1, -1, -1):
                curr_char = short_form[s_index].lower()
                if not (curr_char.isalpha() or curr_char.isdecimal()):
                    continue
                while (l_index >= 0 and long_form[l_index].lower() != curr_char) or (
                    s_index == 0
                    and l_index > 0
                    and (
                        long_form[l_index - 1].isalpha()
                        or long_form[l_index - 1].isdecimal()
                    )
                ):
                    l_index -= 1
                if l_index < 0:
                    return None
                l_index -= 1

            l_index = long_form.rfind(" ", 0, l_index + 1) + 1
            return self._extra_rules(short_form,  long_form[l_index:])
    

    def _extra_rules(self, short_form, long_form):
        expansion = long_form
        expansion_array = expansion.split(' ')
        stopwords_expansion = 0

        if(expansion_array[len(expansion_array)-1] in stop_words):
            expansion_array.pop()

        if(len(expansion_array)>0 and expansion_array[0] in stop_words):
            expansion_array.pop(0)

        short_form_capital_letters = [c.lower() for c in short_form if c.isupper() or c.isdigit()] 
        
        matched_last = False
        matched_first = False

        for word in expansion_array:
            if re.match(r"^[A-Z0-9]+$", word) or word in string.punctuation:
                index = expansion_array.index(word)
                expansion_array.pop(index)
                continue
                
        # letter matching
        for word in reversed(expansion_array):  
            if len(word) > 0 and word[0].lower() == short_form_capital_letters[-1].lower() and word not in stop_words:
                expansion_array = expansion_array[:expansion_array.index(word)+1]
                matched_last = True
                break
        if(matched_last != True):
            return None

        for word in expansion_array:  
            if len(word) > 0 and word[0].lower() == short_form_capital_letters[0].lower() and word not in stop_words:
                expansion_array = expansion_array[expansion_array.index(word):]
                matched_first = True
                break
            

        if(matched_first != True):
            return None
        expansion = ' '.join(expansion_array)

        if(expansion.find(short_form) != -1):
            return None
           
        
        for s in expansion.replace('-', ' ').split(' '):
            if(s in stop_words):
                stopwords_expansion += 1
        
        first_letters_expansion = [ s[0].lower() for s in expansion.replace('-', ' ').split(' ') if len(s)>0]
        for s in expansion:
            if((s.isupper() or s.isdigit()) and s.lower() not in first_letters_expansion):
                first_letters_expansion.append(s.lower())
                
        first_letters_expansion_copy = first_letters_expansion

        for letter in short_form_capital_letters:
            if(len(first_letters_expansion)<1):
                return None
            if letter not in first_letters_expansion:
                return None
            else:
                index = first_letters_expansion.index(letter)
                first_letters_expansion.pop(index)

        
        if(len(short_form_capital_letters) < len(''.join([c for c in expansion if c.isupper() or c.isdigit()]))):
            return None;
        
        capital_letters_expansion_words = re.findall(r"[A-Z0-9]{2}", expansion)


        if(capital_letters_expansion_words is not None and len(capital_letters_expansion_words) > len(short_form_capital_letters)):
            return None
        
        if(len(short_form_capital_letters) + stopwords_expansion < len(first_letters_expansion_copy)):
            return None;

        return expansion

    def get_acronyms_expansions_from_text(self, text):
        """Returns the acronyms expansions from the text.

        Args:
            text (str): the text to extract acronym-expansion pairs from

        Returns:
            dict:
             a dict that has acronyms as values and definitions as keys. Definition is None if no definition is found for the acronym in text.
             The returned dict is enconded in UTF-8 (the python3 standard)
        """
        

        acronyms = self.get_all_acronyms_extended(text)
        # define a dict to store the acronym and its expansion
        abbrev_map = {acronym: None for acronym in acronyms}
        text_split = text.split("\n")
        acronym_list = dict()
        for paragraphs in text_split:
            for sentence in sent_tokenize(paragraphs):
                tokenized_text = tokenizer(sentence)
                if( len(list(set(abbrev_map.keys())))> 0 and len(list(tokenized_text))>0) :
                
                    LENGHT_OF_TOKENIZED_TEXT = len(tokenized_text)
                    # Acronym map per sentence
                    acronym_map = self.find_acronyms_indexes_text(abbrev_map, tokenized_text, acronym_list)

                    # Go through the found acronyms and get the definitions
                    for acronym_index, acronym in acronym_map.items():
                        
                        # get the sum of all of the uppercase letters and digits, ignore the lowercase
                        acronym_capital_letters = [c.lower() for c in acronym.strip() if c.isupper() or c.isdigit()]
                        LENGTH_OF_ACRONYM = len(acronym_capital_letters)

                        acronym_small_letters_words = re.findall(r'[a-z]+', acronym)
                        
                        if(len(acronym_small_letters_words)>0):
                            LENGTH_OF_ACRONYM += len(acronym_small_letters_words)

                        acronym_last_capital_letter = acronym_capital_letters[-1]
                        acronym_first_capital_letter = acronym_capital_letters[0]
                        
                        if acronym in abbrev_map.keys() and acronym_map.get(acronym) is not None:
                            continue
                        if acronym is None:
                            continue
                        
                        if(acronym_index - LENGTH_OF_ACRONYM * 2 < 0):
                            max_distance_left = 0
                        else:
                            max_distance_left =  acronym_index - LENGTH_OF_ACRONYM * 2

                        if(acronym_index + 1 + LENGTH_OF_ACRONYM * 2 >LENGHT_OF_TOKENIZED_TEXT):
                            max_distance_right = LENGHT_OF_TOKENIZED_TEXT
                        else:
                            max_distance_right =  acronym_index + 1 + LENGTH_OF_ACRONYM * 2 
                        abbrev_map[acronym]=[]

                        if acronym_index - LENGTH_OF_ACRONYM >= 0 and acronym_index + 1 + LENGTH_OF_ACRONYM <= LENGHT_OF_TOKENIZED_TEXT:
                            stopwordleft = 0
                            last_word_index = -1
                            first_word_index = -1
                            
                            
                            # Find index of last word of the acronym
                            for left_index in reversed(range(max_distance_left, acronym_index)):
                                if (last_word_index==-1 and tokenized_text[left_index].lower()[0]!= str(acronym_last_capital_letter)) or tokenized_text[left_index] in stop_words:
                                    continue
                                else:
                                    last_word_index = left_index
                                    break
                            # See if there any stopwords in the acronym
                            if (last_word_index!= -1):
                                for left_index in range(last_word_index + 1 - LENGTH_OF_ACRONYM, last_word_index+1):
                                    if tokenized_text[left_index] in stop_words or tokenized_text[left_index] in string.punctuation or tokenized_text[left_index] in acronym_list.keys():
                                        stopwordleft +=1

                                for token in reversed(range(max_distance_left, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in string.punctuation or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token - stopwordleft:acronym_index]))
                                abbrev_map[acronym].append(" ".join(tokenized_text[last_word_index + 1 - LENGTH_OF_ACRONYM - stopwordleft:last_word_index + 1]))
                            else:
                                for token in reversed(range(max_distance_left, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in string.punctuation or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token - stopwordleft:acronym_index]))
                               
                            for right_index in range(acronym_index + 1, max_distance_right):
                                if (first_word_index == -1 and tokenized_text[right_index].lower()[0] != str(acronym_first_capital_letter)) or tokenized_text[right_index] in stop_words:
                                    continue
                                else:
                                    first_word_index = right_index
                                    break

                                
                            stopwordright = 0
                            
                            if(right_index != -1):
                                if first_word_index + LENGTH_OF_ACRONYM <= LENGHT_OF_TOKENIZED_TEXT:
                                    for right_index in range(first_word_index, LENGHT_OF_TOKENIZED_TEXT):
                                        if tokenized_text[right_index] in stop_words or tokenized_text[right_index] in string.punctuation or tokenized_text[right_index] in acronym_list.keys():
                                            stopwordright +=1
                                for token in reversed(range(max_distance_right, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in string.punctuation or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token + stopwordright:max_distance_right]))
                                abbrev_map[acronym].append(" ".join(tokenized_text[first_word_index:first_word_index + LENGTH_OF_ACRONYM + stopwordright]))        	                    
                            else:
                                for token in reversed(range(max_distance_right, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in string.punctuation or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token + stopwordright:max_distance_right]))
                            
                            checked = False
                            for long_form in abbrev_map[acronym]:
                                # print ('line 531', acronym, long_form)
                                if(self._find_best_long_form_extended(acronym, long_form) is not None):
                                    acronym_list[acronym] = abbrev_map[acronym] = self._find_best_long_form_extended(acronym, long_form)
                                    checked = True
                                    break
                            if checked == False:
                                abbrev_map[acronym] = abbrev_map[acronym] = abbrev_map[acronym].append(" ".join(tokenized_text[max_distance_left : max_distance_right]))

                        elif acronym_index - LENGTH_OF_ACRONYM >=0:
                            stopword = 0
                            last_word_index = -1 
                            for left_index in reversed(range(max_distance_left, acronym_index)):
                                if (last_word_index==-1 and tokenized_text[left_index].lower()[0]!= str(acronym_last_capital_letter)) or tokenized_text[left_index] in stop_words:
                                    continue
                                else:
                                    last_word_index = left_index
                                    break
                            if(last_word_index!=-1):
                                for left_index in range(last_word_index - 1 - LENGTH_OF_ACRONYM, last_word_index):
                                    if tokenized_text[left_index] in stop_words or tokenized_text[left_index] in acronym_list.keys():
                                        stopword +=1
                                        continue
                                for token in reversed(range(max_distance_left, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token - stopword:acronym_index]))
                                abbrev_map[acronym].append(" ".join(tokenized_text[last_word_index  + 1 - LENGTH_OF_ACRONYM - stopword:last_word_index+1]))
                            else:
                                for token in reversed(range(max_distance_left, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token - stopword:acronym_index]))
                                
                            checked = False
                            for long_form in abbrev_map[acronym]:
                                if(self._find_best_long_form_extended(acronym, long_form) is not None):
                                    acronym_list[acronym] = abbrev_map[acronym] = self._find_best_long_form_extended(acronym, long_form)
                                    checked = True
                                    break
                            if checked == False:
                                abbrev_map[acronym] = abbrev_map[acronym]  = abbrev_map[acronym].append(" ".join(tokenized_text[max_distance_left : max_distance_right]))

                        elif acronym_index +1 + LENGTH_OF_ACRONYM <= LENGHT_OF_TOKENIZED_TEXT:
                            stopword = 0
                            first_word_index = -1
                            for right_index in range(acronym_index+1, max_distance_right):
                                if (first_word_index == -1 and tokenized_text[right_index].lower()[0] != str(acronym_first_capital_letter)) or tokenized_text[right_index] in stop_words:
                                    continue
                                else:
                                    first_word_index = right_index
                                    break
                            if(first_word_index!=-1):
                                if first_word_index + LENGTH_OF_ACRONYM <= LENGHT_OF_TOKENIZED_TEXT:
                                    for right_index in range(first_word_index, first_word_index + LENGTH_OF_ACRONYM):
                                        if right_index<LENGHT_OF_TOKENIZED_TEXT and (tokenized_text[right_index] in stop_words or tokenized_text[right_index] in acronym_list.keys()):
                                            stopword +=1
                                for token in reversed(range(first_word_index, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token + stopword:acronym_index]))
                                abbrev_map[acronym].append(" ".join(tokenized_text[first_word_index:first_word_index  + LENGTH_OF_ACRONYM + stopword]))
                            else:
                                for token in reversed(range(first_word_index, acronym_index)):
                                    if tokenized_text[token] in stop_words or tokenized_text[token] in acronym_list.keys():
                                        continue
                                    abbrev_map[acronym].append(" ".join(tokenized_text[token + stopword:acronym_index]))
                           
                            checked = False
                            for long_form in abbrev_map[acronym]:
                                if(self._find_best_long_form_extended(acronym, long_form) is not None):
                                    acronym_list[acronym] = abbrev_map[acronym] = self._find_best_long_form_extended(acronym, long_form)
                                    checked = True
                                    break
                            if checked == False:
                                abbrev_map[acronym] = abbrev_map[acronym]  = abbrev_map[acronym].append(" ".join(tokenized_text[max_distance_left : max_distance_right]))

                           
                        else:
                            abbrev_map[acronym] = None
                            acronym_list[acronym] = None
        final_map = {}

        acronyms_original = self._extract_abbr_pairs_from_str(text)
        acronyms_maddog = AcroExpExtractor_MadDog().get_acronym_expansion_pairs(text);
        
        for acronym, expansion in abbrev_map.items():
            if expansion is not None and (not acronym in acronyms_maddog.keys() or acronyms_maddog[acronym] is None or acronyms_maddog[acronym] == ""):
                acronyms_maddog[acronym] = expansion
        for acronym, expansion in acronyms_maddog.items():
            if expansion is not None and (not acronym in acronyms_original.keys() or acronyms_original[acronym] is None or acronyms_original[acronym] == ""):
                acronyms_original[acronym] = expansion

        return acronyms_original

if __name__ == "__main__":
    acroExp = AcroExpExtractor_AAAI_Schwartz_Hearst_extended_SH_Maddog_Iliya()

    r = acroExp.get_acronyms_expansions_from_text(
        "A relational database is a digital database based on the relational model of data, as proposed by E. F. Codd in 1970. A software system used to maintain relational databases is a relational database management system (RDBMS). Many relational database systems have an option of using the SQL for querying and maintaining the database."
    )
    print(r)

    r = acroExp.get_acronyms_expansions_from_text(
        "Interaction between Set1p and checkpoint protein Mec3p in DNA repair and telomere functions.\nThe yeast protein Set1p, inactivation of which alleviates telomeric position effect (TPE), contains a conserved SET domain present in chromosomal proteins involved in epigenetic control of transcription. Mec3p is required for efficient DNA-damage-dependent checkpoints at G1/S, intra-S and G2/M (refs 3-7). We show here that the SET domain of Set1p interacts with Mec3p. Deletion of SET1 increases the viability of mec3delta mutants after DNA damage (in a process that is mostly independent of Rad53p kinase, which has a central role in checkpoint control) but does not significantly affect cell-cycle progression. Deletion of MEC3 enhances TPE and attenuates the Set1delta-induced silencing defect. Furthermore, restoration of TPE in a Set1delta mutant by overexpression of the isolated SET domain requires Mec3p. Finally, deletion of MEC3 results in telomere elongation, whereas cells with deletions of both SET1 and MEC3 do not have elongated telomeres. Our findings indicate that interactions between SET1 and MEC3 have a role in DNA repair and telomere function."
    )
    print(r)

    r = acroExp.get_acronyms_expansions_from_text(
        "Topology and functional domains of the yeast pore membrane protein Pom152p.\nIntegral membrane proteins associated with the nuclear pore complex (NPC) are likely to play an important role in the biogenesis of this structure. Here we have examined the functional roles of domains of the yeast pore membrane protein Pom152p in establishing its topology and its interactions with other NPC proteins. The topology of Pom152p was evaluated by alkaline extraction, protease protection, and endoglycosidase H sensitivity assays. The results of these experiments suggest that Pom152p contains a single transmembrane segment with its N terminus (amino acid residues 1-175) extending into the nuclear pore and its C terminus (amino acid residues 196-1337) positioned in the lumen of the nuclear envelope. The functional role of these different domains was investigated in mutants that are dependent on Pom152p for viability. The requirement for Pom152p in strains containing mutations allelic to the NPC protein genes NIC96 and NUP59 could be alleviated by Pom152p's N terminus, independent of its integration into the membrane. However, complementation of a mutation in NUP170 required both the N terminus and the transmembrane segment. Furthermore, mutations in NUP188 were rescued only by full-length Pom152p, suggesting that the lumenal structures play an important role in the function of pore-side NPC structures."
    )

    print(r)
    text = """
2019–20 Columbus Blue Jackets season

The 2019–20 Columbus Blue Jackets season is the 20th season for the National Hockey League franchise that was established on June 25, 1997.

The preseason schedule was published on June 18, 2019. The September 29 game between the Blue Jackets and the St. Louis Blues was cancelled due to issues with the team's flight.
The regular season schedule was published on June 25, 2019.

Denotes player spent time with another team before joining the Blue Jackets. Stats reflect time with the Blue Jackets only.
Denotes player was traded mid-season. Stats reflect time with the Blue Jackets only.
Bold/italics denotes franchise record.
    """

    r = acroExp.get_acronyms_expansions_from_text(text)
    print(r)

    text = """
Goh Keng Swee Command and Staff College                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                                               
The Goh Keng Swee Command and Staff College (GKS CSC) is one of five officer schools of the SAFTI Military Institute of the Singapore Armed Forces (SAF).                                                                                                                      
                                                                                                                                                                                                                                                                               
Formerly known as the Singapore Command and Staff College (SCSC), the inaugural Command and Staff Course commenced in 1969 and the College was officially opened in February 1970 by the Prime Minister of Singapore, Lee Kuan Yew, at its birthplace at Fort Canning. One of i
ts first commanders was Lieutenant Colonel Ronald Wee Soon Whatt. After relocating to Marina Hill in the seventies and Seletar Camp in the eighties, it finally moved into its present premises in SAFTI in 1995. It was later named after Goh Keng Swee in 2011.              
                                                                                                                                                                                                                                                                               
The College conducts the Command and Staff Course (CSC) for career officers and the National Service Command and Staff Course (NSCSC) for selected reserve officers who have demonstrated potential for higher command and staff appointments in the SAF. Annually, a number of
 International Officers from the region are invited to attend the 10.5-month-long CSC. In 2009, students from Indonesia, South Korea, Malaysia, Philippines, China, Thailand, Brunei, India, Vietnam, New Zealand, Australia and the United States, attended the course.       
                                                                                                                                                                                                                                                                               
The GKSCSC vision is: "World Class College, First Class Experience."      
    """
    r = acroExp.get_acronyms_expansions_from_text(text)
    print(r)
    text = """Софтуер с отворен код

Софтуер с отворен код (СОК, ) е софтуер, за който притежателят на авторските права на изходния код предоставя правата за обучение, промяна и разпространение на софтуера на всекиго и за всякакви цели (или накратко софтуер с лиценз за отворен код). Софтуерът с отворен код може да бъде разработван и по кооперативен публичен начин. Софтуерът с отворен код е най-честият пример за разработване с отворен код и често бива сравнен с потребителски генерирано съдържание (техническо определение) или движения с отворено съдържание (законово определение). 
Моделът отворен код или съвместното разработване от много независими източници генерира много по-разнообразен обхват на гледна точка на дизайна и структурата на кода, отколкото разработването му само от една фирма, което позволява оцеляването му за дълъг период от време. В доклад на Standish Group (от 2008 г.) се казва, че възприемането и използването на модела на софтуер с отворен код е довело до спестявания в размер на 60 милиарда долара на година на потребителите. 
История.
През 1950-те и 1960-те компютърният опериран софтуер и компилатори са били предоставяни като част от покупки на хардуер без допълнителни такси. По това време отвореният код, формата на софтуер, която е подходяща за четене от човек се е разпространявала със софтуер, който е предоставял възможността за оправяне на грешки (бъгове) или за добавяне на нови функционалности. Университетите са използвали компютърните технологии. Много от модификациите по разработката на софтуер и писането на код са се споделяли свободно, за да се следват академичните принципи за споделянето на знания и така се появили организации, които да улесняват споделянето.
Много хора твърдят, че още от основаването на Интернет през 1969 започва и движението на отворен код докато други не правят разлика между отворен код и движението свободен софтуер.
Фондацията за свободен софтуер (ФСС) стартира 1985 г., използвайки думата „свободен“ със значение "свободна дистрибуция", а не "свободна от заплащане". След като голям брой свободни софтуери са били (и са все още) безплатни, такива свободни софтуери се свързват с това, че не струват нищо, което изглежда анти-търговско.
Края на 90-те: Създаването на отворен код.
През 1997 Ерик Реймънд публикува "Катедралата и базарът", задълбочен анализ на обществото на хакерите и принципите на отворения код. Този труд получава голямо внимание през началото на 1998 и е един от факторите, който мотивира корпорацията Нетскейп Комюникейшън да пусне своя популярен Интернет пакет Нетскейп Къмюникатор като свободен софтуер. Този код днес е основа на Mozilla Firefox и Thunderbird.
Ходът на Netscape кара Реймънд и други да потърсят начин принципите и ползите от свободния софтуер да важат и за индустрията на комерсиален софтуер. Те счели, че социалният активизъм Фондацията за свободен софтуер (ФСС) не е привлекателен за Netscape и потърсили начин да променят движението на свободен софтуер, така че да подчертае бизнес потенциала на това да се споделя отворен код. Въвеждането на нов термин било нужно, защото старият – "свободен софтуер", се оказал много объркващ за хората. За тях "свободен" означавало "безплатен" – свободен за разпространение, докато всъщност се имало предвид свободен за модификация. Новият термин разрешил този проблем и се оказал по-лесен за разбиране.
"Отворен код" е приет като термин едва през януари 1998 година, на сбирка на някои от поддръжниците на свободния софтуер в Пало Алто, Калифорния като реакция на обявяването на Netscape, че ще пусне Navigator като отворен код. Част от присъствалите на сбирката са Ерик Реймънд, Тод Андерсън, Сам Окмън, Джон Хол и Кристин Питърсън (която всъщност предлага израза "отворен код"). През следващите дни Реймънд и останалите работят върху това да популяризират новия термин. Линус Торвалдс дава много важно одобрение на следващия ден. На Фил Хюс му е предоставена възможност да публикува статия в "Linux Journal". Ричард Столман, пионерът на движението за свободен софтуер, първоначално приема термина, но след това си променя мнението. Тези, които одобряват термина, използват възможността – пускането на отворения код на Navigator, за да се освободят от идеологията и конфронтиращи конотации от термина „свободен софтуер“. Netscape пуска своя програмен код с лиценза Netscape Public License и по-късно Mozilla Public License.
Терминът получава много голям тласък на събрание, организирано от издателя Тим О'Райли през април 1998 г. Оригиналното заглавие е било „Сбирка на свободния софтуер“ и по-късно е известно като „Сбирка на отворения код“. На него присъстват някои от най-известните и влиятелните сред поддръжниците на свободния софтуер като Линус Торвалдс, Лари Уол, Браян Бехлендорф, Ерик Алман, Пол Викси, Гуидо ван Росум, Майкъл Тииман, Ерик Реймънд и Джейми Завински от Nescape. На тази среща объркването, причинено от свободен софтуер, е било обсъдено. Тииман подкрепя термина „свободен“ докато Реймънд се обявява за „отворен код“. Разработчиците подложили спора на гласуване и победителят бил обявен на пресконференция по-късно през деня. Пет дена по-късно Реймънд прави първата си публична изява, в която призовава обществото на свободния софтуер да приеме новия термин. Инициативата Отворен Код е била създадена малко след това.
Въпреки това Ричард Щалман и ФСС остро възразяват срещу подхода на новообразуваната организация. Те се опасявали, че със строго ограничения фокус на отворения код Инициативата за отворен код (ИОК) заравя философските и социалните ценности на свободния софтуер и крие въпроса за свободата на компютърните потребители. Щалман продължава да поддържа тезата, че потребителите на всеки един от термините са съюзени в борбата срещу собственическия софтуер.
През август 1999 Sun Microsystems пускат StarOffice офис пакет като свободен софтуер с лиценз GNU Lesser General Public License. Свободната версия на софтуера е преименувана на OpenOffice.org, и съществува заедно с StarOffice.
Края на 90-те: Създаването на Инициативата Отворен Код.
Инициативата Отворен Код (ИОК) е основана през февруари 1998 от Ерик Реймънд and Брус Перенс, за да стимулира употребата на новия термин „отворен код“ и да „покръсти“ новите принципи на отворен код. 
Докато Инициативата Отворен Код търси да популяризира използването на новия термин, създателите на комерсиален софтуер се оказват все по-застрашени от концепцията за свободно разпространяване на софтуер и всеобщ достъп до отворения код на приложението. Говорител на Microsoft се изказва публично по този въпрос през 2002 г., че „отвореният код е унищожител на интелектуалната собственост. Не мога да си представя нещо по-лошо от това за софтуерния и интелектуалния бизнес.“ Тази гледна точка перфектно обобщава първоначалното мнение на някои софтуерни корпорации към Свободен Софтуер с Отворен Код (ССОК). Въпреки че ССОК исторически винаги е играл роля извън популярния сектор на частното разработване на софтуер, компании като Microsoft започват да развиват официално присъствието на отворен код в Интернет. IBM, Oracle, Google и State Farm са само част от компаниите с основен публичен дял в днешния конкурентен пазар на отворен код. Налице е голяма промяна в корпоративната философия, отнасяйки се до разработването на ССОК.
Движението за свободен софтуер е основано през 1983. През 1998 група от хора се застъпват, че терминът свободен софтуер трябва да бъде заменен от софтуер с отворен код СОК като изразяване, което е по-малко амбициозно и по-комфортно за корпоративния свят. Разработчиците на софтуер може да искат да публикуват своя софтуер с лиценз с отворен код, така че всеки да може също да разработи същия софтуер или да разбере неговата вътрешна функционалност. Със софтуер с отворен код основно се дава достъп на всеки да създава свои модификации, част от тях са операционни системи и архитектури на процесори, за да ги сподели с други или в някои случаи да ги пусне на пазара. Скорес Касен и Раян посочват няколко причини, основани на политиката на отворения код, в частност високата ценност на отворения код (в сравнение с повечето платени формати), в следните категории:
"Дефиницията за Отворен Код" основно представя философията на отворен код и допълнително дефинира използването на термина, модифицирането му и преразпределянето на софтуера с отворен код. Софтуерните лицензи дават права на потребители, в противен случай лицензите ще бъдат запазени по силата на закона за авторско право на притежателите на авторските права. Няколко лиценза на софтуер с отворен код са квалифицирани в рамките на "Дефинициите за Отворен Код". Най-изтъкнат и популярен пример е Общ публичен лиценз на ГНУ (ОПЛ), който „позволява свободното разпространяване при условие, че бъдещите разработвания и приложения са със същия лиценз“, който също е изплатен. Докато разпространението на отворен код представя начин да предостави отворения код за публичен достъп, то лиценза с отворен код позволява на авторите начин да осигурят този достъп.
Етикетът "отворен код" се появява като стратегическа сесия, проведена на 7 април 1998 в Пало Алто в реакция на обявеното разпространение на Navigator (като Mozilla) с отворен код от Netscape през януари 1998. Участниците в сесията използвали пускането на Navigator с отворен код, за да изяснят потенциален конфликт, причинен от двусмислието на думата „свободен“.
За близо 20 години са събрани доказателства за разработването на затворен срещу отворен софтуер, които са предоставени от общността на разработчици в Интернет. Благодарение на тях ИОК представи случая с „отворения код“ на комерсиалния бизнес, като Netscape. ИОК се надява, че използването на етикета „отворен код“ ще елиминира неяснотата, особено за хора, които възприемат „свободния софтуер“ за анти-комерсиален. Те търсят как да дадат по-висок профил на практическите ползи от използването на свободно наличен отворен код и искат да привлекат основни софтуерни бизнес компании и други високо технологични индустрии в работата и дистрибуцията на отворен код. Перенс се опитва да регистрира „отворен код“ като търговска марка за ИОК, но този опит е бил непрактичен за стандартите на запазена марка. Междувременно поради представянето на труда на Реймънд на главния мениджър на Netscape, те пускат своя програмен код на Navigator като отворен код с благоприятни резултати. Реймънд открива за това едва когато прочита прессъобщението, като е привикан от PA на изпълнителния директор на Netscape Джим Барксдейл по-късно през деня
Дефиниции.
Организацията OSI, чийто председател за момента е Майкъл Тийман, е определила правила, по които може да се установи дали един продукт е с отворен код, или не.
Откъдето се вижда, че отворен код не означава само дадена програма да бъде с публикуван изходен код, който да е станал обществено достояние:
1. Свободно разпространение.
Лицензът, с който се разпространява програмата, не трябва по никакъв начин да забранява продажба или свободно ѝ предоставяне като компонент от друг многокомпонентен софтуер. Лицензът не може да налага плащане на роялти или други такси за авторски права, право на ползване и приходи от продажби.
2. Изходен (сорс) код.
Програмата трябва да съдържа изходния код и да позволява свободното му разпространение, вкл. в компилиран вид (ако има такъв). За случаите в някакъв вид продуктът не се разпространява заедно с кода, трябва да има инструкции откъде може да се свали безплатно от Интернет.
Сорс кодът следва да е в такъв вид, че всеки да може да го променя за своите цели и нужди. Доставянето на маскиран (обфускиран) код или на криптиран сорс код е недопустимо.
3. Допълнителни работи.
Лицензът трябва да позволява промени на кода и дописване, както и да разрешава същите да бъдат разпространявани под същия лиценз, както е на оригиналния софтуер.
4. Цялостност на авторския код.
– Лицензът може да забранява разпространение на сорс код в модифициран вид само когато лицензът позволява добавяне заедно със сорс кода на пач файлове с цел модифициране на програмата по време на изпълнение ѝ (компилиране).
– Лицензът следва още да позволява разпространение на софтуера, създаден по този начин.
– Лицензът може да изисква версия с дописания код да носи различно име или ID номер от този на оригиналния продукт.
5. Без дискриминация на лица или групи.
Лицензът не може да дискриминира хора или социални прослойки.
6. Без дискриминация на области на приложение.
Лицензът не може да ограничава ползване на програмата за определени области. Така например не може да ограничава ползването на софтуера само зао търговски дейности или само за генно инженерство напр.
7. Разпространение на лиценза.
Правата, зададени за всяка програма, следва да са задължителни за всички, които я ползват, без необходимост от допълнителни лицензи.
8. Лицензът не може да важи за определен продукт.
Правата, които предоставя лицензът, не може да зависят от това, дали програмата принадлежи към определено линукс дистро или не. Ако се извади от дистрото или се разпространява отделно, всички нейни части остават подвластни на условията от лиценза на оригиналното дистро.
9. Лицензът не може да ограничава друг софтуер.
Лицензът не следва да налага ограничения върху друг софтуер, който се разпространява заедно с лицензирания. Така например лицензът не може да изисква всички останали програми от едно дистро или пакет да бъдат също с отворен код.
10. Лицензът трябва да е технологично независим.
Никоя клауза на лиценза не може да касае конкретна технология или даден тип интерфейс.
Лицензионен режим и правна рамка.
Лицензът определя правата и задълженията, с които лицензиантите трябва да се съобразяват. Обикновено притежателите на лиценз за софтуер с отворен код имат право да копират, променят и разпространяват кода (съдържанието). Лицензът може да наложи и задължения (напр. всички промени по кода, който подлежи на разпространение, трябва указват приноса на автора им).
Авторите дават лицензи върху собствената си работа, изхождайки от принципа, че те държат авторските права върху продукта си. Давайки лиценз за копиране, промяна и разпространяване на работата им, авторите един вид отдават авторските си права. Авторът все още е носител на авторските си права, но лицензиантът има правото да ги използва, ако това не противоречи на задълженията, упоменати в лиценза. Авторът има възможността да продаде или назначи срещу лиценз изключителните си авторски права върху работата, давайки контрола върху тях на новия им собственик. Притежанието на авторското право се различава от притежанието на самия продукт – копие на код (текст, книга...) може да бъде притежаван без правото да се копира, променя или разпространява.
Участието в отворен проект (напр., Apache.org) става с изрично упоменат лиценз или подразбиращ се такъв. Някои отворени проекти използват код без наложен лиценз, но въпреки това се нуждаят от притежениято на авторските права, за да включат кода в проекта (напр., OpenOffice.org и договорката Joint Copyright Assignment).
Поставянето на код или съдържание на публично място е вид отказ на автора (собственика) от авторските му права върху тази работа. Когато съдържанието на една работа е публично достъпно, не се изисква лиценз за копиране, промяна или разпространение.
Примери за лицензи на продукти с отворен код са Apache License, BSD license, GNU General Public License, GNU Lesser General Public License, MIT License, Eclipse Public License и Mozilla Public License.
Разпространението на лицензите за отворен код е една от отрицателните страни на движението за отворен код, защото често буквичките на закона са трудно различими между различните лицензи. Наличието на повече от 180 000 проекта с отворен код и повече от 1400 уникални лиценза, води до драстично усложняване на управлението на проекти с отворен код при наличието на такива със затворен код. Някои лицензи са локални, а други са произлезли от FOSS (Free and open-source software) лицензи, като Berkeley Software Distribution (BSD), Apache, MIT-лиценз (Massachusetts Institute of Technology) или GNU General Public License (GPL). От тази гледна точка, практикуващите отворен код започват да използват класификации, които групират FOSS лицензите (обикновено въз основа на задълженията, наложени от носителя на авторските права).
През 2008 беше постигнат важен етап за движението за отворен код от правна гледна точка, когато апелативният съд на САЩ отсъжда, че лицензите на свободния софтуер са обвързани с правните норми при работа с авторско право и подлежат на регулиране от съществуващия закон за авторско право и сродните му права. В резултат на това, ако крайните потребители нарушат условията на лиценза, той се прекратява, поради нарушаване на авторското право.
Разпространение на понятието.
Модел на развитие.
В своето есе от 1997 "Катедралата и базарът", Ерик Реймънд предлага модел за развитие на OSS, известен като модела "базар". Реймънд оприличава разработването на софтуер с традиционните методологии за строежа на катедрала, „внимателно изработени от отделни магьосници или малки групи от магове, които работят в пълна изолация“. Той предлага, целият софтуер да се развива с помощта на стила базар, който той описва като „чудесен бърборещ базар на различни програми и подходи.“ 
В традиционния модел на развитие, който той нарича модел на катедралата, развитието се извършва централизирано. Ролите са ясно дефинирани. Ролите включват хора, посветени на проектиране (архитектите), хората, отговорни за управлението на проекта, както и хора, които отговарят за изпълнението. Традиционното софтуерно инженерство следва модела на катедралата. В своята книга "The Mythical Man-Month" Фред Брукс застъпва този модел. Той отива по-далеч, казвайки, че за да се запази целостта на архитектурната система, проектирането на системата трябва да бъде направено от колкото е възможно по-малко архитекти.
Моделът базар, обаче, е различен. В този модел, ролите не са ясно дефинирани. Gregorio Robles показва, че софтуер, разработен по модела базар трябва да има следните модели:
Потребителите трябва да бъдат третирани като съразработчициПотребителите се третират като съразработчици и те трябва да имат достъп до изходния код на софтуера. Освен това, потребителите биват насърчавани да представят допълнения към софтуера – код поправки за софтуера, доклади за грешки, документация и т.н. увеличаването на съразработчици увеличава и скоростта, с която се развива софтуера. В закона на Линус (Linus's Law) се твърди: „Предоставяйки достатъчно очи всички грешки стават видими.“ Това означава, че ако много потребители имат достъп до изходния код, те в крайна сметка ще намерят всички грешки и да предложат как да се оправят. Трябва да се вземе предвид, че някои потребители са с напреднали програмни умения, а освен това, компютърът на всеки потребител осигурява допълнителна среда за тестване. Тази нова среда за тестване предлага способността да се намери и да определи нов „бъг“.Ранните версииПървата версия на софтуера трябва да бъде пусната възможно най-рано, така че да се увеличат шансовете за по-бързо намиране на съразработчици.Честата интеграцияПромените по кода следва да бъдат интегрирани (обединени в обща база код) възможно най-често, така че да бъде избегната необходимостта от оправянето на голям брой грешки в края на жизнения цикъл на проекта. Някои проекти с отворен код имат нощна разработка, където интегрирането се извършва автоматично на база на дневната.Няколко версииТрябва да има най-малко две версии на софтуера. Трябва да има buggier версия с повече функции и по-стабилна версия с по-малко възможности. Buggy версията (наричана също версия на разработка) е за потребители, които искат незабавното използване на най-новите функции, и са готови да приемат риска от използването на код, който все още не е старателно тестван. Потребителите могат след това да действат като съразработчици – да докладват проблеми и да осигуряват корекции за тях.Висока модуларизацияОбщата структура на софтуера трябва да бъде модулно позволяваща паралелно развитие на независими компоненти.Структура за динамично взимане на решенияНалице е необходимост от структура за вземане на решения, независимо дали формална или неформална, което прави стратегически решения зависими от променящите се потребителски изисквания и други фактори. Вж Екстремно програмиране.Данните показват, обаче, че OSS не е толкова демократична както модел на базар предполага. Анализ на пет милиарда байта безплатен / отворен код от 31 999 разработчици показва, че 74% от кода е написан от най-активните 10% от автори. Средният брой на автори, участващи в проект е 5,1, с медианата при 2.
Макар "отворен код" да изглежда тясно свързано понятие със света на програмирането, смисъла му и ползите от него все повече се разпростират. Наглед неразбираемите термини като "култура с отворен код" или "журналистика с отворен код", които някои от последователите на движението налагат и развиват, добиват все повече смисъл. Разбира се налага се промяна на принципите отнасящи се пряко за софтуера, като по-скоро говорим за "отворено съдържание", но основната идеология на отворения код е запазена.
Простичък пример за това са блоговете, които срещаме ежедневно. Съдържанието в тази енциклопедия също е добър пример за това що е то "отворен код" и колко бързо се развиват продуктите с него.
Предимства и недостатъци.
Софтуерни експерти и изследователи на софтуера с отворен код са идентифицирали няколко предимства и недостатъци. Основното предимство за бизнеса е, че отвореният код е добър начин за постигне на по-голямо проникване на пазара. Фирмите, които предлагат софтуер с отворен код, са в състояние да създадат индустриален стандарт и по този начин да спечелят конкурентно предимство. Той също така подпомага изграждането на лоялност в разработчиците, тъй като имат усещането за по-голяма власт и чувство на частична собственост от крайния продукт. 
Също така са необходими много по-малко разходи за маркетинг и логистика за такъв софтуер. Той също помага компаниите да бъдат в крак с развитието на технологиите. Добро средство е за промотирането на имиджа на кампанията, включително и на нейните търговски продукти. Развитието на софтуера с отворен код е допринесло за бързо и с високо качество създаване на надеждни продукти, които изискват малко средства. 
Терминът „отворен код“ е бил първоначално предвиден да бъде запазена марка, но е бил определен като прекалено общ и съответно тази идея е отпаднала. Въпреки това създава потенциала за по-гъвкава технология и по-бърза иновация. Счита се за по-надежден, защото принципно има хиляди индивидуални програмисти, които тестват за проблеми и бъгове. Софтуерът е гъвкав, защото модулни системи позволяват на хората да създават най-различни интерфейси или да вкарват нови способности в програмата. Това е иновационно, тъй като програмите с отворен код са продукт на сътрудничеството между голям брой различни програмисти. Смесицата от различаващи се гледни точки и корпоративни цели, както и на лични цели ускорява иновациите. 
Освен това, свободния софтуер може да се развива в съответствие с чисто техническите изисквания. Липсва търговски натиск, който често намалява качеството на софтуера. Такъв натиск принуждава традиционните софтуерни разработчици да обръщат повече внимание на изискванията на клиентите, отколкото на изискванията за сигурност, тъй като тези функции са донякъде невидими за клиента. 
Понякога се казва, че процесът за разработването на софтуер с отворен код не може добре да бъде дефиниран, което включва и етапите в процеса на развитие, като например тестването и документацията на системата могат да бъдат пренебрегнати. Все пак това е вярно само за малки (най-вече с един програмист) проекти. По-големи, успешни проекти налагат и прилагат някакви правила, защото трябва да се направи възможна работата в екип. В най-сложните проекти тези правила могат да бъдат толкова строги, че да налагат преглед дори на незначителна промяна от двама независими разработчици. 
Не всички инициативи за изграждане на софтуер с отворен код са били успешни, например SourceXchange и Eazel. Софтуерни експерти и изследователи, които не са убедени в способността на отворения код да произвежда качествени системи, идентифицират като основните проблеми неясния процес, късното откриване на дефекти и липсата на емпирични доказателства. Освен това е трудно да се изработи стабилен търговски бизнес модел около парадигмата на отворения код. Следователно, само техническите изисквания могат да бъдат изпълнени, но не и изискванията на пазара. По отношение на сигурността, отвореният код може да позволи на хакери да разберат за слабостите или пропуските на отворения софтуера по-лесно от затворения. Има зависимост от контролни механизми, за да се създаде ефективна работа на автономни агенти, които участват във виртуални организации. 
Инструменти за разработка.
В разработката на "софтуер с отворен код", участниците, повечето от които са доброволци, са разпределени сред различни географски райони, така че има необходимост от инструменти, които да им помагат да си съдействат в правенето на отворен код. Често, тези инструменти също са с "отворен код".
Системи за контрол на версиите като Concurrent Versions System (CVS), Subversion (SVN), Git и GNU Compiler Collection са примери за инструменти, които помагат с управлението на файловете на отворения код и с промяната на тези файлове за софтуерен проект. Тези инструменти също са "софтуер с отворен код".
Средства, които автоматизират тестването, компилирането и докладването за "бъгове" помагат да се запази стабилност и подкрепа на софтуерни проекти, които имат множество девелъпъри, но нямат мениджъри, контрол над качеството или техническа подкрепа. Често използвани "бъг тракери" са Bugzilla и GNATS.
Инструменти като мейлинг листи, IRC и "незабавни съобщения" доставят начини за Интернет комуникация между девелъпърите. Мрежата или уебът също играе главна роля във всичките гореспоменати системи. Някои сайтове използват всичките свойства на тези инструменти като система за управление на разработка на софтуер. Такива сайтове са GNU Savannah, SourceForge и BountySource.
Проекти и организации.
Някои от „по-видните организации“ участващи в разработката на "софтуер с отворен код" са Apache Software Foundation, създатели на Apache уеб сървъра; Linux Foundation, неправителствена организация; Eclipse Foundation, домът на софтуерната платформа за разработка Eclipse; Debian Project, създатели на влиятелната GNU/Linux дистрибуция; Mozilla Foundation, домът на уеб браузъра Firefox; и OW2, европейско общество, което разработва мидълуер с "отворен код". Новите организации са склонни да имат по-изтънчен модел на управление.
Няколко от програмите с "отворен код" са станали определящи записи в тяхното пространство. Такива програми са GIMP, система за редактиране на изображения; езикът за програмиране и среда, Java, на Сън Майкросистъмс; системата за база данни MySQL; Unix операционната система FreeBSD; офис пакета LibreOffice; и анализатора на мрежови протоколи Wireshark.
Разработката на "софтуер с отворен код" е често извършвана на живо пред публика, с помощта на безплатни услуги предлагани от Интернет, като сайтовете Launchpad и GitHub.
Open Source Software Institute е неправителствена организация, установена през 2001, която насърчава разработката и изпълнението на "софтуер с отворен код" в САЩ. Нейните усилия са насочени към насърчаването на приемането на софтуер с отворен код.
Open Source for America е група създадена с цел да повиши осведомеността във федерално правителство на САЩ за ползата от "софтуер с отворен код". Техните обявени цели са да окуражават използването на "софтуер с отворен код" в правителството и да участват в проекти за разработка на този софтуер.
Бизнес модел.
Отвореният код се е доказал през годините като нещо много повече от чиста идеология или подход, използван само от идеалисти и фанатици. Той се е превърнал в бизнес модел и начин продуктът да се развива по-бурно и по-пълноценно. Това е добре описано в есето на Ерик Реймънд "„Катедралата и базарът“".
Все пак има някои пречки пред това един продукт безпроблемно да възприеме принципите на отворения код и веднага да стане печеливш. Такива пречки са например честата липса на утвърдени срокове и планове за развитие на продукта, липсата на подходящо обучение и дори самите лицензи (някои от тях се самоналагат или ограничават продукта, като например GPL).
Разбира се, на база на отворения код са разработени различни бизнес модели, които да се справят с тези пречки и да подобрят резултатите. Но те са в употреба от скоро и тяхното поведение не е достатъчно изучено и изяснено. Пример за такъв проект е BeeKeeper.

"""
    r = acroExp.get_acronyms_expansions_from_text(text)
    print(r)
