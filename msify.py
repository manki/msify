#!/usr/bin/python -t
#
# Part of MSify project (http://code.google.com/p/msify/)
#
# Distributed under GNU GPL version 2.

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

import sify


class MSifyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self._client = sify.SifyClient()
        self._CreateControls()

    def _CreateControls(self):
        """Create UI controls used for the app."""
        self.resize(250, 100)
        self.setWindowTitle('MSify')

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        self.setLayout(grid)

        login = QtGui.QPushButton('Login')
        login.setGeometry(10, 10, 180, 40)
        self.connect(login, QtCore.SIGNAL('clicked()'), self._Login)
        grid.addWidget(login, 1, 1)

        logout = QtGui.QPushButton('Logout', self)
        logout.setGeometry(10, 60, 180, 40)
        self.connect(logout, QtCore.SIGNAL('clicked()'), self._Logout)
        grid.addWidget(logout, 2, 1)

        self._status = QtGui.QLineEdit(self)
        self._status.setGeometry(10, 110, 180, 40)
        self._status.setReadOnly(True)
        grid.addWidget(self._status, 3, 1)

    def _Login(self):
        response = self._client.Login()
        self._ShowStatus(self._ExtractResult(response))
        self._ShowRenewalMessge(response)

    def _Logout(self):
        response = self._client.Logout()
        self._ShowStatus(self._ExtractResult(response))

    def _ExtractResult(self, response_xml):
        """Extract ReplyMessage element from response XML and return it."""
        tag = 'ReplyMessage'
        start = response_xml.index('<%s>' % tag) + len(tag) + 2  # +2 for < and >
        end = response_xml.index('</%s>' % tag)
        return response_xml[start:end]

    def _ShowRenewalMessge(self, response_xml):
        """Show renewal reminder to the user, if any present in response_xml.

        Requires BeautifulSoup to be available.  If BeautifulSoup is not
        installed, behaves like a no-op.
        """
        try:
            import BeautifulSoup
        except ImportError:
            return None
        soup = BeautifulSoup.BeautifulStoneSoup(response_xml)
        elt = soup.find('renewals', flag='Y')
        if not elt:
            return None
        r = QtGui.QMessageBox.information(self,
                                          'Renewal Reminder', elt['message'],
                                          'Renew now', 'Not now', '',
                                          1)   # "Not now" button is default selection
        if r == 0:
            self._OpenBrowser(elt['url'])

    def _ShowStatus(self, status):
        """Display status text to the user."""
        self._status.setText(status)

    def _OpenBrowser(self, url):
        browser = QtCore.QProcess(self)
        browser.start('firefox', [url])


def main(args):
    app = QtGui.QApplication(args)
    window = MSifyWindow()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    import pdb
    sys.exit(main(sys.argv))
