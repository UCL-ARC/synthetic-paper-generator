import yaml
import os
import json
import random
from pylatex import Document, Section, Subsection, Command, Figure, Table, Math
from pylatex.utils import NoEscape
from itertools import product
import uuid

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def generate_text(sentence_count=5):
    return " ".join(["This is a synthetic sentence."] * sentence_count)

def init_ground_truth():
    return {
        "title": "",
        "author": "",
        "abstract": "",
        "sections": [],
        "references": []
    }

def main():
    os.makedirs('output/tex', exist_ok=True)
    os.makedirs('output/pdf', exist_ok=True)
    os.makedirs('output/ground_truth_json', exist_ok=True)

    combinations = list(product(
        config['document_classes'],
        config['font_sizes'],
        config['columns'],
        config['include_math'],
        config['include_tables'],
        config['include_figures'],
        config['num_sections'],
        config['num_references']
    ))

    for combo in combinations[:2]:  # Limit to 2 for quick testing
        (doc_class, font_size, columns, include_math, include_tables, include_figures, num_sections, num_references) = combo
        uid = str(uuid.uuid4())
        filename_prefix = f"{uid}"

        gt = init_ground_truth()
        gt['title'] = f"Synthetic Title {uid}"
        gt['author'] = "Synthetic Author"
        gt['abstract'] = generate_text(3)

        doc = Document(documentclass=doc_class, document_options=[font_size, columns])
        doc.preamble.append(Command('title', gt['title']))
        doc.preamble.append(Command('author', gt['author']))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

        doc.append(NoEscape(r'\begin{abstract}'))
        doc.append(gt['abstract'])
        doc.append(NoEscape(r'\end{abstract}'))

        for sec_num in range(num_sections):
            section_title = f"Section {sec_num+1}"
            section_text = generate_text(5)
            gt['sections'].append({
                "title": section_title,
                "text": section_text,
                "equations": [],
                "tables": [],
                "figures": []
            })
            with doc.create(Section(section_title)):
                doc.append(section_text)

                if include_math:
                    eq = "E = mc^2"
                    gt['sections'][-1]['equations'].append(eq)
                    with doc.create(Subsection("Example Equation")):
                        doc.append(Math(data=[eq]))

                if include_tables:
                    table_text = "Example synthetic table."
                    gt['sections'][-1]['tables'].append(table_text)
                    with doc.create(Subsection("Example Table")):
                        with doc.create(Table(position='h!')) as table:
                            table.add_caption(table_text)
                            table.append(NoEscape(r'''
                            \begin{tabular}{|c|c|c|}
                            \hline
                            A & B & C \\
                            \hline
                            1 & 2 & 3 \\
                            4 & 5 & 6 \\
                            \hline
                            \end{tabular}
                            '''))

        for ref_num in range(num_references):
            ref_text = f"[{ref_num+1}] Synthetic Reference {ref_num+1}."
            gt['references'].append(ref_text)
            doc.append(NoEscape(ref_text + r'\\'))

        tex_path = f'output/tex/{filename_prefix}.tex'
        pdf_path = f'output/pdf/{filename_prefix}.pdf'
        gt_path = f'output/ground_truth_json/{filename_prefix}.json'

        doc.generate_pdf(pdf_path[:-4], clean_tex=False)

        with open(gt_path, 'w') as f:
            json.dump(gt, f, indent=2)

if __name__ == "__main__":
    main()