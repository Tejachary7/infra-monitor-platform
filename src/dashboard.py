from pathlib import Path
from datetime import datetime

DASHBOARD = Path("dashboard/dashboard.html")


def generate_dashboard(all_metrics):

    DASHBOARD.parent.mkdir(exist_ok=True)

    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>Infrastructure Dashboard</title>

<style>

body {{
    font-family: Arial;
    background:#f4f4f4;
    margin:40px;
}}

h1 {{
    color:#1565c0;
}}

table {{
    width:100%;
    border-collapse:collapse;
}}

th,td {{
    border:1px solid #ccc;
    padding:10px;
    text-align:center;
}}

th {{
    background:#1565c0;
    color:white;
}}

.good {{
    color:green;
    font-weight:bold;
}}

.bad {{
    color:red;
    font-weight:bold;
}}

</style>

</head>

<body>

<h1>Infrastructure Monitoring Dashboard</h1>

<p>Generated: {datetime.now()}</p>

<table>

<tr>

<th>Server</th>

<th>CPU</th>

<th>Memory</th>

<th>Disk</th>

<th>Nginx</th>

<th>SSH</th>

<th>HTTP</th>

</tr>
"""

    for metrics in all_metrics:

        nginx = metrics["services"]["nginx"]["status"]
        ssh = metrics["services"]["ssh"]["status"]

        html += f"""

<tr>

<td>{metrics["server"]["name"]}</td>

<td>{metrics["resources"]["cpu"]}%</td>

<td>{metrics["resources"]["memory"]["usage_percent"]}%</td>

<td>{metrics["resources"]["disk"]["usage_percent"]}%</td>

<td class="{"good" if nginx=="active" else "bad"}">

{nginx}

</td>

<td class="{"good" if ssh=="active" else "bad"}">

{ssh}

</td>

<td>

{metrics["network"]["http"]}

</td>

</tr>

"""

    html += """

</table>

</body>

</html>

"""

    DASHBOARD.write_text(
        html,
        encoding="utf-8"
    )