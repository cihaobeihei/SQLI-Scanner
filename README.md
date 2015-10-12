# SQL Injection Scanner

Scanner structure
This is a general description about the structure of a scanner. The scanner consist of 4 phases. The communication between these phases was done via files in JSON format.


2.1 Crawling and identification of Injection points in web pages

• Input: list of web URLs.

• Output: a JSON file(s) of injection points.

Crawling web pages: The aim of this phase is to find out as many pages in the web application as possible. The crawling function takes in the start URL, the depth to crawl (optional), maximum number of URLs (optional). Open source crawlers Scrapy was used for this phase.


Identification of Injection points: After crawling a web page, injection points were identified in each of the crawled pages. An attacker can inject his attack vector at numerous points. Some of the injection points are (but are not limited to):

• GET requests parameters,
• POST requests parameters, 
• Request Headers (including cookies).

The output of this phase is a json file containing the pages and the injection points found in the page. This will be used in the subsequent phases will look similar to the one given below:
[{
  "/page.html": [{
  "type":"GET",
  "param":"foo"
  }],
  "/page2.html":[{
  "type": "Header",
  "param":"X-Requested-By"
  }]
}]


2.2 Payload generation

• Input: Bug category.
• Output: a JSON file(s) of all possible payloads.

These payloads will be injected in the injection points that have been identified in the previous phase. This phase returns a set of exploits to be tested.

Information such as the Database type, version and the current server information was sent to the next phase. The output of this phase for a SQL Injection Scanner for a LAMP installation would be something like what is shown below:

["’ or ’1’=’1", "your other payloads", ...]


2.3 Payload Injection

• Input: Output of Phase 1 and Phase 2.
• Output: a JSON file(s) of all possible exploits.

The next step is to inject every payload generated in Phase 2 into the injection points discovered in Phase 1. After each injection, exploitable pairs (injection point, payload) are identified. The output of this phase would be the list of confirmed exploits in the website. A sample output is:

[{
 "http://example.com/index.html" : [{
 method: GET/POST,
 params:
 [
 key: param1,
 value: ’ or ’1’=’1
 ]
 }]
 }]


2.4 Generate automated verification script

• Input: Output of Phase 3
• Output: list of Selenium scripts to automate the validated exploit.

For each of the exploits identified in Phase 3, an automated script is generated which proves that the exploit is indeed vulnerable. Automated scripts are generated using selenium to make all the process automated.

