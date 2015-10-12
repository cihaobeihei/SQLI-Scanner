echo "scraping..."
scrapy crawl step1 > step1.txt && scrapy crawl step1login > step1login.txt && scrapy crawl step3login > step3login.txt && scrapy crawl step3 > step3.txt && python -c 'import step4; print step4.main();'
echo "next app *******************************************"
