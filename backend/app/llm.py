import os
import openai

# Load your API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY") 


def suggest_skill_gap(resume_data: dict, jd_text: str) -> str:
    """
    Given parsed resume data and raw JD text
    ask the LLM to identify missing skills.
    """
    skills = resume_data.get("skills", [])
    prompt = (
        "You are a helpful career coach.\n\n"
        f"Candidate skills: {skills}\n"
        f"Job description: {jd_text}\n\n"
        "What key skills or qualifications is the candidate missing? "
        "Respond with a bullet-point roadmap to acquire those skills."
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()
