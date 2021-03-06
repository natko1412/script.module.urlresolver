"""
    urlresolver XBMC Addon
    Copyright (C) 2015 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
from t0mm0.common.net import Net
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay.interfaces import PluginSettings
from urlresolver.plugnplay import Plugin
from lib import jsunpack

class FilehootResolver(Plugin, UrlResolver, PluginSettings):
    implements = [UrlResolver, PluginSettings]
    name = "filehoot"
    domains = ['filehoot.com']

    def __init__(self):
        p = self.get_setting('priority') or 100
        self.priority = int(p)
        self.net = Net()

    def get_media_url(self, host, media_id):
        
        web_url='http://filehoot.com/embed-%s.html'%media_id
        
        link = repr(self.net.http_GET(web_url).content)
        if link.find('404 Not Found') >= 0:
            raise UrlResolver.ResolverError('The requested video was not found.')

        videoUrl = []
        
        html = link.replace('\n\r', '').replace('\r', '').replace('\n', '').replace('\\', '')
        reg="file:'(.+?)','provider':'http'"
        video_link=re.findall(re.compile(reg),html)[0]
        return video_link
            

        

    def get_url(self, host, media_id):
        return 'http://%s/embed-%s.html' % (host, media_id)

    def get_host_and_id(self, url):
        r = re.search('//(.+?)/(?:embed-)?([0-9a-z]+)', url)
        if r:
            return r.groups()
        else:
            return False

    def valid_url(self, url, host):
        if self.get_setting('enabled') == 'false': return False
        return re.search('//(?:www.)?filehoot.com/(embed-)?[0-9a-z]+', url) or 'filehoot' in host
