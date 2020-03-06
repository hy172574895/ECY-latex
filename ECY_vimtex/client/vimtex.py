import re

import lib.scope as scope_
import lib.vim_or_neovim_support as vim_lib

# the class must be named as 'Operate'
class Operate(scope_.Event):
    def __init__(self, source_name):
        scope_.Event.__init__(self, source_name)
        self._use_vimtex = None
        self.taxlab_path = None
        self._vimtex_candidates = []
        self._position_cookies = {}

    def _using_taxlab(self):
        if self._use_vimtex is None:
            self._use_vimtex = vim_lib.GetVariableValue('g:use_vimtex')
        return not self._use_vimtex

    def _get_taxlab_path(self):
        if self.taxlab_path is None:
            self.taxlab_path = vim_lib.GetVariableValue('g:ECY_vimtex_texlab_path')
        return self.taxlab_path

    def _get_vimtex_candiates(self):
        try:
            current_colum = vim_lib.CurrentColumn()
            current_line_text = vim_lib.CurrentLineContents()
            pre_words = current_line_text[:current_colum]
            current_line = vim_lib.CurrenLineNr()
            current_colum, filter_words, last_key = \
                self.FindStart(pre_words, r'[\w]')
            current_start_postion = \
                {'Line': current_line, 'Colum': current_colum}
            if current_start_postion != self._position_cookies:
                self._position_cookies = current_start_postion
                self._vimtex_candidates = vim_lib.CallEval('ECY_vimtex#GetCandidate()')
            current_start_postion = ''
        except:
            self._vimtex_candidates = []
        return self._vimtex_candidates

    def OnBufferEnter(self):
        msg = {}
        msg['UseTablab'] = self._using_taxlab()
        if self._using_taxlab():
            msg['TexlabCMD'] = self._get_taxlab_path()
        return self._pack(msg, 'OnBufferEnter')

    def DoCompletion(self):
        msg = {}
        msg['TriggerLength'] = self._trigger_len
        msg['ReturnMatchPoint'] = self._is_return_match_point

        msg['UseTablab'] = self._using_taxlab()
        if self._using_taxlab():
            msg['TexlabCMD'] = self._get_taxlab_path()
        else:
            msg['Candidates'] = self._get_vimtex_candiates()
        return self._pack(msg, 'DoCompletion')

    def FindStart(self, text, reg):
        # {{{
        """ 0 of lsp is means complete on the very first character
        e.g '|abc' where the | means the start-position equal 0.
        """
        start_position = len(text)
        text_len = start_position-1
        last_key = ''
        match_words = ''
        if text_len < 300:
            while text_len >= 0:
                temp = text[text_len]
                if (re.match(reg, temp) is not None):
                    match_words = temp+match_words
                    start_position -= 1
                    if text_len == 0:
                        break
                    text_len = text_len-1
                    continue
                break
            if start_position != 0:
                last_key = text[start_position-1]
            elif text_len >= 0:
                last_key = text[0]
        return start_position, match_words, last_key
# }}}
