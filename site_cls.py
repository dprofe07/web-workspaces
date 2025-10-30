class Site:
    def __init__(self, name, url, is_sep=False):
        self.name = name
        self.url = url
        self.is_sep = is_sep

    def to_html(self, index):
        if not self.is_sep:
            return f'''\
    <div class="site-item" data-index="{index}" onclick="loadSite('{self.url}')">
        {self.name}
            <span class="controls-site">
                <span onclick="moveSiteUp({index});event.stopPropagation()">▵</span>
                <span onclick="moveSiteDown({index});event.stopPropagation()">▿</span>
                <span class="delete-btn" onclick="deleteSite({index});event.stopPropagation()">×</span>
            </span>
    </div>'''
        else:
            return f'''<div class="site-separator" data-index="{index}"/>'''

    def to_dict(self):
        if self.is_sep:
            return {'is_sep': True}
        return {
            'name': self.name,
            'url': self.url,
            'is_sep': self.is_sep,
        }

    @staticmethod
    def from_dict(data):
        if data.get('is_sep', False):
            return Site('', '', True)
        return Site(data['name'], data['url'])
