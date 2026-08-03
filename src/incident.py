from pathlib import Path
from datetime import datetime


REPORT = Path("reports/incident_report.html")


def generate_incident_report(metrics):

    REPORT.parent.mkdir(exist_ok=True)

    html = f"""
<!DOCTYPE html>
<html>

<head>

<title>Infrastructure Incident Report</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f5f5f5;
}}

table{{
border-collapse:collapse;
width:100%;
}}

th,td{{
border:1px solid #ddd;
padding:10px;
}}

th{{
background:#2d6cdf;
color:white;
}}

h1,h2{{
color:#2d6cdf;
}}

</style>

</head>

<body>

<h1>Infrastructure Incident Report</h1>

<p><b>Generated:</b> {datetime.now()}</p>

<h2>Server</h2>

<table>

<tr><th>Name</th><td>{metrics["server"]["name"]}</td></tr>

<tr><th>Host</th><td>{metrics["server"]["host"]}</td></tr>

</table>

<h2>Resources</h2>

<table>

<tr>

<th>CPU</th>

<th>Memory</th>

<th>Disk</th>

</tr>

<tr>

<td>{metrics["resources"]["cpu"]}%</td>

<td>{metrics["resources"]["memory"]["usage_percent"]}%</td>

<td>{metrics["resources"]["disk"]["usage_percent"]}%</td>

</tr>

</table>

<h2>Services</h2>

<table>

<tr>

<th>Service</th>

<th>Status</th>

<th>Healthy</th>

</tr>
"""

    for service, info in metrics["services"].items():

        html += f"""
<tr>

<td>{service}</td>

<td>{info["status"]}</td>

<td>{info["healthy"]}</td>

</tr>
"""

    html += """

</table>

<h2>Recovery</h2>

<table>

<tr>

<th>Service</th>

<th>Action</th>

<th>Success</th>

</tr>
"""

    for service, recovery in metrics["recovery"].items():

        html += f"""

<tr>

<td>{service}</td>

<td>{recovery["action"]}</td>

<td>{recovery["success"]}</td>

</tr>

"""

    html += """

</table>

</body>

</html>

"""

    REPORT.write_text(
        html,
        encoding="utf-8"
    )