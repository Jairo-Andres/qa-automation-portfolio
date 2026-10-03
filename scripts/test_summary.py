"""Convierte un reporte JUnit XML en una tabla Markdown para el resumen de GitHub Actions.

Uso: python scripts/test_summary.py "<título>" <reporte.xml>
Escribe en $GITHUB_STEP_SUMMARY si existe; si no, por consola.
"""
import os
import sys
import xml.etree.ElementTree as ET

ICONS = {"passed": "✅", "failed": "❌", "skipped": "⏭️"}


def result_of(testcase: ET.Element) -> str:
    if testcase.find("failure") is not None or testcase.find("error") is not None:
        return "failed"
    if testcase.find("skipped") is not None:
        return "skipped"
    return "passed"


def group_of(suite: ET.Element, testcase: ET.Element) -> str:
    # pytest: classname = "ui-tests.tests.test_login" -> "test_login"
    # newman: un testsuite por petición, con el nombre de la petición
    classname = testcase.get("classname", "")
    if classname.startswith("ui-tests"):
        return classname.split(".")[-1]
    return suite.get("name", classname)


def build_summary(title: str, xml_path: str) -> str:
    if not os.path.exists(xml_path):
        return f"## {title}\n\n⚠️ No se generó el reporte `{xml_path}`.\n"

    root = ET.parse(xml_path).getroot()
    suites = [root] if root.tag == "testsuite" else root.iter("testsuite")

    rows, counts = [], {"passed": 0, "failed": 0, "skipped": 0}
    for suite in suites:
        for tc in suite.findall("testcase"):
            result = result_of(tc)
            counts[result] += 1
            seconds = float(tc.get("time") or 0)
            rows.append(f"| {group_of(suite, tc)} | {tc.get('name')} | {ICONS[result]} | {seconds:.2f}s |")

    total = sum(counts.values())
    status = "✅ Todo correcto" if counts["failed"] == 0 else f"❌ {counts['failed']} fallidos"
    lines = [
        f"## {title}",
        "",
        f"**{status}** · {counts['passed']}/{total} pasados"
        + (f" · {counts['skipped']} omitidos" if counts["skipped"] else ""),
        "",
        "<details><summary>Ver cada prueba</summary>",
        "",
        "| Grupo | Prueba | Resultado | Duración |",
        "|---|---|:---:|---:|",
        *rows,
        "",
        "</details>",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    summary = build_summary(sys.argv[1], sys.argv[2])
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with open(target, "a", encoding="utf-8") as f:
            f.write(summary + "\n")
    else:
        print(summary)
