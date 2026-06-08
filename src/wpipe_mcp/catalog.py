import json
import urllib.request
import logging

# Use a module-level logger
logger = logging.getLogger(__name__)

class StepsCatalog:
    """
    Manages the synchronization of available steps from the wisrovi SUITE.
    Synchronizes from GitHub just like the VS Code extension.
    """
    
    # URLs synchronized with the VS Code extension
    OFFICIAL_URL = "https://raw.githubusercontent.com/wisrovi/wpipe-steps/001-DEVELOPMENT/steps_catalog.json"
    COMMUNITY_URL = "https://raw.githubusercontent.com/wisrovi/wpipe-plugins/001-DEVELOPMENT/steps_catalog.json"
    
    def __init__(self):
        self.cached_steps = []
        self._load_initial_catalog()

    def _fetch_url(self, url: str) -> list:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'wpipe-mcp'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    return json.loads(response.read().decode('utf-8'))
        except Exception as e:
            logger.warning(f"Failed to fetch catalog from {url}: {e}")
        return []

    def refresh_catalog(self) -> list:
        """Fetch latest steps from both official and community repositories."""
        official = self._fetch_url(self.OFFICIAL_URL)
        community = self._fetch_url(self.COMMUNITY_URL)
        
        # Merge and mark origin
        all_steps = []
        for s in official:
            s['origin'] = 'Official'
            all_steps.append(s)
        for s in community:
            s['origin'] = 'Community'
            all_steps.append(s)
            
        if all_steps:
            self.cached_steps = all_steps
            logger.info(f"Catalog refreshed: {len(self.cached_steps)} steps found.")
        
        return self.cached_steps

    def search(self, query: str) -> list:
        """Filters cataloged steps based on a search query keyword."""
        if not self.cached_steps:
            self.refresh_catalog()
            
        query_lower = query.lower()
        results = []
        for step in self.cached_steps:
            # Match against multiple fields
            fields = [
                step.get('name', ''),
                step.get('func_name', ''),
                step.get('namespace', ''),
                step.get('description', ''),
                step.get('category', '')
            ]
            if any(query_lower in str(f).lower() for f in fields):
                results.append(step)
        return results

    def _load_initial_catalog(self):
        """Initial load with hardcoded fallbacks if offline."""
        self.cached_steps = [
            {
                "name": "http_request",
                "func_name": "HttpRequestStep",
                "namespace": "wpipe_steps.connectivity.http",
                "description": "Resilient HTTP client for REST APIs",
                "category": "Connectivity",
                "origin": "Official"
            },
            {
                "name": "postgresql_query",
                "func_name": "PostgreSQLQueryStep",
                "namespace": "wpipe_steps.databases.postgresql",
                "description": "Database worker with connection pooling",
                "category": "Databases",
                "origin": "Official"
            }
        ]
        # Attempt an immediate refresh
        try:
            self.refresh_catalog()
        except:
            pass
