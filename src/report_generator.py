from pathlib import Path
from datetime import datetime


def generate_summary_report(metrics_list, report_type):

    report_dir = Path(f"reports/{report_type}")

    report_dir.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    report = report_dir / f"{filename}.html"

    html = f"""
<html>

<head>

<title>{report_type.title()} Infrastructure Report</title>

<style>

body {{
    font-family: Arial;
    margin: 40px;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    border:1px solid #ccc;
    padding:8px;
}}

th {{
    background:#1565c0;
    color:white;
}}

</style>

</head>

<body>

<h1>{report_type.title()} Infrastructure Report</h1>

<p>Generated : {datetime.now()}</p>

<table>

<tr>

<th>Server</th>

<th>CPU</th>

<th>Memory</th>

<th>Disk</th>

<th>Nginx</th>

<th>SSH</th>

</tr>
"""

    for metrics in metrics_list:

        html += f"""

<tr>

<td>{metrics["server"]["name"]}</td>

<td>{metrics["resources"]["cpu"]}%</td>

<td>{metrics["resources"]["memory"]["usage_percent"]}%</td>

<td>{metrics["resources"]["disk"]["usage_percent"]}%</td>

<td>{metrics["services"]["nginx"]["status"]}</td>

<td>{metrics["services"]["ssh"]["status"]}</td>

</tr>

"""

    html += """

</table>

</body>

</html>

"""

    report.write_text(html, encoding="utf-8")

    return report