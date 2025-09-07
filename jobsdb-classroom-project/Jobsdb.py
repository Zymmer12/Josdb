from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console
from rich.table import Table
from rich.text import Text
import pandas as pd
import time

def JobsDB_Category_Phuket(category):
    console = Console()
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    job_data = []

    base_url = f"https://th.jobsdb.com/th/{category}-jobs/in-%E0%B8%A0%E0%B8%B9%E0%B9%80%E0%B8%81%E0%B9%87%E0%B8%95?Page={{}}"

    page = 1
    while True:
        url = base_url.format(page)
        driver.get(url)
        time.sleep(1)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
            )
            jobs = driver.find_elements(By.CSS_SELECTOR, "article")
            if not jobs:
                break
        except:
            break

        for job in jobs:
            try:
                title_el = job.find_element(By.CSS_SELECTOR, "a[data-automation='jobTitle']")
                title = title_el.text.strip()
                job_url = title_el.get_attribute("href")
            except:
                title = "ไม่ระบุ"
                job_url = ""

            try:
                company = job.find_element(By.CSS_SELECTOR, "a[data-automation='jobCompany']").text.strip()
            except:
                company = "ไม่ระบุ"

            try:
                location = job.find_element(By.CSS_SELECTOR, "span[data-automation='jobLocation']").text.strip()
            except:
                location = "ไม่ระบุ"

            try:
                salary = job.find_element(By.CSS_SELECTOR, "span[data-automation='jobSalary']").text.strip()
            except:
                salary = "ไม่ระบุ"

            skills = "ไม่พบข้อมูล"
            if job_url:
                try:
                    driver.execute_script("window.open('');")
                    driver.switch_to.window(driver.window_handles[1])
                    driver.get(job_url)

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation='jobDescription']"))
                    )
                    desc = driver.find_element(By.CSS_SELECTOR, "[data-automation='jobDescription']").text.strip()
                    skills = desc[:300]
                except:
                    skills = "ไม่สามารถดึงสกิล"
                finally:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

            job_data.append([title, company, salary, location, skills])

        print(f"ดึงข้อมูลหน้า {page} ของสายงาน {category} ในภูเก็ตเสร็จแล้ว")
        page += 1

    driver.quit()

    table = Table(
        title=Text(f"🚀 ตำแหน่งงานสาย {category} ในภูเก็ต", style="bold magenta"),
        show_lines=True,
        header_style="bold white on dark_blue",
        row_styles=["", "dim"],
        border_style="bright_cyan",
        show_edge=True
    )
    table.add_column("ตำแหน่ง", style="bold cyan", width=25)
    table.add_column("บริษัท", style="bold green", width=20)
    table.add_column("เงินเดือน", style="bold yellow", width=12)
    table.add_column("สถานที่", style="bold magenta", width=15)
    table.add_column("สกิล / คุณสมบัติ", style="white", width=50, overflow="fold")

    for row in job_data:
        table.add_row(*row)

    console.print(table)

    df = pd.DataFrame(job_data, columns=["ตำแหน่ง", "บริษัท", "เงินเดือน", "สถานที่", "สกิล/คุณสมบัติ"])
    df.to_csv(f"JobsDB_{category}_Phuket.csv", index=False, encoding="utf-8-sig")
    print(f"บันทึก CSV สำเร็จ: JobsDB_{category}_Phuket.csv")

if __name__ == "__main__":
    category = input("กรอกสายงานที่ต้องการ (เช่น E-commerce, Data, Marketing, AI): ").strip()
    JobsDB_Category_Phuket(category)