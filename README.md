## Data Extraction and NLP - Blackcoffer

### Installation and Setup

##### For linux
```bash
python3 -m venv .venv # Making a virtual environment for isolation
source .venv/bin/activate
pip install -r requirements.txt
```
##### For windows
```powershell
python -m venv .venv
.venv/scripts/activate
pip install -r requirements.txt
```

### Extract Articles

```bash
cd article_scraper
scrapy crawl article_scraper
```
All the articles will be stored in data/articles folder.

`Note: There are 2 links in input.xlsx which doesn't exist hence gives 404. Ignore it.`

