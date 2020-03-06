import logging
global g_logger
g_logger = logging.getLogger('ECY_server')

import utils.interface as scope_
import utils.lsp.language_server_protocol as lsp

# the class must be named as 'Operate'
class Operate(scope_.Source_interface):
    def __init__(self):
        # must same as the same defined in Client side.
        self._name = 'latex'
        self._taxlab_status = 'not started'
        self._did_open_list = {}
        self._deamon_queue = None

    def GetInfo(self):
        return {'Name': self._name, 'WhiteList': ['tex'],
                'Regex': r'[\w]', 'TriggerKey': ['\\']}

    def OnBufferEnter(self, version):
        self._check(version)
        self._did_open_or_change(version)

    def OnBufferTextChanged(self, version):
        self._did_open_or_change(version)

    def _check(self, version):
        self._deamon_queue = version['DeamonQueue']
        if version['UseTablab']:
            if self._taxlab_status == 'not started':
                self._taxlab_status = 'tried'
                self._lsp = lsp.LSP()
                self._start_taxlab_server(version['TexlabCMD'])
            if self._taxlab_status == 'started':
                return True
            return False
        return True

    def _output_queue(self, msg):
        if self._deamon_queue is not None and msg is not None:
            msg['EngineName'] = self._name
            self._deamon_queue.put(msg)

    def _start_taxlab_server(self, server_path):
        self._lsp.StartJob(server_path)
        init_msg = self._lsp.initialize()
        try:
            server_info = self._lsp.GetResponse(init_msg['Method'])
            self._taxlab_status = 'started'
            g_logger.debug(server_info)
        except:
            self._build_erro_msg(2, 'Failed to start Taxlab server')

    def _build_erro_msg(self, code, msg):
        """and and send it
        """
        msg = msg.split('\n')
        g_logger.debug(msg)
        temp = {'ID': -1, 'Results': 'ok', 'ErroCode': code,
                'Event': 'erro_code',
                'Description': msg}
        self._output_queue(temp)
        

    def _return_vimtex(self, version):
        return_ = {'ID': version['VersionID']}
        candidates = version['Candidates']
        for item in candidates:
            item['abbr'] = item['word']
            if item['kind'].find('cmd') != -1:
                item['snippet'] = item['word'] + '\{${0}\}'
        return_['Lists'] = candidates
        return return_

    def _did_open_or_change(self, version):
        '''update text to server
        '''
        # {{{ 
        if self._taxlab_status != 'started':
            return
        uri = self._lsp.PathToUri(version['FilePath'])
        text = version['AllTextList']
        # LSP require the edit-version
        if uri not in self._did_open_list:
            return_id = self._lsp.didopen(uri, 'html', text, version=0)
            self._did_open_list[uri] = {}
            self._did_open_list[uri]['change_version'] = 0
        else:
            self._did_open_list[uri]['change_version'] += 1
            return_id = self._lsp.didchange(
                uri, text, version=self._did_open_list[uri]['change_version'])
        return return_id
        # }}}

    def DoCompletion(self, version):
        g_logger.debug(version['UseTablab'])
        if not version['UseTablab']:
            return self._return_vimtex(version)
        if not self._check(version):
            return None
        return_ = {'ID': version['VersionID']}
