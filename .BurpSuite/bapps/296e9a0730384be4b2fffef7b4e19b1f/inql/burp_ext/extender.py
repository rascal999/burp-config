import platform

if platform.system() != "Java":
    print("Load this file inside jython, if you need the stand-alone tool run: inql")
    exit(-1)

import os
import shutil
import tempfile

from burp import (IBurpExtender, IScannerInsertionPointProvider, IExtensionStateListener)

from inql.burp_ext.editor import GraphQLEditorTab
from inql.burp_ext.scanner import BurpScannerCheck
from inql.burp_ext.generator_tab import GeneratorTab
from inql import __version__
from inql.burp_ext.timer_tab import TimerTab
from inql.utils import stop

class BurpExtender(IBurpExtender, IScannerInsertionPointProvider, IExtensionStateListener):
    """
    Main Class for Burp Extenders
    """

    def registerExtenderCallbacks(self, callbacks):
        """
        Overrides IBurpExtender method, it registers all the elements that compose this extension

        :param callbacks:  burp callbacks
        :return: None
        """
        self._tmpdir = tempfile.mkdtemp()
        os.chdir(self._tmpdir)
        helpers = callbacks.getHelpers()
        callbacks.setExtensionName("InQL: Introspection GraphQL Scanner %s" % __version__)
        callbacks.issueAlert("InQL Scanner Started")
        print("InQL Scanner Started! (tmpdir: %s )" % os.getcwd())
        # Registering GraphQL Tab
        callbacks.registerMessageEditorTabFactory(lambda _, editable: GraphQLEditorTab(callbacks, editable))
        # Register ourselves as a custom scanner check
        callbacks.registerScannerCheck(BurpScannerCheck(callbacks))
        # Register Suite Tab(s)
        self._tab = GeneratorTab(callbacks, helpers)
        callbacks.addSuiteTab(self._tab)
        callbacks.addSuiteTab(TimerTab(callbacks, helpers))
        # Register extension state listener
        callbacks.registerExtensionStateListener(self)

    def extensionUnloaded(self):
        """
        Overrides IExtensionStateListener method, it unregisters all the element that compose this extension and it will save the
        state if available.

        :return: None
        """
        os.chdir('/')
        shutil.rmtree(self._tmpdir, ignore_errors=False, onerror=None)
        stop()
        self._tab.save()
        self._tab.stop()
