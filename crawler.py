# !/usr/bin/env python
# -*- coding: utf-8 -*-

# thanhlv
# lethanhx2k@gmail.com
# github.com/thanhleviet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

baseURL = "http://ecdc.europa.eu/en/healthtopics/antimicrobial_resistance/database/Pages/table_reports.aspx"

# driver = webdriver.Firefox()
driver = webdriver.PhantomJS('/Users/thanhlv/Downloads/phantomjs-2.0.0-macosx/bin/phantomjs')

driver.get(baseURL)

def find_by_xpath(locator):
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )

        return element
# Copied from http://stackoverflow.com/questions/26050075/filling-out-web-form-data-using-built-in-python-modules
class FormPage(object):
        def fill_form(self, data):
            find_by_xpath('//select[contains(@id,"PathogenAntibiotic")]').send_keys(data['cat'])
            find_by_xpath('//select[contains(@id,"Country")]').send_keys(data['country'])
            find_by_xpath('//select[contains(@id,"YearFrom")]').send_keys(data['yf'])
            find_by_xpath('//select[contains(@id,"YearTo")]').send_keys(data['yt'])

            return self # makes it so you can call .submit() after calling this function

        def submit(self):
            find_by_xpath('//input[contains(@id,"btnFilter")]').click()



# countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'EU/EEA','Finland', 'France', 'Germany', 'Greek', 'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia', 'Lithuania',
# 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Spain', 'Sweden', 'United Kingdom']

countries = ['EU/EEA']
cats = ["Enterococcus faecalis / Aminopenicillins", "Enterococcus faecalis / High level gentamicin", "Enterococcus faecalis / Vancomycin", "Enterococcus faecium / Aminopenicillins", "Enterococcus faecium / High level gentamicin", "Enterococcus faecium / Vancomycin", "Escherichia coli / 3rd gen. cephalosporins", "Escherichia coli / Aminoglycosides", "Escherichia coli / Aminopenicillins", "Escherichia coli / Carbapenems", "Escherichia coli / Fluoroquinolones", "Klebsiella pneumoniae / 3rd gen. cephalosporins", "Klebsiella pneumoniae / Aminoglycosides", "Klebsiella pneumoniae / Carbapenems", "Klebsiella pneumoniae / Fluoroquinolones", "Klebsiella pneumoniae / Multiple drug resistance", "Pseudomonas aeruginosa / Amikacin", "Pseudomonas aeruginosa / Aminoglycosides", "Pseudomonas aeruginosa / Carbapenems", "Pseudomonas aeruginosa / Ceftazidime", "Pseudomonas aeruginosa / Fluoroquinolones","Staphylococcus aureus / MRSA", "Staphylococcus aureus / Rifampin", "Streptococcus pneumoniae / Macrolides", "Streptococcus pneumoniae / Penicillins", u"Pseudomonas aeruginosa / Piperacillinñtaz"]


for cat in cats:
	# cat = cat.enc("utf8")
	print cat
	data = {
	'cat':cat,
	'country': 'EU/EEA',
	'yf': '1998',
	'yt': '2013',
	}
	fname = "{}_{}.csv".format(data['country'].replace("/","_"), data['cat'].replace(" / ","_"))

	if not os.path.exists(fname):

		FormPage().fill_form(data).submit()

		content = driver.find_elements_by_xpath('//td[contains(@style,"background-color")]')

		new_content = [c.text for c in content[2:]]

		list_of_groups = zip(*(iter(new_content),) * 10)

		with open(fname, "w") as f:
			csv_f = csv.writer(f)
			csv_f.writerow(['Country','Year', 'Antibiotic_Group', 'S', 'I', 'R', 'TotalN', 'pS', 'pI', 'pR'])
			for l in list_of_groups:
				csv_f.writerow(l)
				print l

driver.quit()
