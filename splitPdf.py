import os

from pypdf import PdfReader, PdfWriter

def parse_range(range_str, max_pages):
    """
    Converte una stringa del tipo '1-5,8,10-12' in una lista di indici pagina (0-based).
    """
    pages = []

    for part in range_str.split(","):
        part = part.strip()

        if "-" in part:
            start, end = map(int, part.split("-"))
            if start > end:
                raise ValueError(f"Range non valido: {part}")
            pages.extend(range(start - 1, end))
        else:
            pages.append(int(part) - 1)

    # Controllo validità
    for p in pages:
        if p < 0 or p >= max_pages:
            raise ValueError(f"Pagina {p + 1} fuori dal range del PDF.")

    return pages


def save_pdf(reader, pages, output_name):
    writer = PdfWriter()

    for p in pages:
        writer.add_page(reader.pages[p])

    with open(output_name, "wb") as f:
        writer.write(f)


def main():
    pdf_path = input("Percorso del PDF: ").strip()

    if not os.path.exists(pdf_path):
        print("File non trovato.")
        return

    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    print(f"\nIl PDF contiene {num_pages} pagine.\n")

    print("Esempi di range:")
    print("  1-10")
    print("  1-5,8,12-15\n")

    range1 = input("Range del primo PDF: ").strip()
    range2 = input("Range del secondo PDF: ").strip()

    try:
        pages1 = parse_range(range1, num_pages)
        pages2 = parse_range(range2, num_pages)

        base = os.path.splitext(pdf_path)[0]

        out1 = base + "_parte1.pdf"
        out2 = base + "_parte2.pdf"

        save_pdf(reader, pages1, out1)
        save_pdf(reader, pages2, out2)

        print("\nOperazione completata!")
        print(f"Creato: {out1}")
        print(f"Creato: {out2}")

    except Exception as e:
        print(f"\nErrore: {e}")


if __name__ == "__main__":
    main()