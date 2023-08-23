import pandas as pd
from playwright.sync_api import sync_playwright

REGISTRO_CIVIL_URL = "https://estadisticas.sed.srcei.cl/nomrank"
l = []
years_list = [str(x) for x in range(2010, 2022)]
months_list = [str(x) for x in range(1, 13)]
sex_list = ["F", "M"]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(REGISTRO_CIVIL_URL)
    for sex in sex_list:
        page.locator("select >> nth=2").select_option(sex)
        for year in years_list:
            page.locator("select >> nth=0").select_option(year)
            for month in months_list:
                page.locator("select >> nth=1").select_option(str(month))
                search_btn = page.query_selector("div>>button")
                search_btn.click()
                page.wait_for_timeout(5000)
                last_page_number = page.query_selector_all("a.paginate_button")[
                    -2
                ].inner_text()

                for i in range(0, int(last_page_number) - 1):
                    data_entries = page.query_selector_all("tbody >> tr")
                    for data in data_entries:
                        data_list = data.inner_text().replace("\t", " ").split()
                        name = data_list[0]
                        count = data_list[1]
                        l.append(
                            {
                                "name": name,
                                "count": count,
                                "gender": sex,
                                "year": year,
                                "month": month,
                            }
                        )
                    page.wait_for_timeout(250)
                    try:
                        page.query_selector_all("a.paginate_button")[-1].click()
                    except:
                        print("Error")
                print(
                    "Pagina {} de {} para datos del año {}".format(
                        i, last_page_number, year
                    )
                )

df = pd.DataFrame.from_records(l)
df.to_csv(f"Nombres {str(year[0])}-{str(year[-1])}.csv")
