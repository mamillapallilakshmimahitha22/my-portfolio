# Simple PDF generator for plain text CV
# Writes a minimal PDF (one page) from `Mahitha_CV.txt` into `Mahitha_CV.pdf`.

def escape_pdf_str(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

with open('Mahitha_CV.txt', 'r', encoding='utf-8') as f:
    lines = [line.rstrip() for line in f]

# Build PDF objects
objs = []
objs.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
objs.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
page_obj = '3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n'
objs.append(page_obj.encode('utf-8'))
objs.append(b'4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')

# Build content stream
content_lines = []
for i, line in enumerate(lines):
    esc = escape_pdf_str(line)
    if i == 0:
        content_lines.append(f'({esc}) Tj')
    else:
        content_lines.append(f'T* ({esc}) Tj')

content_stream = 'BT\n/F1 12 Tf\n12 TL\n50 750 Td\n' + '\n'.join(content_lines) + '\nET\n'
content_bytes = content_stream.encode('utf-8')
content_obj = f'5 0 obj\n<< /Length {len(content_bytes)} >>\nstream\n'.encode('utf-8') + content_bytes + b'\nendstream\nendobj\n'
objs.append(content_obj)

# Write PDF with xref
with open('Mahitha_CV.pdf', 'wb') as f:
    f.write(b'%PDF-1.4\n%\xE2\xE3\xCF\xD3\n')
    offsets = []
    for obj in objs:
        offsets.append(f.tell())
        f.write(obj)
    xref_start = f.tell()
    f.write(b'xref\n0 %d\n' % (len(objs) + 1))
    f.write(b'0000000000 65535 f \n')
    for off in offsets:
        f.write(b'%010d 00000 n \n' % off)
    f.write(b'trailer\n<< /Size %d /Root 1 0 R >>\n' % (len(objs) + 1))
    f.write(b'startxref\n%d\n%%%%EOF\n' % xref_start)

print('Mahitha_CV.pdf generated.')
