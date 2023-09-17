import requests
from bs4 import BeautifulSoup

import cache as cache
import data as hdata
import time

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

def getESGData(company_ticker):
    try:
        response = requests.get("https://finance.yahoo.com/quote/{}/sustainability".format(company_ticker), headers=headers)
        result = {}

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all div elements with the specified class
            risk_score_divs = soup.find_all('div', class_='Va(t) D(ib) W(22%) smartphone_W(33%) Wow(bw) Bxz(bb) Px(5px)')

            # Create a dictionary to store the extracted data
            risk_scores = {}

            # Iterate through the div elements and extract the risk scores
            for div in risk_score_divs:
                risk_type = div.find('span').text.strip()
                score = div.find('div', class_='D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)').text.strip()
                risk_scores[risk_type] = score

            # Print the extracted risk scores
            for risk_type, score in risk_scores.items(): result[risk_type] = score

            # Find the div element with class "smartphone_Pt(20px)"
            total_esg_div = soup.find('div', class_='smartphone_Pt(20px)')

            # Extract the Total ESG Risk score and related information
            total_esg_score = total_esg_div.find('div', class_='Fz(36px) Fw(600) D(ib) Mend(5px)').text.strip()
            total_esg_percentile = total_esg_div.find('span', class_='Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($seperatorColor) Fz(12px) smartphone_Bd(n) Fw(500)').text.strip()
            total_esg_risk_level = total_esg_div.find('div', class_='Fz(s) Fw(500) smartphone_Pstart(4px)').text.strip()

            # Print the extracted Total ESG Risk data
            result["Total ESG Risk Score"] = total_esg_score
            result["Total ESG Percentile"] = total_esg_percentile
            result["Total ESG Risk Level"] = total_esg_risk_level

            return result
        else:
            time.sleep(1)
            print('Something went bad')
            return result
    except:
        time.sleep(1)
        print('Something went wrong')
        return result

def getESGForCompanies():
    cached_data = cache.get_cache('getESGForCompanies')
    if cached_data: return cached_data
    company_tickers = hdata.getSPCompanies()

    computed_data = map(lambda ticker: { ticker: getESGData(ticker) }, company_tickers)
    data = list(computed_data)
    cache.put_cache('getESGForCompanies', data)
    return data
    

if __name__ == "__main__":
    data = getESGForCompanies()
    print(data)