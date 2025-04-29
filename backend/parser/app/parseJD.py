import time
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def extract_linkedin_job_async(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        
        await page.wait_for_timeout(5000)  # Wait 5 seconds for the page to fully load

        html = await page.content()
        await browser.close()
        
    soup = BeautifulSoup(html, "html.parser")
    job_info = {}

    # Title
    title = soup.find('h1')
    job_info['title'] = title.get_text(strip=True) if title else None

    # Company
    company = soup.find('a', class_='topcard__org-name-link')
    if not company:
        company = soup.find('span', class_='topcard__flavor')
    job_info['company'] = company.get_text(strip=True) if company else None

    # Location
    location = soup.find('span', class_='topcard__flavor topcard__flavor--bullet')
    job_info['location'] = location.get_text(strip=True) if location else None

    # Employment Type and Industries
    job_info['employment_type'] = None
    job_info['industries'] = None
    criteria_blocks = soup.find_all('li', class_='description__job-criteria-item')
    for block in criteria_blocks:
        header = block.find('h3').get_text(strip=True).lower()
        value = block.find('span').get_text(strip=True)
        if 'employment type' in header:
            job_info['employment_type'] = value
        if 'industries' in header:
            job_info['industries'] = value

    # Full Job Description
    description_block = soup.find('div', class_='show-more-less-html__markup')
    job_info['full_description'] = description_block.get_text(separator="\n", strip=True) if description_block else None

    return job_info


def split_job_description(full_description):
    """
    Split LinkedIn job description into structured sections.
    """
    sections = {
        "responsibilities": None,
        "required_qualifications": None,
        "preferred_qualifications": None,
        "other": None,
    }
    # Normalize
    text = full_description.replace("\r", "").strip()

    # Define simple section headings to split on
    patterns = {
        "responsibilities": r"(responsibilities|what you'll do|duties)",
        "required_qualifications": r"(required qualifications|basic qualifications|must have|requirements)",
        "preferred_qualifications": r"(preferred qualifications|nice to have|would be great if)",
    }

    # Find split points
    split_points = {}
    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            split_points[match.start()] = section

    if not split_points:
        # Nothing matched, fallback
        sections["other"] = text
        return sections

    # Sort split points
    sorted_points = sorted(split_points.items())
    sorted_points.append((len(text), None))  # Add end of text

    # Extract sections
    for idx in range(len(sorted_points) - 1):
        start_idx, section = sorted_points[idx]
        end_idx, _ = sorted_points[idx + 1]
        extracted_text = text[start_idx:end_idx].strip()

        if section:
            sections[section] = extracted_text

    return sections


# Step 1: Scrape full_description
# url = 'https://www.linkedin.com/jobs/view/4215657027/?alternateChannel=search&refId=l0Y1nQXsuWT3weM4a3zs%2Fw%3D%3D&trackingId=3iqJ%2Fqp2QBpUbhWpR7Nufg%3D%3D'
# job_data = await extract_linkedin_job_async(url)

# # Step 2: Split full_description into sections
# if job_data.get("full_description"):
#     split_sections = split_job_description(job_data["full_description"])
#     job_data.update(split_sections)

# # Step 3: (Optional) Remove full_description if you only want clean fields
# del job_data["full_description"]

# print(job_data.keys())
# # Now job_data looks clean
# for k, v in job_data.items():
#     print(f"{k}: {v}\n")