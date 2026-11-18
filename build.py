# src/template.html + src/data.js -> index.html
from pathlib import Path
r=Path(__file__).parent
t=(r/"src/template.html").read_text(encoding="utf-8"); d=(r/"src/data.js").read_text(encoding="utf-8")
(r/"index.html").write_text(t.replace("/*__DATA__*/",d),encoding="utf-8"); print("built index.html")
