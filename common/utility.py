import inspect
import matplotlib.pyplot as plt

def show_implementation(cls, section=None):
    SECTION_DELIMITER = "Section"
    found_section = False
    it = inspect.getsourcelines(cls)[0]
    print(it[0], end='')
    for line in it[1:]:
        if section is not None and section not in line and not found_section:
            continue
        found_section = True
        
        if SECTION_DELIMITER in line and section is not None and section not in line:
            break
        print(line, end='')
