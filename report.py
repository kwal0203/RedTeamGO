import streamlit as st
import csv

PATH = "tester.csv"


def generate_html_table_response_eval(data):
    # Start the HTML table with border styles
    html = '<table style="border-collapse: collapse; width: 100%;">'
    # Add table headers with bold black borders
    html += """
        <tr style="border: 2px solid black; background-color: white; text-align: center;">
            <th style="border: 2px solid black; padding: 8px;">Evaluation Passed</th>
            <th style="border: 2px solid black; padding: 8px;">Response</th>
            <th style="border: 2px solid black; padding: 8px;">Reason</th>
            <th style="border: 2px solid black; padding: 8px;">Repair Model</th>
        </tr>
    """

    # Add table rows with lighter shades of red and green
    for row in data:
        # Determine the row color based on the eval_passed value
        color = "#15f60a" if row["eval_passed"].lower() == "true" else "#ffd1d1"
        html += f'<tr style="background-color: {color}; border: 2px solid black;">'
        html += f'<td style="border: 2px solid black; padding: 8px;">{row["eval_passed"]}</td>'
        html += (
            f'<td style="border: 2px solid black; padding: 8px;">{row["response"]}</td>'
        )
        html += (
            f'<td style="border: 2px solid black; padding: 8px;">{row["reason"]}</td>'
        )
        if row["eval_passed"].lower() == "true":
            html += f'<td style="border: 2px solid black; padding: 8px; text-align: center;"><span style="font-size: 36px;">✅</span></td>'
        else:
            html += f'<td style="border: 2px solid black; padding: 8px; text-align: center;"><button style="background-color: red; color: white; border: none; font-size: 16px; font-weight: bold; padding: 8px; border-radius: 5px; cursor: pointer;">REPAIR</button></td>'
        html += "</tr>"

    # End the HTML table
    html += "</table>"

    return html


# Function to create the report content
def create_report_response_eval():
    results = []

    success, total = 0, 0
    with open(file=PATH, mode="r") as f:
        csv_reader = csv.reader(f, delimiter=",")
        for row in csv_reader:
            results.append(
                {"eval_passed": row[0], "response": row[1], "reason": row[2]}
            )
            if row[0].lower() == "false":
                success += 1
            total += 1

    html_table = generate_html_table_response_eval(results)

    return html_table, success, total


def create_report_asr(success, total):
    # Calculate the attack success rate
    attack_success_rate = int((success / total) * 100) if total > 0 else 0
    color = "#f60a0a"
    if attack_success_rate < 50:
        color = "#15f60a"
    html = f"""
        <table style="border-collapse: collapse; width: 100%; margin-top: 20px; border: 2px solid black;">
            <tr style="border: 2px solid black; background-color: white; text-align: center;">
                <th style="border: 2px solid black; padding: 8px;">Successful Attacks</th>
                <th style="border: 2px solid black; padding: 8px;">Attempted Attacks</th>
                <th style="border: 2px solid black; padding: 8px;">Attack Success Rate (%)</th>
            </tr>
            <tr style="background-color: {color}; border: 2px solid black; text-align: center; font-size: 36px; font-weight: bold;">
                <td style="border: 2px solid black; padding: 8px;">{success}</td>
                <td style="border: 2px solid black; padding: 8px;">{total}</td>
                <td style="border: 2px solid black; padding: 8px;">{attack_success_rate}</td>
            </tr>
        </table>
    """

    return html


center_title_css = """
<style>
.centered-title {
    text-align: center;
}
</style>
"""

# Inject the custom CSS
st.markdown(center_title_css, unsafe_allow_html=True)

# Create the title using st.markdown with custom CSS
st.markdown(
    '<h1 class="centered-title">Vulnerability summary</h1>', unsafe_allow_html=True
)

# Generate reports
report_html_response_eval, success, total = create_report_response_eval()
report_html_asr = create_report_asr(success=success, total=total)

# Display the attack success rate table
st.markdown(
    '<h2 class="centered-title">Attack success rate</h2>', unsafe_allow_html=True
)
st.markdown(report_html_asr, unsafe_allow_html=True)

# Display the response evaluations report content
st.markdown(
    '<h2 class="centered-title">Target model responses</h2>', unsafe_allow_html=True
)
st.markdown(report_html_response_eval, unsafe_allow_html=True)
