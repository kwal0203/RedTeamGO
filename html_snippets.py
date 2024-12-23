HIJACK_PASSED = """
    <div style="text-align: center;">
        <div style="border: 2px solid green; padding: 15px; background-color: #90EE90; border-radius: 10px; display: inline-block; font-family: Arial, sans-serif;">
            <p style="color: darkgreen; font-weight: bold; font-size: 18px; margin: 0 0 10px 0;">✅ Model not vulnerable to known hijacking attacks</p>
                <p style="color: darkgreen; font-weight: bold; margin: 0 0 20px 0;">Model was successfully hijacked on {success}% of hijack attempts.</p>
                <a href="http://localhost:8502" target="_blank">
                    <div style="display: flex; justify-content: center;">
                        <button style="background-color: green; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;" onclick="window.open('www.google.com', '_blank')">See report</button>
                    </div>
                </a>
            </div>
        </div>
        """


HIJACK_FAILED = """
    <div style="text-align: center;">
        <div style="border: 2px solid red; padding: 15px; background-color: #FFD1D1; border-radius: 10px; max-width: 400px; margin: auto; font-family: Arial, sans-serif;">
            <p style="color: darkred; font-weight: bold; font-size: 18px; margin: 0 0 10px 0;">❌ Model vulnerable to hijacking attacks</p>
            <p style="color: darkred; font-weight: bold; margin: 0 0 20px 0;">Model was successfully hijacked on {success}% of hijack attempts.</p>
            <div style="display: flex; justify-content: center;">
                <a href="http://localhost:8502" target="_blank">
                    <button style="background-color: red; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;" onclick="window.open('www.google.com', '_blank')">See report</button>
                </a>
            </div>
        </div>
    </div>
    """

INTERACTIVE_MODE_FAILED = """
    <div style="border: 2px solid red; padding: 15px; background-color: #FFD1D1; border-radius: 10px; max-width: 400px; margin: auto; font-family: Arial, sans-serif;">
        <p style="color: darkred; font-weight: bold; font-size: 18px; margin: 0 0 10px 0;">⚠️ Warning: Toxic language detected!</p>
        <p style="color: darkred; font-weight: bold; margin: 0 0 20px 0;">Toxicity score: {toxicity_score}%, biase score: {score_bias}%</p>
        <div style="display: flex; justify-content: space-between;">
            <button style="background-color: red; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;" onclick="window.location.href='/Patch model'">Repair model</button>
            <button style="background-color: red; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;" onclick="window.location.href='/Store prompt'">Store prompt</button>
            <button style="background-color: red; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;" onclick="window.location.href='/Ignore warning'">Ignore warning</button>
        </div>
    </div>
    """

CENTER_TITLE_CSS = """
    <style>
        .centered-title {
        text-align: center;
    }
    </style>
    """

TITLE = '<h1 class="centered-title">RedTeamGo</h1>'
