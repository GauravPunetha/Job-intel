"""
Scrapy spider for ethical web crawling of career pages.
IMPORTANT: Only use on sites that allow crawling per robots.txt.
Always respects robots.txt and throttles requests.
"""
import scrapy
import hashlib
import re
from w3lib.html import remove_tags
from collectors.common.robots_guard import allowed_to_fetch


class CareerSpider(scrapy.Spider):
    name = "career_spider"
    custom_settings = {
        "DOWNLOAD_DELAY": 1.0,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 10,
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "JobIntelBot/1.0 (+contact@example.com)"
    }

    def start_requests(self):
        """
        Start with seed URLs. Pass via:
        scrapy runspider scrapy_spider.py -a seeds="url1,url2"
        """
        seeds = getattr(self, "seeds", "")
        for seed in [s.strip() for s in seeds.split(",") if s.strip()]:
            # Extract domain for robots.txt check
            parts = seed.split("/")
            domain = f"{parts[0]}//{parts[2]}"
            robots_url = f"{domain}/robots.txt"
            
            # Check robots.txt before fetching
            if not allowed_to_fetch(robots_url, self.custom_settings["USER_AGENT"], seed):
                self.logger.warning(f"robots.txt forbids crawling: {seed}")
                continue
            
            yield scrapy.Request(seed, callback=self.parse_list, dont_obey_robotstxt=False)

    def parse_list(self, response):
        """
        Parse job listing page.
        Adjust selectors based on the actual site structure.
        """
        # Generic selectors for job cards
        for href in response.css(".job-card a::attr(href)").getall():
            if href:
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=self.parse_job, dont_obey_robotstxt=False)
        
        # Try alternative selectors
        for href in response.css("[data-job-id] a::attr(href)").getall():
            if href:
                url = response.urljoin(href)
                yield scrapy.Request(url, callback=self.parse_job, dont_obey_robotstxt=False)

    def parse_job(self, response):
        """
        Parse individual job detail page.
        """
        # Extract title (try multiple selectors)
        title = response.css("h1::text, .job-title::text, [data-title]::text").get("").strip()
        
        # Extract description HTML
        desc_html = response.css(
            "#job-description, .job-description, .job-content, article"
        ).get("")
        
        # Clean HTML to text
        desc_text = re.sub(r"\s+", " ", remove_tags(desc_html or "")).strip()
        
        # Create dedupe signature
        domain = response.url.split("/")[2]
        signature = hashlib.sha1(
            f"{domain}|{title}|{desc_text[:300]}".encode()
        ).hexdigest()
        
        item = {
            "source": domain,
            "title": title,
            "url": response.url,
            "description_text": desc_text,
            "dedupe_signature": signature,
        }
        
        yield item
