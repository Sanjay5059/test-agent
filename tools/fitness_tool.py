from langchain.tools import tool


@tool
def jogging_advice(weather_report: str) -> str:
    """
    Suggest jogging advice based on weather.
    """
    report = weather_report.lower()

    if "rain" in report:
        return "Not ideal for jogging due to rain."
    elif "haze" in report:
        return "Air quality may be poor. Morning jogging is better."
    elif "clear" in report:
        return "Excellent weather for jogging."
    elif "hot" in report:
        return "Avoid afternoon jogging. Prefer early morning."
    else:
        return "Weather is moderate for jogging."


@tool
def create_jogging_plan(weather_report: str) -> str:
    """
    Create jogging plan using weather conditions.
    """
    report = weather_report.lower()
    advice = []

    if "32" in report or "33" in report or "34" in report:
        advice.append("Avoid afternoon jogging")

    if "humidity" in report:
        advice.append("Carry water bottle")

    if "haze" in report:
        advice.append("Prefer indoor exercise if air quality worsens")

    advice.append("Best jogging time: 6 AM to 8 AM")
    advice.append("Jogging duration: 30 minutes")

    return "\n".join(advice)
