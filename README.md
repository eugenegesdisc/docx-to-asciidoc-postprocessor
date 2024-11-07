# docx-to-asciidoc-postprocessor
This repository contains a post-processing tool designed to convert DOCX files to AsciiDoc format, specifically tailored for the Earth Science Data Systems Working Group (ESDSWG) Data Product Development Guide (DPDG). The tool ensures that the converted documents maintain the required formatting and structure, making them ready for publication and further use within the ESDSWG community.

---
## Features
- **Automated Conversion**: Converts DOCX files to AsciiDoc format.
- **Formatting Preservation**: Retains the original formatting and structure of the DOCX files by cleaning headings, checking and cleaning captions for tables and figures, enabling section numbering (sectnum) for the main parts, and disabling section numbering for front pages and appendices.
- **Cross-Referencing Correction**: Removes or cleans identification tags that are not compatible with GitHub AsciiDoc and unifies the cross-references.

## Usage
1. **Pre-process your Word DOCX**: Verify that `dpdg2.docx` has proper headings and updated cross-references.
2. **Convert to AsciiDoc**: Use the following Docker command to convert `dpdg2.docx` to AsciiDoc. Note that this command assumes a Linux environment. If running under Windows, the volume parameter for retrieving the current working directory may differ slightly.
    ```bash
    docker run --rm --volume "$PWD:/data" --user `id -u`:`id -g` pandoc/core dpdg2.docx -f docx -t asciidoc --wrap=none --markdown-headings=atx --extract-media=. -o dpdg2.adoc
    ```
3. **Download and Install the Program**: Clone the repository using the following command:
    ```bash
    git clone https://github.com/yourusername/docx-to-asciidoc-postprocessor.git
    cd docx-to-asciidoc-postprocessor
    ```
4. **Run the Post-Processing Tool**: Follow the installation instructions to install the program. Change the current working directory to the source program root. Run the following command to fix the converted AsciiDoc document.
    ```bash
    python -m dpdgw2a.fix_adoc -i /yourdocpath/dpdg2.adoc -o /yourdocpath/dpdg2_final.adoc --force
    ```

## Requirements
- Python 3.10+
- Pandoc
- Asciidoctor

## Installation
```bash
git clone https://github.com/yourusername/docx-to-asciidoc-postprocessor.git
cd docx-to-asciidoc-postprocessor
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.

---

### Short Description
"Enhancing AsciiDoc output with post-processing after Pandoc conversion from DOCX for the ESDSWG Data Product Development Guide (DPDG)."

---