import json
import os

class GeneratePrompt():
    __fixed_prompt_separator = "\n\n###\n\n" # Each prompt should end with a fixed separator to inform the model when the prompt ends and the completion begins. A simple separator which generally works well is \n\n###\n\n. The separator should not appear elsewhere in any prompt.
    __fixed_completion_seperator = "###" # Each completion should end with a fixed stop sequence to inform the model when the completion ends. A stop sequence could be \n, ###, or any other token that does not appear in any completion.
    __acceptable_sections = [
        'Demographics',
        'Marketing Plan Overview',
        'Visual Content',
        'Publicity',
        'Radio',
        'Radio Advertising',
        'Social Media Marketing',
        'Digital Advertising',
        'Out-Of-Home Advertising'
    ]

    def start(self):
        while(True):
            self.__get_all_user_input()

    def __get_all_user_input(self):
        sample_text = self.__get_user_input('Copy & paste sample text: ')
        section = self.__get_user_input(f'Section: ', self.__acceptable_sections)

        prompt_text = self.__generate_prompt_text(section)
        self.__write_to_json_file(sample_text, prompt_text)

    def __clean_sample_text(self, sample_text:str):
        sample_text = repr(sample_text)
        sample_text = sample_text.replace("\u201d", '"')
        sample_text = sample_text.replace("\u201c", '"')
        sample_text = sample_text.replace("\u2019", '\'')
        sample_text = sample_text.replace("\ufb02", "fl")
        sample_text = sample_text.replace("\u00e9", "é")
        sample_text = sample_text.replace("\ufb00", "ff")
        sample_text = sample_text.replace("\\\\n", "\n")
        return str(sample_text)

    def __write_to_json_file(self, sample_text: str, prompt_text:str):
        sample_text = self.__clean_sample_text(sample_text)
        sample_text = f" {sample_text}{self.__fixed_completion_seperator}" # Each completion should start with a whitespace due to our tokenization, which tokenizes most words with a preceding whitespace.
        prompt_text = f"{prompt_text}{self.__fixed_prompt_separator}"
        with open('data.jsonl', 'a') as file:
            json.dump({"prompt": prompt_text, "completion": sample_text}, file)
            file.write("\n")

    def __get_user_input(self, question:str, checklist:list = None, type:str = None) -> str:
        if type == None:
            type = str(question[:-2]).lower()
        if checklist != None:
            checklist = self.__str_items_to_lower(checklist)
        while (True):
            val = input(question)
            if checklist == None and val != None:
                break
            if checklist != None and val.lower() in checklist:
                break
            elif val == "":
                print(f"Please enter a valid {type}.")
            else:
                print(f"{val} is not an accepted {type}. Valid {type}s include: {checklist}")
        return val

    def __str_items_to_lower(self, items:list) -> list:
        for i in range(len(items)):
            items[i] = items[i].lower()
        return items

    def __generate_prompt_text(self, section:str) -> str:    
        # PROMPT TEXT
        prompt = f"""Generate a {section} section for a FACTOR Juried Sound Recording (JSR) marketing plan"""
        print(f"\nPROMPT TEXT\n{prompt}\n")
        return prompt

def main():
    # Print readme to console on running application
    with open('user_instructions.txt', 'r') as f:
        for line in f:
            if len(line) > 10:
                line = line.rstrip("\n")
            print(line)
        print("\n\n")

    GeneratePrompt().start()

if __name__ == '__main__':
    main()