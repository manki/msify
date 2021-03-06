#!/usr/bin/python -t
#
# Part of MSify project (http://code.google.com/p/msify/)
#
# Distributed under GNU GPL version 2.

"""Main executable file for MSify."""

from xml.dom import minidom
import os
import re
import popen2
import sys
import urllib
import urllib2

import config


class SifyClient(object):
    _session_id = None

    def __init__(self,
                 config_file=config.CONFIG_FILE,
                 sess_file=config.SESSION_FILE):
        """Initializer.

        Arguments:
          config_file: Path to the configuration file.
          sess_file:   Path to the temporary session information file.
                       If this file exists, information from this file is
                       used.  Otherwise a new session is created.
        """
        self.configuration = config.Configuration(config_file)
        self.sess_file = sess_file
        self._InitSession()

    def _InitSession(self):
        if not os.path.exists(self.sess_file):
            self._CreateSession()

        self._sess = minidom.parse(self.sess_file)
        self._session_id = self._GetSessionData('sessionID')

    def Login(self):
        """Connects to the Sify broadband Internet."""
        login_url = self._GetSessionData('LoginURL')
        data = self._GetServerResponse(login_url)
        print 'Response from Sify: ' + data
        return data

    def Logout(self):
        """Logs out of Sify broadband Internet and deletes session file."""
        try:
            logout_url = self._GetUrl('Logout')
            # XXX This is a hack.  I have no idea why Sify sends an invalid
            # URL as logout URL.
            if logout_url.endswith('logout1.php'):
                logout_url = logout_url.replace('/logout1.php', '/logout.php')
            data = self._GetServerResponse(logout_url)
            print 'Response from Sify: ' + data
            return data
        finally:
            os.unlink(self.sess_file)
            self._sess = None
            self._session_id = None

    def _GetServerResponse(self, url, headers={}):
        """POSTs data got from self._FormatPostData() to url and
        returns whatever response server sends back.

        Arguments:
          url: URL to be requested.
          headers: HTTP headers to be sent ({header: value, ...})
        """
        data = self._FormatPostData()
        request = urllib2.Request(url, data=data, headers=headers)
        opener = urllib2.build_opener()
        strm = opener.open(request)
        resp = strm.read()
        strm.close()
        return resp

    def _FormatPostData(self):
        """Formats POST data to be passed on to Sify.

        Returns:
            Data that can be POSTed to Sify servers.
        """
        data = { 'macaddress': self.configuration.NetSetting('macaddress'),
                 'version': '2.52',
                 'srcip': self.configuration.NetSetting('localip'),
                 'username': self.configuration.AuthenticationSetting('username'),
                 'password': self.configuration.AuthenticationSetting('password') }

        if self._session_id:
            data['sessionid'] = self._session_id

        return urllib.urlencode(data)

    def _CreateSession(self):
        """Talks to Sify server and gets session information.

        Session information includes Session ID, Login URL, Logout URL,
        and a lot other URLs.  This method gets the session info (which
        is in XML format) and saves it in session file.
        """
        HOST = '202.144.65.70'
        PORT = 8090
        URI = '/'
        USER_AGENT = 'BBClient'

        url = 'http://%s:%s%s' % (HOST, PORT, URI)
        resp = self._GetServerResponse(url, headers={'User-Agent': USER_AGENT})
        out = open(self.sess_file, 'w')
        out.write(resp)
        out.close()

    def _GetSessionData(self, tag):
        """Reads session data file and returns data contained in tag."""
        if not self._sess:
            self._InitSession()
        elts = self._sess.getElementsByTagName(tag)
        if len(elts) == 0:
            raise ValueError('Tag %s is not found in session file.' % tag)
        return elts[0].firstChild.nodeValue

    def _GetUrl(self, name):
        """Returns the URL whose name is specified.

        Reads session information for getting the URLs.
        """
        if not self._sess:
            self._InitSession()
        urls = self._sess.getElementsByTagName('Urls')[0]
        elt = urls.getElementsByTagName(name)[0]
        return elt.getAttribute('url')


def PrintXml(xml_string):
    """Print given XML string on console."""
    output = None
    try:
        import BeautifulSoup
        output = BeautifulSoup.BeautifulSoup(xml_string).prettify()
    except ImportError:
        output = xml_string
    print output


def main(args):
    """Main entry point function -- when invoked, connects to Sify broadband.

    To get connection parameters, it reads ./.sify file.  It uses
    ./.sifysess as temporary session information file.
    """
    client = SifyClient()

    if args[1] == 'i':       # i -> sign in
        PrintXml(client.Login())
    elif args[1] == 'o':     # o -> sign out
        PrintXml(client.Logout())
    else:
        print 'Unknown option %s' % args[1]


if __name__ == '__main__':
    main(sys.argv)
