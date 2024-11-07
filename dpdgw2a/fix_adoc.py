import re
import argparse
import logging
import pathlib
import os

def find_introduction_section(content):
    # Find the position of "== Introduction"
    introduction_pos = content.find("== Introduction")
    if introduction_pos == -1:
        logging.warning("Introduction section not found")
        return None
    return introduction_pos

def add_sectnums_before_introduction(content):
    introduction_pos = find_introduction_section(content)
    if introduction_pos is None:
        return content

    # Extract the substring starting from the position of "== Introduction"
    introduction_text = content[introduction_pos:]

    content = content[:introduction_pos] + "\n:sectnums:\n"+introduction_text
    return content

def find_appendix_a_section(content):
    # Find the position of "== Appendix A. "
    appendix_a_pos = content.find("== Appendix A. ")
    if appendix_a_pos == -1:
        logging.warning("appendix_a section not found")
        return None
    return appendix_a_pos

def add_unsectnums_before_appendix_a(content):
    appendix_a_pos = find_appendix_a_section(content)
    if appendix_a_pos is None:
        return content

    # Extract the substring starting from the position of "== Appendix A. "
    appendix_a_text = content[appendix_a_pos:]

    content = content[:appendix_a_pos] + "\n:sectnums!:\n"+appendix_a_text
    return content


def remove_heading_figures(content):
    # === Figure 1
    reg_exp = r'=+ Figure [1-9]+[0-9\-\.]*\n'
    content = re.sub(reg_exp, '', content)

    # === Figure 1 image:
    #reg_exp = r'=+ Figure [0-9-] image:'
    #content = re.sub(reg_exp, 'image:', content)

    # Flip & replace
    reg_exp = r'(=+ Figure [1-9][0-9\.\-]* image:\.)(.*)[\n]*(.*##Figure .*)\n'
    content = re.sub(reg_exp,
                     r'.\3\nimage::.\2',
                     content)

    # move mark out of the figure title & remove Figure 5
    reg_exp = r'.(\[#_Toc\d* \.anchor])####Figure \d*\:?\s?\. '
    content = re.sub(reg_exp,
                     r'\1\n.',
                     content)

    return content

def clean_headings(content):
    # remove empty headings
    # === 
    reg_exp = '\n=+[ ]+\n'
    content = re.sub(reg_exp,
                     '',
                     content)

    # remove '''' and replace ==  + with ==
    reg_exp = r"'+\n\n([=]+)[ ]+\+\nAppendix A\. "
    content = re.sub(reg_exp, r'\1 Appendix A. ', content)

    # remove 11.1 Heading
    reg_exp = r'\n(=+ )\d+[\.\-0-9]* (.*)\n'
    content = re.sub(reg_exp,
                     r'\n\1\2\n',
                     content)

    return content

def remove_heading_tables(content):

    # === Table 1
    reg_exp = r'=+ Table [1-9]+[0-9\-\.]*\n'
    content = re.sub(reg_exp, '', content)


    #clean table 1
    reg_exp = r'\n=+ \[\.mark\]#Table \d+#[\n]+(\[#_Toc\d* \.anchor])####Table \d*\. (.*)[\n]+(image:\..*)\[\.mark\]#+'
    content = re.sub(reg_exp, r'\n\1\n.\2\n[frame=none]\n|===\n\3\n|===\n\n',
                     content)

    # move mark out of the table title & remove table 5
    reg_exp = r'.(\[#_Toc\d* \.anchor])####Table \d*\.?\s?\. '
    content = re.sub(reg_exp,
                     r'\1\n.',
                     content)

    return content

def remove_number_in_headings(content):
    # === 11.2 Contributors
    reg_exp = r'(=+ )[0-9\.-]+ (Figure [0-9-]*)'
    content = re.sub(reg_exp, '', content)
    return content

def remove_special_marks(content):
    # remove special 
    reg_exp = r'\[\.mark\]####([^\[]+ )\[\.mark\]####'
    content = re.sub(reg_exp,
                     r'\1',
                     content)
    
    # remove note mark
    reg_exp = r'____\n(.+)\n____'
    content = re.sub(reg_exp,
                     r'\n\1\n',
                     content)
    return content

def add_id_before_section(content):
    """
    appendix_a_pos = find_appendix_a_section(content)
    if appendix_a_pos is None:
        return content

    # Extract the substring starting from the position of "== Appendix A. "
    appendix_a_text = content[appendix_a_pos:]

    content = content[:appendix_a_pos] + "\n:sectnums!:\n"+appendix_a_text
 
    """
    # find all ids in the automatically generated TOC
    reg_exp = r'\nlink:#([a-z0-9-.]+)\[([0-9. ]*)(.+) link:#([a-z0-9-.]+)\[(\d+)\]\]\n'
    matches = re.findall(reg_exp, content)
    print ("total matches = ", len(matches))
    ret_content = content
    for mm in matches:
        print("id=", mm[0])
        print("sect_number=", mm[1])
        print("title=", mm[2])
        print("link ID=", mm[3])
        print("page number=", mm[4])
        title = mm[2]
        sect_id = mm[0]
        if "." in sect_id:
            new_sect_id = re.sub('\\.', '_', sect_id)
            reg1 = f'link:#{sect_id}['
            reg2 = f'link:#{new_sect_id}['
            ret_content = ret_content.replace(reg1, reg2)
            sect_id = new_sect_id
        if "Appendix E. Important Variable-level Attribute" in title:
            print("TITLE=", title)
        ret_content = add_id_to_section_before_title(content=ret_content, title=title, sect_id=sect_id)
    return ret_content

def add_id_to_section_before_title(content, title, sect_id):
    reg_exp = f"(\n==+ {title}[ ]*\n)"
    new_reg_exp = f'\n[#{sect_id}]\\1'
    ret_content = re.sub(reg_exp, new_reg_exp, content)
    return ret_content

def fix_figure_id_cross_ref(content):
    # find all ids in the automatically generated TOC for figures
    reg_exp = r'\nlink:#([a-zA-Z0-9-._]+)\[(Figure [0-9]+)(.+)\]\n'
    matches = re.findall(reg_exp, content)
    print ("total matches = ", len(matches))
    ret_content = content
    for mm in matches:
        print("id=", mm[0])
        print("figure_number=", mm[1])
        print('title=', mm[2])
        title = mm[2]
        fig_no = mm[1]
        cross_ref_id = fig_no.lower().replace(' ', '-')
        fig_id = mm[0]
        if "_Toc166511807" in fig_id:
            print("fig_id=", fig_id)
        ret_content = remove_id_figure_table_anchor(content=ret_content, fig_id=fig_id)
        ret_content = update_figure_table_cross_id(content=ret_content, old_id=cross_ref_id, new_id=fig_id)
    return ret_content

def fix_table_id_cross_ref(content):
    # find all ids in the automatically generated TOC for figures
    reg_exp = r'\nlink:#([a-zA-Z0-9-._]+)\[(Table [0-9]+)(.+)\]\n'
    matches = re.findall(reg_exp, content)
    print ("total matches = ", len(matches))
    ret_content = content
    for mm in matches:
        print("id=", mm[0])
        print("table_number=", mm[1])
        print('title=', mm[2])
        title = mm[2]
        fig_no = mm[1]
        cross_ref_id = fig_no.lower().replace(' ', '-')
        fig_id = mm[0]
        if "_Toc166511807" in fig_id:
            print("fig_id=", fig_id)
        ret_content = remove_id_figure_table_anchor(content=ret_content, fig_id=fig_id)
        ret_content = update_figure_table_cross_id(content=ret_content, old_id=cross_ref_id, new_id=fig_id)
    return ret_content


def  remove_id_figure_table_anchor(content, fig_id):
    reg_exp = f'\n\[#{fig_id} .anchor\]\n'
    new_reg_exp = f'\n[#{fig_id}]\n'
    ret_content = re.sub(reg_exp, new_reg_exp, content)
    return ret_content

def  update_figure_table_cross_id(content, old_id, new_id):
    reg_exp = f'link:#{old_id}\['
    new_reg_exp = f'link:#{new_id}['
    ret_content = re.sub(reg_exp, new_reg_exp, content)
    return ret_content


def write_output(output_file:str, content):
    logging.info(f"Writing fixed content to the output file: {output_file}")
    with open(output_file, 'w', encoding="utf-8") as file:
        file.write(content)

def process_content(content):
    content = clean_headings(content)

    content = add_sectnums_before_introduction(content)

    content = add_unsectnums_before_appendix_a(content)
    
    content = remove_heading_figures(content=content)

    content = remove_heading_tables(content=content)

    content = remove_special_marks(content=content)

    content = add_id_before_section(content=content)

    content = fix_figure_id_cross_ref(content=content)

    content = fix_table_id_cross_ref(content=content)


    return content

def fix_asciidoc(input_file:str, output_file:str, force:bool=False):
    input_path = pathlib.Path(input_file)
    output_path = pathlib.Path(output_file)
    if not input_path.exists():
        raise FileNotFoundError(f'Adoc file does not exist: {input_file}')
    output_path.parent.mkdir(exist_ok=True, parents=True)
    if output_path.exists() and not force:
        raise FileExistsError(f"Output file already exists: {output_file}. Use --force to overwrite.")

    logging.info("Read the initial asciidoc file...")
    with open(input_file, 'r', encoding="utf-8") as file:
        content = file.read()

    content = process_content(content=content)
    write_output(output_file=output_file,content=content) 



def main()->None:
    parser = argparse.ArgumentParser(
        prog="python -m dpdgw2a.fix_adoc",
        description="Post-processing specifically for converting DPDG word document into asciidoc.")

    parser.add_argument("-i", "--adoc-input", required=True,
                        dest="adoc_input",
                        help="Path to the initial generated AsciiDoc file")
    parser.add_argument("-o", "--adoc-output", required=True,
                        dest="adoc_output",
                        help="Path to the output AsciiDoc file")

    parser.add_argument("-f", "--force", action="store_true",
                        help="Overwrite existing files without asking")
    args = parser.parse_args()

    fix_asciidoc(
        input_file=args.adoc_input,
        output_file=args.adoc_output,
        force=args.force)
    

if __name__ == "__main__":
    main()